"""
A naive algorithm won't give good results when applied to real-world data.
Exploit relative word frequency to give accurate results for real-word text.

(Define what exactly is meant by "longest word": is it better to have a 20-letter word and ten 3-letter
words, or is itbetter to have five 10-letter words?
Once settled on a precise definition, change the line defining wordcost to reflect the intended meaning.)

The idea
The best way to proceed is to model the distribution of the output.
A good approximation is to assume all words are independently distributed.
Then we only need to know the relative frequency of all words.
We are assuming that they follow Zipf's law, that is the word with rank n
in the list of words has probability roughly 1/(n log N)
where N is the number of words in the dictionary.

Once the model is fixed, we can use dynamic programming to infer the position of the spaces.
The most likely sentence is the one that maximizes the product of the probability of each individual word,
and it's easy to compute it with dynamic programming.
Instead of directly using the probability we use a cost defined as the logarithm of the
inverse of the probability to avoid overflows.
"""

from math import log
# from math import inf  # infinity comparison
# from json import dumps


def get_word_cost(word_rank, total_words):
    """
        # TODO: explain Zipf's law
        :param word_rank:
        :param total_words:
        :return:
    """
    # print('called get word cost')
    return log(word_rank*log(total_words))


def get_cost_map(words):
    # print('called get cost map')
    word_costs = list(map(lambda x: get_word_cost(x[0]+1, len(words)), enumerate(words)))
    cost_map = dict(zip(words, word_costs))
    # print(f'CM: {cost_map}')
    return cost_map


# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability)
# read all the words in the dictionary
vocab = r'/Users/mandeepsingh/dev/projects/py/Decat/tests/words-by-frequency.txt'
words = open(vocab).read().split()

# find cost for each one
wordcost = get_cost_map(words)  # independent operation, can be stored as static content

# length of the longest word
maxword = max(map(len, words))

# cost array, to be populated character by character
costs_by_character = [0]


# Find the best match for the i first characters, assuming cost has
# been built for the i-1 first characters.
# Returns a pair (match_cost, match_length)
def get_minimum_cost_pair(index, string):
    # this variable is use to extract relevant values from cost array
    # these values never exceed the maxword in number
    start = max(0, index - maxword)

    # extract relevant values, always limited to maxword in number
    target_values = costs_by_character[start:index]

    # TODO: does this work while back tracking also?
    reversed_values = list(reversed(target_values))

    # generate pairs of indeces and cost value
    candidates = list(enumerate(reversed_values))

    cost_pairs = []
    for k, c in candidates:
        # overwrite start variable and use it to extract target string
        start = index - k - 1
        target_string = string[start:index]
        string_cost = c + wordcost.get(target_string, 1e1000)
        length = k + 1
        cost_pairs.append((string_cost, length))
    minimum_cost_pair = min(cost_pairs)
    return minimum_cost_pair


def decat(string):
    """
        Uses dynamic programming to infer the location of spaces in a string
        without spaces.
    """
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length)
    # Build the cost array.
    total_characters = len(string)
    for i in range(total_characters):
        c, k = get_minimum_cost_pair(i + 1, string)  # send character index starting from 1 and the whole
        costs_by_character.append(c)

    print(f'Cost Array: {costs_by_character}\n{"-"*100}')

    # backtrack to recover the minimal-cost string
    out = []
    i = total_characters
    while i > 0:
        c, k = get_minimum_cost_pair(i, string)
        if c == costs_by_character[i]:
            out.append(string[i-k:i])
            i -= k

    return " ".join(reversed(out))


if __name__ == '__main__':
    test_string = "userprofile"
    print(f'Input: {test_string} | Results: {decat(test_string)}')
    print(f'C: {costs_by_character}')
