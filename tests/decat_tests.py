from os.path import dirname
from os.path import join
from os.path import realpath
from json import loads
import unittest
from decat.models.decat import Decat


class DecatLoadTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		good_tests_path = join(realpath(dirname(__file__)), 'good_tests.json')
		bad_tests_path = join(realpath(dirname(__file__)), 'bad_tests.json')

		with open(good_tests_path, 'r') as f:
			cls.good_tokens = loads(f.read())

		with open(bad_tests_path, 'r') as f:
			cls.bad_tokens = loads(f.read())

		cls.decat = Decat(debug=True)

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_success(self):
		"""
			test with acceptable values
			decat should be able to load all these values
		"""
		decat = self.decat
		for token in self.good_tokens:
			with self.subTest(text=token):
				decat.load_text(token)
				self.assertTrue(decat.is_loaded, f'bad text: {token}')

	def test_failure(self):
		"""
			test with unacceptable values
			none of these value should go through
		"""
		decat = self.decat
		err_msg = 'Only alpha characters are allowed'
		for token in self.bad_tokens:
			with self.subTest(token=token):
				if decat.debug:
					with self.assertRaises(Exception) as context:
						decat.load_text(token)
					self.assertTrue(err_msg in context.exception.args[0])
				else:
					decat.load_text(token)
					self.assertFalse(decat.is_loaded, f'bad token loaded: {token}')

	def test_character_map(self):
		"""
			testing with acceptable values
			data type of character map should be dict
			keys must be all unique characters from text
		"""
		for token in self.good_tokens:
			with self.subTest(token=token):
				self.decat.load_text(token)
				character_map = self.decat.character_map
				self.assertTrue(type(character_map), dict)
				self.assertEqual(set(token), set(character_map.keys()))


class DecatExtractorTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		input_path = join(realpath(dirname(__file__)), 'extractor_input.json')

		with open(input_path, 'r') as f:
			cls.input = loads(f.read())

		cls.decat = Decat(debug=True)

	def test_extractor(self):
		decat = self.decat
		for token in self.input:
			expected = self.input[token]
			with self.subTest(token=token):
				decat.load_text(token)
				results = decat.extractor(token)
				# print(f'T: {token} | R: {results}')
				self.assertEqual(expected, results)
			# break


if __name__ == '__main__':
	unittest.main(verbosity=2)
