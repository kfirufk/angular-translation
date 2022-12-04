import sqlite3
from googletrans import Translator


translator = Translator()
db_file = "trans.db"
con = sqlite3.connect(db_file)
cur = con.cursor()
update_cur = con.cursor()
for row in cur.execute('select the_text, the_text_he, the_text_fr from trans_en where the_text_he is null or the_text_fr is null'):
    the_text = row[0]
    the_text_he = row[1]
    the_text_fr = row[2]
    print("working on translating '%s'..." % the_text)
    if the_text_fr is None:
        the_text_fr = translator.translate(the_text, dest='fr').text
    if the_text_he is None:
        the_text_he = translator.translate(the_text, dest='he').text
    print("inserting to db..")
    update_cur.execute("update trans_en set the_text_he=?, the_text_fr=? where the_text=?", (the_text_he, the_text_fr, the_text))
print("finished, closing up")
con.commit()
cur.close()
update_cur.close()
con.close()

