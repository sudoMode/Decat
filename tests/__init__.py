from decat import decat
import json

from unittest import TestCase
from unittest import main


INPUT_FILE = 'extractor_input.json'


class DecatTester(TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INPUT_FILE, 'r') as f:
            cls.input_data = json.loads(f.read())

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decat(self):
        for key, value in self.input_data.items():
            out = decat(key)
            print(f'I: {key} | J: {value} | O: {out}')
            self.assertEqual(decat(key), value)


if __name__ == '__main__':
    main()
