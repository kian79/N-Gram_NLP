import re
from typing import Dict, List


def read_train(train_data):
    with open(train_data, 'r') as train_file:
        train = train_file.read()
        # print(train)
        train = train.split('\\')
        return train


def add_probability(dict: Dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1


def unigram(train):
    uni_dict = {'<s>': len(train), '</s>': len(train)}
    for line in train:
        line = line.split()
        for word in line:
            uni_key = word
            add_probability(uni_dict, uni_key)

    return uni_dict


def bigram(train):
    bi_dict = {}
    # print(train)
    for line in train:
        first = '<s>'
        line = line.split()
        line.append('</s>')
        for word in line:
            bi_key = (first, word)
            add_probability(bi_dict, bi_key)
            first = word

    return bi_dict


def trigram(train):
    tri_dict = {}
    for line in train:
        first = '<s>'
        line = line.split()
        line.append('</s>')
        for i in range(len(line)):
            if line[i] == '</s>':
                break
            tri_key = (first, line[i], line[i + 1])
            add_probability(tri_dict, tri_key)
            first = line[i]
    return tri_dict


# def count_

if __name__ == '__main__':
    my_train = read_train('Train_data.rtf')
    uni = unigram(my_train)
    bi = bigram(my_train)
    tri = trigram(my_train)
    with open('Test_data.rtf', 'r') as text:
        test_list = []
        for line1 in text:
            l = re.compile(r'[0-9]*,+[\\*\'*\"*[0-9]*]*(.*)')
            comp = l.findall(line1.lower())
            if comp:
                n = comp[0].rfind(".")
                compiled_line = comp[0][:n]
                test_list.append(compiled_line)
    answers = []
    for a_test in test_list:
        words: List = a_test.split()
        words.append('</s>')
        words.insert(0, '<s>')
        c_words = words.copy()
        # print(c_words)
        removed_index = words.index('$')
        max_prob = 0
        chosen_word = ""
        for word in uni.keys():
            c_words[removed_index] = word
            if word not in uni.keys():
                uni[word] = 0
            if (c_words[removed_index - 2], c_words[removed_index - 1]) not in bi.keys():
                bi[(c_words[removed_index - 2], c_words[removed_index - 1])] = 0
            if (c_words[removed_index - 1], word) not in bi.keys():
                bi[(c_words[removed_index - 1], word)] = 0
            if (c_words[removed_index - 2], c_words[removed_index - 1], word) not in tri.keys():
                tri[(c_words[removed_index - 2], c_words[removed_index - 1], word)] = 0
            b = 0
            if c_words[removed_index - 1] in uni.keys():
                b = 0 * bi[(c_words[removed_index - 1], word)] / \
                    uni[c_words[removed_index - 1]]

            probability = uni[word] * 0.8 / len(uni) + b
            if bi[(c_words[removed_index - 2], c_words[removed_index - 1])] :
                probability+= 0.2 * tri[c_words[removed_index - 2], c_words[removed_index - 1], word] / bi[
                    (c_words[removed_index - 2], c_words[removed_index - 1])]
            if probability > max_prob:
                max_prob = probability
                chosen_word = word
        answers.append(chosen_word)
    labs = []
    print(len(answers))
    with open('labels.rtf', 'r') as text:
        for line in text:
            l = re.compile(r'[0-9]*,+(.*)\\')
            lab = l.findall(line)
            # print(lab)
            if lab:
                lab = lab[0].strip()
                labs.append(lab)
    labs.append('professor')
    print(len(labs))
    for i in range(len(answers)):
        if answers[i] == labs[i ]:
            print(answers[i])