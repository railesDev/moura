import random


def create_users(conn, c):
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, gender integer, campus text, program text, course integer, frd_goal integer, dts_goal integer, ntw_goal integer, gender_goals integer, photo_id integer, ad_text text)''')
    conn.commit()


def create_reactions(conn, c):
    c.execute('''CREATE TABLE IF NOT EXISTS reactions
                 (id INTEGER PRIMARY KEY, match_id integer, reaction integer)''')
    conn.commit()


def user_exists(c, id_):
    c.execute('''SELECT * FROM users WHERE id = ?''', (id_,))
    return c.fetchone()


def erase_user(conn, c, id_):
    c.execute('''DELETE FROM users WHERE id = ?''', (id_,))
    c.execute('''DELETE FROM reactions WHERE id = ?''', (id_,))
    c.execute('''DELETE FROM reactions WHERE match_id = ?''', (id_,))
    conn.commit()


def deactivate_user(conn, c, id_):
    c.execute("""
            UPDATE users
            SET gender = ?, gender_goals = ?, ad_text = ?
            WHERE id = ?
        """, (2, 3, '-', id_,))
    c.execute('''DELETE FROM reactions WHERE id = ?''', (id_,))
    c.execute('''DELETE FROM reactions WHERE match_id = ?''', (id_,))
    conn.commit()


def save_user(conn, c, data):
    c.execute('''INSERT INTO users (id, gender, campus, program, course, frd_goal, dts_goal, 
        ntw_goal, gender_goals, photo_id, ad_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()


def extract_user(conn, c, id_):
    c.execute('''
                SELECT id, gender, gender_goals, frd_goal, dts_goal, ntw_goal
                FROM users
                WHERE id = ?
                LIMIT 1
            ''', (id_,))
    return c.fetchone()


def find_match(conn, c, user_data):
    c.execute('''
    SELECT users.id
    FROM users
    JOIN reactions ON users.id = reactions.id
    WHERE reactions.reaction != 0 
    AND (
    (users.gender_goals = ? OR users.gender_goals = 2) AND (users.gender = ? OR ? = 2) AND (users.frd_goal*? = 1 OR users.dts_goal*? = 1 OR users.ntw_goal*? = 1)
    )
    AND users.id NOT IN (SELECT reactions.match_id FROM reactions WHERE reactions.id = users.id) 
    LIMIT 10
    ''', (user_data[1], user_data[2], user_data[2], user_data[3], user_data[4], user_data[5],))
    res = c.fetchall()
    return random.choice(res) if res else None


def get_match_data(conn, c, match_id):
    c.execute('''
    SELECT *
    FROM users
    WHERE id = ?
    LIMIT 1
    ''', (match_id,))
    match_data = c.fetchone()
    return match_data


def react(conn, c, id_, match_id_, reaction):
    c.execute(f'''
    INSERT OR IGNORE INTO reactions (id, match_id, reaction)
    VALUES (?, ?, ?)
    ''', (id_, match_id_, reaction))
    conn.commit()


def update_reaction(conn, c, id_, reaction):
    c.execute(f'''
    UPDATE reactions
    SET reaction = ?
    WHERE reaction != 2 AND id = ?
    ''', (reaction, id_))
    c.execute(f'''
    UPDATE matches
    SET reaction = ?
    WHERE reaction != 2 AND match_id = ?
    ''', (reaction, id_))
    conn.commit()


def find_like(conn, c, id_):
    c.execute('''
                SELECT id
                FROM reactions
                WHERE match_id = ? AND reaction = 1
                LIMIT 1
                ''', (id_,))
    return c.fetchone()

