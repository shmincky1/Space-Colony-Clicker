
class SerializableMeta(type):
	registry={}
	def __new__(cls, name, parents, dct):
		res=super().__new__(cls, name, parents, dct)
		cls.registry[name]=res
		return res

class Serializable(object, metaclass=SerializableMeta):
	def save(self): return {}
	def load(self, data): pass

	@classmethod
	def create_empty(cls):
		return cls.__new__(cls)

	@staticmethod
	def save_object(obj):
		if type(obj) == dict:
			return {k:Serializable.save_object(v) for k,v in obj}
		if type(obj) in [list, set]:
			return [Serializable.save_object(i) for i in obj]
		if isinstance(obj, Serializable):
			return obj.save()
		return obj

	@staticmethod
	def load_object(data):
		if type(data) == dict:
			if "__type" not in data:
				print(data.items())
				return {k:Serializable.load_object(v) for k,v in data.items()}

			obj=SerializableMeta.registry[data["__type"]].create_empty()
			del data["__type"]
			obj.load(Serializable.load_object(data))

			return obj
		if type(data) == list:
			return [Serializable.load_object(i) for i in data.items()]
		return data

class EnumeratedFieldSerializable(Serializable):
	_saved_fields=[]
	def save(self):
		ret = {k:Serializable.save_object(getattr(self, k)) for k in self._saved_fields}
		ret["__type"]=type(self).__name__
		return ret
	def load(self, data):
		[setattr(self, k, Serializable.load_object(v)) for k,v in data.items()]
