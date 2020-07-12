 # TODO: add logger


class ConcatenatedString:

	def __init__(self, text=None, debug=False, verbose=False):
		self.text = text
		self.debug = debug
		self.verbose = verbose
		self.type = None
		self.length = None
		self.characters = None
		self.is_loaded = False
		self._err = ''
		self.__err_stack = []
		self.__load()

	def __repr__(self):
		return f'<decat.concatenated_string.ConcatenatedString object: "{self.text}">'

	def __error_handler(self, error, msg=None, debug=None):
		"""
			update error stack, raises error if debug is True
			:param error: python exception object
			:param debug: True/False
		"""
		if debug is None:
			debug = self.debug

		if msg is None:
			msg = str(error)

		self._err = msg
		self.__err_stack.append(self._err)

		if debug:
			raise error

	def __load(self, text=None):
		if text is not None:
			self.text = text
		try:
			self.__initial_check()
			self.type = type(self.text)
			self.length = len(self.text)
			self.characters = list(set(self.text))
			self.is_loaded = True
		except Exception as e:
			self.__error_handler(e)

	def __initial_check(self):
		self.__type_check()
		self.__character_check()

	def __type_check(self):
		if type(self.text) is not str:
			raise TypeError(f'Expected a string, got: {type(self.text)}')

	def __character_check(self):
		if not self.text.isalpha():
			raise ValueError(f'Only alpha characters are allowed, got: {self.text}')

	def get_error_message(self):
		return self._err
