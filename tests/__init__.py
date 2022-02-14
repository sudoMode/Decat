from decat import decat
import json

from unittest import TestCase
from unittest import main

EXTRACTOR_INPUT = 'extractor_input.json'
PASSAGE_INPUT = 'passage_input.json'


class DecatTester(TestCase):

    @classmethod
    def setUpClass(cls):
        with open(EXTRACTOR_INPUT, 'r') as f:
            cls.extractor_input = json.loads(f.read())

        with open(PASSAGE_INPUT, 'r') as f:
            cls.passage_input = json.loads(f.read())

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_decat(self):
        for key, value in self.extractor_input.items():
            out = decat(key)
            self.assertEqual(out, value)

    def test_passage_decat(self):
        for passage in self.passage_input:
            out = decat(passage['input'])
            self.assertEqual(out, passage['output'])

    def test_presevervation_of_special_characters(self):
        input_ = {
                    'stringwithoutspace,andwithacomma':
                    ['string', 'without', 'space,', 'and', 'with', 'a', 'comma']
        }
        for key, value in input_.items():
            out = decat(key, preserve_special_characters=True)
            self.assertEqual(out, value)


if __name__ == '__main__':
    main()
