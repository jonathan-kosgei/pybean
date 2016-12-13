### A port of the RedBeanPHP ORM to Python.

**_To Create a new database table_**
```
pybean.setup()
book = pybean.dispense(bean_type)
pybean.db.commit()
pybean.close()
```

**_To store data in a database table_**
```
pybean.setup()
bean_type = 'book'
bookone.name = 'Eragon'
bookone.author = 'Christopher Paolini'
bean_id = pybean.store(bookone)
pybean.db.commit()
```

**_To load data from a database table_**
```
pybean.setup()
bean_type = 'book'
bookone = pybean.dispense(bean_type)
bookone.name = 'Eldest'
bookone.author = 'Christopher Paolini'
bean_id = pybean.store(bookone)
bean = pybean.load(bean_type, bean_id)
#print(bean)
```

**_To enter multiple rows in a database table_**
```
pybean.setup()
bean_type1 = 'movies'
bean_type2 = 'books'
beans = pybean.dispenseAll(bean_type1, bean_type2)
pybean.db.commit()
```

**_To load multiple rows from a database table_**
```
pybean.setup()
bean_type = 'book'
book = pybean.dispense(bean_type)
book.title = 'The Inheritance'
id1 = pybean.store(book)
page = pybean.dispense(bean_type)
page.number = 145
id2 = pybean.store(page)
#print(id2, page)
beans = pybean.loadAll(bean_type, id1, id2)
#print(beans)
pybean.close()
```

**_To delete a row in a database table_**
```
pybean.setup()
bean_type = 'book'
bookone = pybean.dispense(bean_type)
bookone.name = 'Eldest'
bookone.author = 'Christopher Paolini'
id = pybean.store(bookone)
pybean.trash(bookone.type, id)
pybean.close()
```

**_To delete multiple rows in a database table_**
```
pybean.setup()
bean_type1 = 'book'
bean_type2 = 'book'
beans = pybean.dispenseAll(bean_type1, bean_type2)
beans[0].name = 'The Man from St.Petersburg'
beans[1].name = 'Preface'
id1 = pybean.store(beans[0])
id2 = pybean.store(beans[1])
pybean.trashAll('book', id1, id2)
pybean.close()
```

**_To delete a database table_**
```
pybean.setup()
cursor = pybean.db.cursor()
bean_type = 'book'
book = pybean.dispense(bean_type)
book.title = 'Head Fist C#'
id = pybean.store(book)
pybean.wipe('book')
pybean.close()
```

**_To delete an entire database_**
```
pybean.setup()
pybean.nuke()
```

**_Notes:_**

The codebase currently supports only sqlite, it'd be a minor change to the setup() function to support other sql databases but I haven't gotten around to doing it :-). If you find any bugs lets me know at jonathan@saharacluster.com