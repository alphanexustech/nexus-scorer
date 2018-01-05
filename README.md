# nexus-scorer
Scores data. Starting with NLP.

# Gotchas
* Make sure to load the database with the corpora:
```
mongodump -d affect-corpus -o ./<dir name>
```
_linux EXPORT (DUMP)_
```
mongodump.exe -d affect-corpus -o ..\..\..\..\..\Users\<USER>\<dir_name>
```
_windows EXPORT (DUMP)_
```
mongorestore --db affect-corpus ./mongo_database_backup/affect-corpus/
```
_linux IMPORT (RESTORE)_
```
mongorestore.exe --db affect-corpus C:\<root_dir>\copious-affect-corpus\mongo_database_backup\affect-corpus
```
_windows IMPORT IMPORT (RESTORE)_

  <b>(Note on mongorestore from docs)</b>

  mongorestore can create a new database or add data to an existing database. However, mongorestore performs inserts only and does not perform updates. That is, if restoring documents to an existing database and collection and existing documents have the same value `_id` field as the to-be-restored documents, mongorestore will not overwrite those documents.

* Make sure to run the `nltk` commands in a python terminal as part of a build script, such as:
```
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('wordnet')
>>> nltk.download('averaged_perceptron_tagger')
```
