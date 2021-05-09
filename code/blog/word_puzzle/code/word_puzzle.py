from typing import Set
from collections import defaultdict
from re import split


def character_ngrams(word, n=2):
    return [word[i:i + n] for i in range(len(word) - n + 1)]


def repeated_ngram(ngrams: list) -> Set[str]:
    r = set()
    for i in range(len(ngrams)):
        j = i + 1
        for k in range(j, len(ngrams)):
            if ngrams[i] == ngrams[k] and ngrams[i] not in r:
                r.add(ngrams[i])
    return r


def solve(input_words, words, n=2, print_debug=False):
    rd = defaultdict(list)
    for word in words:
        ngrams = character_ngrams(word, n)
        # TODO check overlapping ngrams - do we need to eliminate those?
        repeated = repeated_ngram(ngrams)
        for gram in repeated:
            rd[gram].append(word)

    print_stats(rd, print_debug)

    i = 0
    for input_word in input_words:
        for gram in rd.keys():
            candidate = ""
            for part in input_word:
                if part == '_':
                    candidate = candidate + gram
                else:
                    candidate = candidate + part
            for gram_word in rd[gram]:
                if gram_word == candidate:
                    i = i + 1
                    i_w = ''.join(input_word)
                    print(f'{i} input word "{i_w}" gram "{gram}" word "{candidate}"')


def print_stats(rd, print_mapping=False):
    num_words = 0
    max_words = 0
    for gram in rd.keys():
        if print_mapping:
            print(f'{gram} words {rd[gram]}')
        num_words = num_words + len(rd[gram])
        if len(rd[gram]) > max_words:
            max_words = len(rd[gram])

    print(f'Total repeated ngrams {len(rd.keys())}  Words {num_words} Max words for ngram {max_words}')


def test():
    with open('input_words.txt') as f:
        input_words = [split('(_)', line.rstrip('\n')) for line in f]

    with open('words_alpha.txt') as f:
        words = set([line.rstrip('\n') for line in f])

    solve(input_words, words, 2, False)


if __name__ == '__main__':
    test()
