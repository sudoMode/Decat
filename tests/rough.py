"""

A naive algorithm won't give good results when applied to real-world data. Here is a 20-line algorithm that
exploits relative word frequency to give accurate results for real-word text.

(If you want an answer to your original question which does not use word frequency, you need to refine what
exactly is meant by "longest word": is it better to have a 20-letter word and ten 3-letter words, or is it
better to have five 10-letter words? Once you settle on a precise definition, you just have to change the
line defining wordcost to reflect the intended meaning.)

The idea
The best way to proceed is to model the distribution of the output.
A good first approximation is to assume all words are independently distributed.
Then you only need to know the relative frequency of all words.
It is reasonable to assume that they follow Zipf's law,
that is the word with rank n in the list of words has probability roughly 1/(n log N)
where N is the number of words in the dictionary.

Once you have fixed the model, you can use dynamic programming to infer the position of the spaces.
The most likely sentence is the one that maximizes the product of the probability of each individual word,
and it's easy to compute it with dynamic programming.
Instead of directly using the probability we use a cost defined as the logarithm of the
inverse of the probability to avoid overflows.

"""
from math import log
# from json import dumps


def get_word_cost(word_rank, total_words):
    """
        # TODO: explain Zipf's law
        :param word_rank:
        :param total_words:
        :return:
    """
    return log(word_rank*log(total_words))


def get_cost_map(words):
    word_costs = list(map(lambda x: get_word_cost(x[0]+1, len(words)), enumerate(words)))
    return dict(zip(words, word_costs))


# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
# read all the words in the dictionary
words = open("words-by-frequency.txt").read().split()[:35]

# find cost for each one
wordcost = get_cost_map(words)

# length of the longest word
maxword = max(map(len, words))
cost = [0]


# Find the best match for the i first characters, assuming cost has
# been built for the i-1 first characters.
# Returns a pair (match_cost, match_length)
def best_match(i, s):
    t = max(0, i - maxword)
    target_values = cost[t:i]
    reversed_values = reversed(target_values)
    candidates = enumerate(reversed_values)
    print(f'I: {i} | T: {t}')
    print(f'IC: {cost}')
    print(f'TV: {target_values}')
    print(f'RV: {list(reversed(target_values))}')
    print(f'CAN: {list(enumerate(reversed(target_values)))}')
    print('-------------')

    tc = []
    for k, c in enumerate(reversed(target_values)):
        print(f'K: {k} | C: {c}')
        ts = s[i-k-1:i]
        print(f'TS: {ts}')
        ec1 = wordcost.get(ts, 1e1000)
        ec2 = k + 1
        print(f'EC: {ec1}')
        tc.append((ec1, ec2))
    print(f'TC: {tc}')
    rv = min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k, c in candidates)
    print(f'RVR: {rv}')
    print('_________________________________________')

    return rv


def infer_spaces(s):
    """
        Uses dynamic programming to infer the location of spaces in a string
        without spaces.
    """

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length)
    # def best_match(i):
    #     candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
    #     return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    total_characters = len(s)
    # cost = [0]
    for i in range(total_characters):
        c, k = best_match(i+1, s)  # send character index starting from 1 and the whole string
        cost.append(c)
        print(f'C: {c} | K {k}')
        print(f'Cost: {cost}')
        print('============================================\n')

    print(f'C: {cost}')
    return 0

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))


# s = 'thumbgreenappleactiveassignmentweeklymetaphor'
# s = 'downloadmentionedfilefromthegivensource'
string = 'thepeople'
r = infer_spaces(string)
print(f'R: {r}')
