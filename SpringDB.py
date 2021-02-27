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
def insert_job(id, **columns):
    insert_cols = "id"
    insert_values = str(id)
    for k in columns.keys():
        columns[k] = str(columns[k])
    if len(columns) > 0:
        insert_cols += ", " + ", ".join(columns.keys())
        insert_values += ", " + ", ".join(columns.values())
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''INSERT INTO jobs ({}) VALUES ({})'''.format(insert_cols, insert_values))
    conn.commit()
    conn.close()


# update a job with the matching id and return the old row
def update_job(id, **columns):
    col_list = []
    for k in columns.keys():
        col_list.append(k + " = " + str(columns[k]))
    update_str = ", ".join(col_list)
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute('''SELECT * FROM jobs WHERE id = {:d}'''.format(id))
    row = c.fetchone()
    c.execute('''UPDATE jobs SET {} WHERE id = {:d}'''.format(update_str, id))
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
