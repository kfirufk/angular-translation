import sqlite3
from os import path

import xmltodict

db_file = "trans.db"
msg_file = "messages.xlf"
should_create_db = not path.exists(db_file)

con = sqlite3.connect(db_file)
cur = con.cursor()
if should_create_db:
    print("db file not find, creating table")
    cur.execute("create table trans_en (the_text TEXT PRIMARY KEY, the_text_he TEXT, the_text_fr TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP)")
print("done creating table")

print("reading messaging file...")
file = open(msg_file, 'r')
data = file.read()
file.close()
my_dict = xmltodict.parse(data, strip_whitespace=False)
data = []
for dict_line in my_dict['xliff']['file']['unit']:
    source = dict_line['segment']['source']
    source_stripped = source.strip(" \n")
    if (source_stripped,) not in data:
        data.append((source_stripped,))
print("done creating msg file, inserting to db")
cur.executemany('''insert into trans_en(the_text) values(?) on conflict(the_text) 
                    do update set updated_at=CURRENT_TIMESTAMP''', data)
con.commit()
cur.close()
con.close()
print("done adding to db")
