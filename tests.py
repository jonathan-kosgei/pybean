from pybean import *
import unittest


class beanTests(unittest.TestCase):
	def test_setup_method_returns_a_database_connection(self):
		pybean.setup()
		self.assertTrue(pybean.db)
		pybean.close()
		
	def test_close_method_closes_database_connection(self):
		pybean.setup()
		self.assertTrue(pybean.db)
		pybean.close()
		self.assertFalse(pybean.db)
		
	def test_dispense_method_creates_a_new_database_table(self):
		pybean.setup()
		exists = 0
		cursor = pybean.db.cursor()
		bean_type = 'book'	
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		book = pybean.dispense(bean_type)
		test = cursor.execute('''
		SELECT COUNT(*) FROM sqlite_master
		WHERE name = "{0}"
		'''.format(bean_type))		
		pybean.db.commit()
		fetch = test.fetchone()[0]
		if fetch == 1:
			exists = 1
		self.assertEqual(1, exists)
		pybean.close()
		
	def test_dispense_method_returns_bean_object(self):
		pybean.setup()
		bean_type = 'book'
		book = pybean.dispense(bean_type)
		self.assertIsInstance(book, Bean)
		pybean.close()
		
	def test_store_method_stores_data(self):
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type = 'book'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		bookone = pybean.dispense(bean_type)
		bookone.name = 'Eragon'
		bookone.author = 'Christopher Paolini'
		bean_id = pybean.store(bookone)
		#print(bean_id)
		cursor.execute('''
		SELECT * FROM {0} WHERE id = {1} LIMIT 1
		'''.format(bean_type, bean_id))
		book = cursor.fetchone()
		#Find a way to get column names and match them to the values from fetchone
		#print(book)
		columns = ['name', 'author']
		bean = {(col, book) for value in book for col in columns}
		#self.assertEqual(bean, bookone)
		pybean.close()
		
	def test_load_method_returns_data(self):
		"""Note an sqlite error is thrown when an invalid type is passed to dispense so write some error handling for this"""
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type = 'book'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		bookone = pybean.dispense(bean_type)
		bookone.name = 'Eldest'
		bookone.author = 'Christopher Paolini'
		bean_id = pybean.store(bookone)
		bean = pybean.load(bean_type, bean_id)
		#print(bean, bookone)
		self.assertEqual(bean, bookone)
		
	def test_dipenseAll_method_returns_multiple_beans(self):
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type1 = 'movies'
		bean_type2 = 'books'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type1))
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type2))
		beans = pybean.dispenseAll(bean_type1, bean_type2)
		for bean in beans:
			self.assertIsInstance(bean, Bean)
		pybean.close()
		
	def test_loadAll_method_loads_multiple_beans(self):
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type = 'book'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		book = pybean.dispense(bean_type)
		book.title = 'The Inheritance'
		id1 = pybean.store(book)
		page = pybean.dispense(bean_type)
		page.number = 145
		id2 = pybean.store(page)
		#print(id2, page)
		beans = pybean.loadAll(bean_type, id1, id2)
		#print(beans)
		self.assertTrue(beans[0].title and beans[1].number)
		pybean.close()
		
	def test_load_method_returns_instance_of_bean(self):
		pybean.setup()
		bean_type = 'book'
		cursor = pybean.db.cursor()
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		bookone = pybean.dispense(bean_type)
		bookone.name = 'Brisingr'
		bookone.author = 'Christopher Paolini'
		id = pybean.store(bookone)
		bean = pybean.load(bean_type, id)
		self.assertIsInstance(bookone, Bean)
		
	def test_trash_method_deletes_bean(self):
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type = 'book'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		bookone = pybean.dispense(bean_type)
		bookone.name = 'Eldest'
		bookone.author = 'Christopher Paolini'
		id = pybean.store(bookone)
		pybean.trash(bookone.type, id)
		#The pybean.load method should ideally raise an error if the id in the table type does not exist
		#bean = pybean.load(bean_type, id)
		bean = None
		#The below check should ideally check for an exception being raised
		self.assertFalse(bean)
		pybean.close()
		
	def test_trashAll_method_deletes_all_beans(self):
		'''Have a storeAll method that returns a tuple of ids? '''
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type1 = 'book'
		bean_type2 = 'book'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type1))
		beans = pybean.dispenseAll(bean_type1, bean_type2)
		beans[0].name = 'The Man from St.Petersburg'
		beans[1].name = 'Preface'
		id1 = pybean.store(beans[0])
		id2 = pybean.store(beans[1])
		pybean.trashAll('book', id1, id2)
		#trashall works, need to setup that error handling
		#beans1 = pybean.loadAll('book', id1, id2)
		#The above line should raise an error 
		#self.assert should check for an error being raised
		pybean.close()
		
	def test_wipe_method_deletes_table(self):
		pybean.setup()
		cursor = pybean.db.cursor()
		bean_type = 'book'
		cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		book = pybean.dispense(bean_type)
		book.title = 'Head Fist C#'
		id = pybean.store(book)
		pybean.wipe('book')
		#bean = pybean.load('book', id)
		#self.assert raises error
		pybean.close()
	
	def test_nuke_method_destroys_database(self):
		'''Need to add another test method for testing mysql databases'''
		pybean.setup()
		pybean.nuke()
		from glob import glob
		db = glob(pybean.db_location)
		self.assertFalse(db)		
		
if __name__ == '__main__':
	unittest.main()