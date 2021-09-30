from json import loads
from math import log


class Decat:
    PUNTUATION_MARKS = [',', '.', '?', '!', '#', ':', ';', '-', '[', ']', '{', '}',
                        '(', ')', '`', '...', '"', "'"]

    def __init__(self, supported_languages, vocabulary_map, target_string='',
                 language='en', preserve_punctuation_marks=True):
        assert language in supported_languages.values(), f'Language "{language}" is not' \
                                                         f' supported yet, pick from: ' \
                                                         f'{supported_languages.keys()}'
        self.target_string = target_string
        self._target_string = ''
        self.language = language
        self.vocabulary_map = vocabulary_map
        self.preserve_punction_marks = preserve_punctuation_marks
        self.vocabulary = list()
        self.max_word = 0
        self.cost_map = dict()
        self.punctuation_map = dict()
        self.costs = [0]
        self.out = list()
        self._out = list()
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

    def _reset_costs(self):
        self.costs = [0]

    def _load_target_string(self, string):
        # remove punctuation marks, numbers and white spaces
        self._target_string = string
        for i in range(len(string)):
            char = string[i]
            if self.preserve_punction_marks:
                if char in Decat.PUNTUATION_MARKS:
                    self.punctuation_map[i] = char
                    continue
            self.target_string += char
        print('Processed: ', self.target_string)
        print('Raw: ', self._target_string)
        self._reset_costs()

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
        self._out = list(reversed(out))

    def _flush_out(self):
        _out = []
        print('PM: ', self.punctuation_map)
        counter = 0
        for out in self._out:
            inserted = 0
            _out = list(out)
            length = len(_out)
            for index, punctuation in self.punctuation_map.items():
                if index in range(counter, counter + length+1):
                    _out.insert(index - counter, punctuation)
                    length = len(_out)
            counter += length
            self.out.append(''.join(_out))
            print(f'O: {_out}')
        print('RR: ', self._out)
        print('RP: ', self.out)
        # self.out = self._out

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
    test_string = '{te,sting#string!is,cool'
    client.decat(target_string=test_string)
    # print(client.out)


if __name__ == '__main__':
    _test()
    """
        
    """
