# angular-translation
a set of tools to have localization\translation migrations for angular

# why
well... I wanted a set of tools to be able to re-create the translation files 
and update them freely when adding or modifying words.

note that this is a basic version, i created it for my usage, to have the words in english and to translate
them to france and hebrew. to add/remove languages you will need to modify the code

so i'm trimming new lines and spaces from start and end of strings, add them to a sqlite3 
db in order to update the translations.

i created a script that will update untranslated fields using google translation, you should of course after
that verify the translations manually, you will need basic sqlite knowledge for that or use some kind of sqlite browser

# how

1. so first you need to create xliff2 format of the translation file for your project. 
   for example: `ng extract-i18n --format=xlf2 --output-path src/locale` and then copy the translation 
   file to the python project
2. run `load_trans_to_db.py`. if you run it on the first time, it will create the translation table `trans_en`
   and add rows for each `<source>` element. 
   * if you run it the 2nd time, it will create new elements with new words, and update the updated_at 
     field with current timestamp of words that i already there, that way with a bit of sqlite knowledge
     you can tell what words are not in your project anymore, and you can delete these lines if you want.
3. run `update_trans.py` that will use Google Translate api to update empty fields with their translated words
4. run `generate_trans_files.py` to generate translation files
5. copy the translated files back to your project and rebuild your angular project
   
   
# Future plans

well... I did this tool for my own comfort, I guess that the first thing I would do is to allow dynamic languages with
some kind of settings file, for now it translate the origin language to Hebrew and French. 