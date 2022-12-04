import sqlite3
from os import path

import xmltodict

db_file = "trans.db"
msg_file = "messages.xlf"

if not path.exists(db_file):
    print("translation db file %s not found!" % db_file)
    exit(0)

con = sqlite3.connect(db_file)
cur = con.cursor()

print("reading messaging file...")
file = open(msg_file, 'r')
data = file.read()
file.close()
my_dict = xmltodict.parse(data, strip_whitespace=False)
my_dict_he = xmltodict.parse(data, strip_whitespace=False)
my_dict_fr = xmltodict.parse(data, strip_whitespace=False)
for dict_idx in range(len(my_dict['xliff']['file']['unit'])):
    dict_line = my_dict['xliff']['file']['unit'][dict_idx]
    source = dict_line['segment']['source']
    source_stripped = source.strip(" \n")
    row = cur.execute('select the_text_he, the_text_fr from  trans_en where the_text = ?', (source_stripped,)).fetchone()
    the_text_he = row[0]
    the_text_fr = row[1]
    my_dict_he['xliff']['file']['unit'][dict_idx]['segment']['target'] = source.replace(source_stripped, the_text_he)
    my_dict_fr['xliff']['file']['unit'][dict_idx]['segment']['target'] = source.replace(source_stripped, the_text_fr)

print("done parsing words")
cur.close()
con.close()

he = xmltodict.unparse(my_dict_he, pretty=True)
fr = xmltodict.unparse(my_dict_fr, pretty=True)

with open('messages.he.xlf', 'w') as f:
    f.write(he)

with open('messages.fr.xlf', 'w') as f:
    f.write(fr)

print("done creating translation files")
