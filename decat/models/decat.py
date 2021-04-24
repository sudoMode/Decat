from decat.models.concatenated_string import ConcatenatedString
from decat.vocabulary import get_language_map
from decat.vocabulary import get_stop_words
from json import loads


class Decat:

	def __init__(self, text=None, language='english', min_length=2,
	             max_length=None, stopwords=[], debug=True, verbose=False):
		# TODO: change debug value
		# TODO: update load checker
		# self.__load_check(text, language, min_length, max_length, stopwords)
		self.text = text
		self.debug = debug
		self.verbose = verbose
		self.language = language
		self.min_length = min_length
		self.max_length = max_length
		self.stopwords = stopwords
		self.language_map = {}
		self.character_map = {}
		self.possible_words = []
		self.possible_words = []
		self.resolved_string = self.text
		self.is_resolved = False
		self.is_loaded = False
		self._err = ''
		self.__err_stack = []
		self.__load()

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

	def __load(self):
		try:
			if self.text is not None:
				self.concatenated_string = ConcatenatedString(self.text, debug=self.debug)
				if not self.concatenated_string.is_loaded:
					raise ValueError(f'Could not generate concatenated string for: {self.text}')
				if self.max_length is None:
					self.max_length = self.concatenated_string.length
				self.language_map = get_language_map(self.language)
				self.__load_character_map()
				self.__load_stopwords()
				self.is_loaded = True
		except Exception as e:
			self.__error_handler(e)

	def __load_character_map(self):
		"""
			map each unique character to all possible words
		"""
		_chars, _min, _max = self.concatenated_string.characters, self.min_length, self.max_length
		_load, _lang = self.__load_vocabulary, self.language_map
		_char_vocab = list(map(lambda x: list(filter(lambda y: _min <= len(y) <= _max, _load(_lang[x]))), _chars))
		self.character_map = dict(zip(_chars, _char_vocab))

	def __load_stopwords(self):
		stopwords = self.__load_vocabulary(get_stop_words(self.language))
		self.stopwords = list(set(stopwords).union(self.stopwords))

	def __update_stopwords(self, stopwords, alpha_check):
		assert type(stopwords) is list, f'Stopwords must be passed in a list, received: {type(stopwords)}'
		if alpha_check:
			bad_tokens = list(set(stopwords).difference(list(filter(lambda x: str(x).isalpha(), stopwords))))
			assert not (bool(bad_tokens)), f'Non-alpha characters not allowed, received: {bad_tokens}'
		self.stopwords = list(set(self.stopwords).union(stopwords))

	def __load_vocabulary(self, file_path):
		"""
			loads json file
			:param file_path: file to read
			:return: file's content in a python object
		"""
		vocabulary = []
		try:
			# load array of tokens
			with open(file_path, 'r') as f:
				vocabulary = loads(f.read())
		except Exception as e:
			e = f'failed to load file: {file_path} | Err Msg={e}'
			self.__error_handler(e)
		return vocabulary

	def __load_check(self, text, language, min_length, max_length, stopwords=[]):
		"""
			check for input validity
			:param text: string to load
			:param language: language of text
			:param min_length: minimum length of expected keywords
			:param max_length: maximum length of expected keywords
		"""
		try:
			text_length = len(text)
			assert type(text) is str, f'text should be a string value only, got {type(text)}'
			assert type(language) is str, f'language should be a string value only, got {type(text)}'
			assert type(min_length) is int and min_length > 0, 'min_length should be a positive integer.'
			assert type(max_length) is int and max_length > 0, 'max_length should be a positive integer.'
			assert min_length <= max_length, f'min_length [{min_length}] should be <= max_length [{max_length}]'
			assert max_length <= text_length, f'max_length [{max_length}] should be <= text_length [{text_length}]'
			assert type(stopwords) is list, f'stopwords must be passed in a list, received: {type(list)}'
		except Exception as e:
			_e = f'Load check failure | {e}'  # TODO: add msg to error handler
			self.__error_handler(e, _e)

	def __reset(self, text=None, language='english', min_length=2, max_length=None):
		"""
			reset provided attributes
			:param text: string to load
			:param language: language of text
			:param min_length: minimum length of expected keywords
			:param max_length: maximum length of expected keywords
		"""
		self.is_loaded = False
		self._err = ''
		if text is not None:
			self.text = text
		if language != self.language:
			self.language = language
		if min_length != self.min_length:
			self.min_length = min_length
		if max_length != self.max_length:
			self.max_length = max_length
		self.possible_words = []

	def __go_for_large_tokens(self, text, exclude_stopwords, j=0):
		"""
			'sillycat' -> ['silly', 'cat']

			prioritize large tokens first
			:param exclude_stopwords: True/False
		"""
		j += 1
		if not (bool(text)):
			return
		vocab = self.character_map.get(text[0], [])  # load vocabulary
		l1 = len(self.possible_words)  # total tokens extracted so fail
		total_chars = len(text)
		for i in range(total_chars):
			target_token = text[:total_chars - i]
			# print(f'i: {i} | j: {j} | T: {target_token}')
			if target_token in vocab:
				if not (exclude_stopwords and target_token in self.stopwords):
					self.possible_words.append(target_token)
					text = text[len(target_token):]
					self.__go_for_large_tokens(text, exclude_stopwords, j)
					break

		if l1 == len(self.possible_words):
			if len(text) > 1:
				self.__go_for_large_tokens(text[1:], exclude_stopwords, j)

	def __go_for_small_tokens(self, text, exclude_stopwords, j=0):
		"""
			prioritize small tokens first
			:param exclude_stopwords: True/False
		"""
		j += 1  # to count number of calls
		if not (bool(text)):
			return  # breaks recursion
		vocab = self.character_map.get(text[0], [])  # load vocabulary by character
		l1 = len(self.possible_words)  # total tokens extracted so far
		for i in range(len(text)):
			target_token = text[:i + 1]  # increment from left to right: 'c' -> 'ca' -> 'cat'
			print(f'i: {i} | J: {j} | T: {target_token}')
			if target_token in vocab:
				if not (exclude_stopwords and target_token in self.stopwords):
					self.possible_words.append(target_token)  # capture this token
					text = text[len(target_token):]  # update text
					self.__go_for_small_tokens(text, exclude_stopwords, j)  # recurse
					break

		if l1 == len(self.possible_words):  # no valid token was matched with the given character
			if len(text) > 1:  # at least 2 characters are still left
				self.__go_for_small_tokens(text[1:], exclude_stopwords, j)  # update text & recurse

	def __extract_possible_words(self, text, prioritize_large_tokens, exclude_stopwords):
		"""
			extract possible words from character map
			passwordprotectedfile
		"""
		if prioritize_large_tokens:
			self.__go_for_large_tokens(text, exclude_stopwords)
		else:
			self.__go_for_small_tokens(text, exclude_stopwords)

	def update_stopwords(self, stopwords, alpha_check=True):
		try:
			self.__update_stopwords(stopwords, alpha_check)
		except Exception as e:
			_err = f'Failed to update stopwords | {e}'
			self.__error_handler(_err)

	def load_text(self, text, language='english', min_length=2, max_length=None):
		"""
			reset existing attributes and load new ones
			:param text: string to load
			:param language: language, default is english
			:param min_length: minimum length of expected keywords1
			:param max_length: maximum length of expected keywords
		"""
		text_length = len(text)
		if max_length is None:
			max_length = text_length
		try:
			self.__load_check(text, language, min_length, max_length)
			self.__reset(text, language, min_length, max_length)
			self.__load()
		except Exception as e:
			_e = f'Load text failure | Err Msg={e}'
			self.__error_handler(e, _e)

	def extractor(self, text=None, prioritize_large_tokens=True, exclude_stopwords=True):
		"""
			TODO: __load_check
			:param text:
			:param prioritize_large_tokens:
			:param exclude_stopwords:
			:return:
		"""
		if text is None:
			text = self.text
		self.__extract_possible_words(text, prioritize_large_tokens, exclude_stopwords)
		return self.possible_words
