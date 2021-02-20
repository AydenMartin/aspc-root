import sqlite3

# temporary file path
file_path = 'C:\\Users\\tlham\\Documents\\spring.db'


# create tables and insert some sample rows
def initialize_db():
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE jobs (id int PRIMARY KEY, prog decimal(5, 2), scrap int)''')
    c.execute('''INSERT INTO jobs (id, prog, scrap) VALUES (1, 6.00, 50)''')
    c.execute('''INSERT INTO jobs (id, prog, scrap) VALUES (2, 7.45, 50)''')
    c.execute('''INSERT INTO jobs (id, prog, scrap) VALUES (3, 3.60, 50)''')
    c.execute('''INSERT INTO jobs (id, prog, scrap) VALUES (4, 12.50, 50)''')
    conn.commit()
    conn.close()


# return a job with the matching id
def get_job(id):
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''SELECT * FROM jobs WHERE id = {:d}'''.format(id))
    row = c.fetchone()
    conn.close()
    return row


# insert a job into the table
def insert_job(id, prog, scrap):
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''INSERT INTO jobs (id, prog, scrap) VALUES ({:d}, {:.2f}, {:.2f})'''.format(id, prog, scrap))
    conn.commit()
    conn.close()


# update a job with the matching id and return the old row
def update_job(id, prog, scrap):
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''SELECT * FROM jobs WHERE id = {:d}'''.format(id))
    row = c.fetchone()
    c.execute('''UPDATE jobs SET prog = {:.2f}, scrap = {:.2f} WHERE id = {:d}'''.format(prog, scrap, id))
    conn.commit()
    conn.close()
    return row


# delete a job from the table and return the row that was deleted
def delete_job(id):
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''SELECT * FROM jobs WHERE id = {:d}'''.format(id))
    row = c.fetchone()
    c.execute('''DELETE FROM jobs WHERE id = {:d}'''.format(id))
    conn.commit()
    conn.close()
    return row
