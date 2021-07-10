from collections import defaultdict
from re import split


def character_ngrams(word, n=2):
    return [word[i:i + n] for i in range(len(word) - n + 1)]


def repeated_ngram(ngrams: list, num_reps=2):
    result = []
    for i in range(len(ngrams)):
        r = []
        j = i + 1
        for k in range(j, len(ngrams)):
            if ngrams[i] == ngrams[k] and len(r) < num_reps:
                if len(r) == 0:
                    r.append(ngrams[i])
                r.append(ngrams[k])
        if len(r) == num_reps:
            result.append(r)
    return result


def reverse_ngram(ngrams: list, num_reps=2):
    result = []
    for i in range(len(ngrams)):
        r = []
        j = i + 1
        for k in range(j, len(ngrams)):
            rev = ngrams[k][::-1]
            if ngrams[i] == rev and len(r) < num_reps:
                if len(r) == 0:
                    r.append(ngrams[i])
                r.append(ngrams[k])
        if len(r) == num_reps:
            result.append(r)
    return result


def initialize(words, func_filter_ngrams, gram_len=2, num_reps=2, print_debug=False) -> defaultdict:
    rd = defaultdict(list)
    for word in words:
        ngrams = character_ngrams(word, gram_len)
        filtered_ngrams = func_filter_ngrams(ngrams, num_reps)
        for ngram_list in filtered_ngrams:
            if len(ngram_list) > 0:
                rd[','.join(ngram_list)].append(word)

    print_stats(rd, print_debug)
    return rd


def solve(input_words, rd: defaultdict):
    i = 0
    for input_word in input_words:
        found = False
        for key in rd.keys():
            gram_list = split(',', key)
            candidate = ""
            j = 0
            for part in input_word:
                if part == '_':
                    candidate = candidate + gram_list[j]
                    j = j + 1
                else:
                    candidate = candidate + part

            for gram_word in rd[key]:
                if gram_word == candidate:
                    i = i + 1
                    i_w = ''.join(input_word)
                    print(f'{i} input word "{i_w}" gram_list "{gram_list}" word "{candidate}"')
                    found = True

        if not found:
            print(f'{i} input word NOT FOUND "{input_word}"')


def print_stats(rd, print_mapping=False):
    num_words = 0
    max_words = 0
    for gram in rd.keys():
        if print_mapping:
            print(f'{gram} words {len(rd[gram])} : {rd[gram][0:300]}')
        num_words = num_words + len(rd[gram])
        if len(rd[gram]) > max_words:
            max_words = len(rd[gram])

    print(f'Total repeated ngrams {len(rd.keys())}  Words {num_words} Max words for ngram {max_words}')


def test():
    input_words = []
    with open('input_words.txt') as f:
        # with open('input_words_10k_common.txt') as f:
        for line in f:
            parts = []
            for p in split('(_)', line.rstrip('\n')):
                if p != '':
                    parts.append(p)
            if len(parts) > 0:
                input_words.append(parts)

    with open('words_alpha.txt') as f:
        # with open('words_10k_common.txt') as f:
        words = set([line.rstrip('\n') for line in f])

    rd = initialize(words, repeated_ngram, 2, 2, True)
    # rd = initialize(words, reverse_ngram, 2, 2, True)
    solve(input_words, rd)


if __name__ == '__main__':
    test()
