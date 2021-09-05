from math import log
from json import loads
from decat.__settings__ import SUPPORTED_LANGUAGES
from decat.__settings__ import VOCABULARY_MAP


class Decat:

    def __init__(self, target_string=None, language='en'):
        assert language in SUPPORTED_LANGUAGES.values(), f'Language "{language}" is not' \
                                                         f' supported yet, pick from: ' \
                                                         f'{SUPPORTED_LANGUAGES.keys()}'
        self.target_string = target_string
        self.language = language
        self.vocabulary = list()
        self.max_word = 0
        self.cost_map = dict()
        self.costs = [0]
        self.out = []
        self._load()

    @staticmethod
    def _get_word_cost(rank, total, decimals=3):
        return round(log(rank * log(total)), decimals)

    def _load(self):
        self._load_vocabulary()
        self._load_cost_map()
        self.max_word = max(map(len, self.vocabulary))

    def _load_vocabulary(self):
        vocabulary = VOCABULARY_MAP[self.language]
        with open(vocabulary, 'r') as f:
            self.vocabulary = loads(f.read())

    def _load_cost_map(self):
        total = len(self.vocabulary)
        costs = list(map(lambda x: Decat._get_word_cost(x, total), range(1, total+1)))
        self.cost_map = dict(zip(self.vocabulary, costs))

    def _load_target_string(self, string):
        # remove punctuation marks, numbers and white spaces
        self.target_string = ''.join(e for e in string if e.isalpha())

    def _get_minimum_cost_pair(self, i):
        return min(map(lambda x: (x[1] + self.cost_map.get(
               self.target_string[i - x[0] - 1: i], 1e1000), x[0]+1),
               enumerate(reversed(self.costs[max(0, i - self.max_word):i]))))

    def _compute_costs(self):
        for i in range(1, len(self.target_string)+1):
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
        self.out = list(reversed(out))

    def decat(self, target_string):
        self._load_target_string(string=target_string)
        self._compute_costs()
        self._backtrack()


def _test():
    decat = Decat()
    string = 'thisisawesome'
    decat.decat(string)
    print(f'I: {string} | O: {decat.out}')


if __name__ == '__main__':
    _test()