from json import loads
from math import log


class Decat:
    CHARACTERS_TO_PRESERVE = [',', '.', '?', '!', '#', ':', ';', '-', '[', ']', '{', '}',
                        '(', ')', '`', '...', '"', "'", '@', '0', '1', '2', '3', '4',
                        '5', '6', '7', '8', '9']

    def __init__(self, supported_languages, vocabulary_map, target_string='',
                 language='en', preserve_special_characters=False):
        assert language in supported_languages.values(), f'Language "{language}" is not' \
                                                         f' supported yet, pick from: ' \
                                                         f'{supported_languages.keys()}'
        self.target_string = target_string
        self._target_string = ''
        self.language = language
        self.vocabulary_map = vocabulary_map
        self.preserve_special_characters = preserve_special_characters
        self.vocabulary = list()
        self.max_word = 0
        self.cost_map = dict()
        self.preservable_character_map = dict()
        self.costs = [0]
        self.output = list()
        self._output = list()
        self._load()

    @staticmethod
    def _get_word_cost(rank, total, decimals=3):
        return round(log(rank * log(total)), decimals)

    def _load(self):
        self._load_vocabulary()
        self._load_cost_map()
        self.max_word = max(map(len, self.vocabulary))

    def _load_vocabulary(self):
        vocabulary = self.vocabulary_map[self.language]
        with open(vocabulary, 'r') as f:
            self.vocabulary = loads(f.read())

    def _load_cost_map(self):
        total = len(self.vocabulary)
        costs = list(map(lambda x: Decat._get_word_cost(x, total), range(1, total + 1)))
        self.cost_map = dict(zip(self.vocabulary, costs))

    def _reset_output(self):
        """
            Sets private & public output to an empty list
        """
        self._output = []
        self.output = []

    def _reset_costs(self):
        """
            Sets cost array to the inital value, a list with a single element i.e. 0
        """
        self.costs = [0]

    def _reset_target_string(self):
        """
            Sets private & public target strings to an empty string
        """
        self._target_string = ''
        self.target_string = ''

    def _reset_preservable_character_map(self):
        """
            Sets preservable character map to an empyt dictionary
        """
        self.preservable_character_map = {}

    def _load_target_string(self, string):
        """
            - Parses user input
            - Preserves user input in a private variable called _target_string
            - Parses alpha characters into a public variable called target_string
        """
        self._reset_target_string()
        self._reset_preservable_character_map()
        self._reset_output()
        self._reset_costs()
        # remove punctuation marks, numbers and white spaces
        string = string.replace(' ', '')
        self._target_string = string
        for i in range(len(string)):
            char = string[i]
            if self.preserve_special_characters:
                if char in Decat.CHARACTERS_TO_PRESERVE:
                    self.preservable_character_map[i] = char
                    continue
            if char.isalpha(): self.target_string += char.lower()

    def _get_minimum_cost_pair(self, i):
        return min(map(lambda x: (x[1] + self.cost_map.get(
            self.target_string[i - x[0] - 1: i], 1e1000), x[0] + 1),
                       enumerate(reversed(self.costs[max(0, i - self.max_word):i]))))

    def _compute_costs(self):
        for i in range(1, len(self.target_string) + 1):
            cost, length = self._get_minimum_cost_pair(i)
            self.costs.append(cost)

    def _backtrack(self):
        i = len(self.target_string)
        out = []
        while i > 0:
            cost, length = self._get_minimum_cost_pair(i)
            if cost == self.costs[i]:
                out.append(self.target_string[i - length:i])
                i -= length
        self._output = list(reversed(out))

    def _flush_out(self):
        _out = []
        counter = 0
        for out in self._output:
            inserted = 0
            _out = list(out)
            length = len(_out)
            for index, punctuation in self.preservable_character_map.items():
                if index in range(counter, counter + length+1):
                    _out.insert(index - counter, punctuation)
                    length = len(_out)
            counter += length
            self.output.append(''.join(_out))

    def _setup(self):
        pass

    def decat(self, target_string):
        self._load_target_string(string=target_string)
        self._compute_costs()
        self._backtrack()
        self._flush_out()


def _test():
    from decat import __settings__ as settings
    client = Decat(supported_languages=settings.SUPPORTED_LANGUAGES,
                   vocabulary_map=settings.VOCABULARY_MAP)
    client.preserve_special_characters = True
    test_string = "\"Just-try#with...someweirdpiecesoftext,okay?\""
    client.decat(target_string=test_string)
    print(client.output)


if __name__ == '__main__':
    _test()
