"""Python 3 port of the RedbeanPHP ORM"""
from bean import *
import sqlite3

class pybean():
	db = False
	db_location = 'stringbean.db'
	db_cursor = None
	
	@staticmethod 
	def setup():
		"""Opens an sqlite3 database connection at db_location"""
		db = sqlite3.connect(__class__.db_location)
		__class__.db = db
		__class__.db_cursor = __class__.db.cursor()
	
	@staticmethod
	def close():
		"""Closes the sqlite3 database connection at db_location"""
		__class__.db.close()
		__class__.db = False
		
	@staticmethod
	def dispense(bean_type):
		"""Creates a database table for every bean type dispensed"""
		__class__.db.execute('''
		CREATE TABLE IF NOT EXISTS {0} 
		(id INTEGER PRIMARY KEY
		)
		'''.format(bean_type))
		#The create statement works without the ,
		#{0} VARCHAR DEFAULT '{0}' part, this was creating a field on key 'book' and value 'book' instead of key 'type' and value 'book'
		__class__.db.commit()
		bean = Bean(bean_type)
		return bean
		
	@staticmethod
	def store(bean):
		__class__.db_cursor.execute('''
		SELECT * FROM {0} LIMIT 1
		'''.format(bean['type']))
		cols = [f[0] for f in __class__.db_cursor.description]
		new_cols = [col for col in bean.keys() if col not in cols]
		for col in new_cols:
			__class__.db_cursor.execute('''
			ALTER TABLE {0} ADD COLUMN {1}
			'''.format(bean['type'], col))
			__class__.db.commit()
		fields = bean.keys()
		values = bean.values()
		query = 'INSERT INTO {0} ({1}) values ({2})'.format(bean['type'], ",".join(fields), ",".join(['?']*len(fields)))
		__class__.db_cursor.execute(query, values)
		__class__.db.commit()
		bean['id'] = __class__.db_cursor.lastrowid
		return __class__.db_cursor.lastrowid
		
	@staticmethod
	def load(bean_type, bean_id):
		__class__.db_cursor.execute('''
		SELECT * FROM {0} WHERE id={1} LIMIT 1
		'''.format(bean_type, bean_id))
		cols = [f[0] for f in __class__.db_cursor.description]
		row = __class__.db_cursor.fetchone()
		bean_rep = dict(zip(cols, row))
		bean = Bean(bean_type)
		for k in bean_rep:
			bean[k] = bean_rep[k]
		return bean
		
	@staticmethod
	def dispenseAll(*args):
		beans = []
		for bean_type in args:
			bean = __class__.dispense(bean_type)
			beans.append(bean)
		return beans
		
	@staticmethod
	def loadAll(bean_type, *args):
		beans = []
		for id in args:
			bean = pybean.load(bean_type, id)
			beans.append(bean)
		return beans
		
	@staticmethod
	def trash(bean_type, bean_id):
		#You don't trash a bean that hasn't been pybean.stored so first check whether we can load the bean without getting an error
		__class__.db_cursor.execute('''
		DELETE FROM {0} WHERE id={1}
		'''.format(bean_type, bean_id))
		__class__.db.commit()
		
	@staticmethod
	def trashAll(bean_type, *args):
		for bean_id in args:
			pybean.trash(bean_type, bean_id)
			
	@staticmethod
	def wipe(bean_type):
		__class__.db_cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(bean_type))
		__class__.db.commit()
		
	def nuke():
		'''Add code to drop mysql database'''
		import os
		if os.path.isfile(__class__.db_location):
			os.remove(__class__.db_location)
		else:
			pass
			#raise error Cannot delete nonexistent database
		
			
		