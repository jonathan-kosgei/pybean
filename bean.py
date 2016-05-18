class Bean(dict):
	def __init__(self, type):
		self.__dict__['type'] = type
		
	def __setitem__(self, key, item):
		self.__dict__[key] = item
		
	def __getitem__(self, key):
		return self.__dict__[key]
		
	def __repr__(self):
		return repr(self.__dict__)
		
	def __len__(self):
		return len(self.__dict__)
		
	def __delitem__(self, key):
		del self.__dict__[key]
		
	def keys(self):
		return self.__dict__.keys()
		
	def values(self):
		return list(self.__dict__.values())
		
	def __cmp__(self):
		return cmp(self.__dict__, dict)
		
	def __contains__(self, item):
		return item in self.__dict__
		
	def add(self, key, value):
		self.__dict__[key] = value
		
	def __iter__(self):
		return iter(self.__dict__)
		
	def __call__(self):
		return self.__dict__
		
	def __unicode__(self):
		return unicode(repr(self.__dict__))
		
	def __missing__(self, key):
		return key