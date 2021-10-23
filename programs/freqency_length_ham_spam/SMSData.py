import csv
import re
import tkinter

import pylab

import pandas as pd
import numpy as np

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

if __name__ == '__main__':

    # extracting ham and spam words to different files with frequencies
    # from the file with all sms messages

    porter = PorterStemmer()
    with open('sms-spam-corpus.csv', 'r', encoding='ISO-8859-1') as read_file:
        csv_reader = csv.reader(read_file)
        spec_chars = "[^a-zA-Z ]"
        stop_words = set(stopwords.words('english'))

        str_arrays = []
        ham_array = {}
        spam_array = {}
        for line in csv_reader:
            if line[0] == 'ham':
                for word in re.sub(spec_chars, '', line[1]).lower().split(" "):
                    if word != '':
                        if word not in stop_words:
                            ham_array[porter.stem(word)] = ham_array.setdefault(porter.stem(word), 0) + 1
            else:
                for word in re.sub(spec_chars, '', line[1]).lower().split(" "):
                    if word != '':
                        if word not in stop_words:
                            spam_array[porter.stem(word)] = spam_array.setdefault(porter.stem(word), 0) + 1

        ham_array = dict(sorted(ham_array.items(), key=lambda item: len(item[0])))
        spam_array = dict(sorted(spam_array.items(), key=lambda item: len(item[0])))
        str_arrays.append(ham_array)
        str_arrays.append(spam_array)

        with open('sms-all-words.csv', 'w', newline='') as dictionary:
            writer = csv.writer(dictionary)
            writer.writerow(['type', 'word', 'length'])

            for key in str_arrays[0].keys():
                writer.writerow(['ham', key, len(key)])

            for key in str_arrays[1].keys():
                writer.writerow(['spam', key, len(key)])

        with open('sms-ham-dictionary.csv', 'w', newline='') as dictionary:
            writer = csv.writer(dictionary)
            writer.writerow(['word', 'frequency'])

            for key, value in ham_array.items():
                writer.writerow([key, value])

        with open('sms-spam-dictionary.csv', 'w', newline='') as dictionary:
            writer = csv.writer(dictionary)
            writer.writerow(['word', 'frequency'])

            for key, value in spam_array.items():
                writer.writerow([key, value])

    # Calculating total average length of all words
    # Creating plot with normalized words lengths and average length

    average_length = 0
    words_amount = sum(1 for line in open('sms-all-words.csv'))
    hams_lengths = {}
    spams_lengths = {}

    with open('sms-all-words.csv', 'r') as all_words:
        reader = csv.reader(all_words)
        total_sum_length = 0
        for line in reader:
            total_sum_length += len(line[1])
            if line[0] == 'ham':
                hams_lengths[len(line[1])] = hams_lengths.setdefault(len(line[1]), 0) + 1
            elif line[0] == 'spam':
                spams_lengths[len(line[1])] = spams_lengths.setdefault(len(line[1]), 0) + 1
        average_length = total_sum_length / words_amount

    for key in hams_lengths.keys():
        hams_lengths[key] /= words_amount
    for key in spams_lengths.keys():
        spams_lengths[key] /= words_amount

    pylab.subplot(2, 2, 1)
    pylab.bar(range(len(hams_lengths)), width=0.2, height=hams_lengths.values())
    pylab.bar(range(len(spams_lengths)), width=0.2, height=spams_lengths.values())
    pylab.bar(average_length, width=0.2, height=max(hams_lengths.values()), color='red')
    pylab.title('Words lengths')
    pylab.ylabel('Number of words with length')
    pylab.legend(['ham', 'spam', 'average'])

    # Getting ham and spam messages
    # and creating arrays of normalized messages lengths
    # and calculating average length of all messages

    average_messages_length = 0
    messages_amount = sum(1 for line in open('sms-spam-corpus.csv', encoding='ISO-8859-1'))
    ham_messages_lengths = {}
    spam_messages_lengths = {}

    with open('sms-spam-corpus.csv', 'r', encoding='ISO-8859-1') as all_messages:
        reader = csv.reader(all_messages)
        total_sum_length = 0
        for line in reader:
            total_sum_length += len(line[1])
            if line[0] == 'ham':
                ham_messages_lengths[len(line[1])] = ham_messages_lengths.setdefault(len(line[1]), 0) + 1
            elif line[0] == 'spam':
                spam_messages_lengths[len(line[1])] = spam_messages_lengths.setdefault(len(line[1]), 0) + 1
        average_messages_length = total_sum_length / messages_amount

    for key in ham_messages_lengths.keys():
        ham_messages_lengths[key] /= messages_amount
    for key in spam_messages_lengths.keys():
        spam_messages_lengths[key] /= messages_amount

    pylab.subplot(2, 2, 2)
    pylab.bar(range(len(ham_messages_lengths)), width=1, height=ham_messages_lengths.values())
    pylab.bar(range(len(spam_messages_lengths)), width=1, height=spam_messages_lengths.values())
    pylab.bar(average_messages_length, width=1, height=max(ham_messages_lengths.values()), color='red')
    pylab.title('Messages lengths')
    pylab.ylabel('Number of messages with length')
    pylab.legend(['ham', 'spam', 'average'])

    ham_dictionary = pd.read_csv('sms-ham-dictionary.csv', header=None, index_col=0, squeeze=True).to_dict()
    ham_dictionary = sorted(ham_dictionary.items(), key=lambda item: int(item[1]), reverse=True)
    most_frequent_ham_words = list(ham_dictionary)[:20]
    most_frequent_ham_words_dict = {x[0]: int(x[1]) / len(ham_dictionary) for x in most_frequent_ham_words}
    most_frequent_ham_words_dict = dict(sorted(most_frequent_ham_words_dict.items(), key=lambda item: item[1]))

    pylab.subplot(2, 2, 3)
    pylab.bar(range(len(most_frequent_ham_words_dict)), height=most_frequent_ham_words_dict.values())
    pylab.xticks(np.arange(len(most_frequent_ham_words_dict)), most_frequent_ham_words_dict.keys(), rotation='vertical')
    pylab.title('Ham frequencies')
    pylab.ylabel("frequency")

    spam_dictionary = pd.read_csv('sms-spam-dictionary.csv', header=None, index_col=0, squeeze=True).to_dict()
    spam_dictionary = sorted(spam_dictionary.items(), key=lambda item: int(item[1]), reverse=True)
    most_frequent_spam_words = list(spam_dictionary)[:20]
    most_frequent_ham_words = sorted(most_frequent_ham_words_dict, )
    most_frequent_spam_words_dict = {x[0]: int(x[1]) / len(spam_dictionary) for x in most_frequent_spam_words}
    most_frequent_spam_words_dict = dict(sorted(most_frequent_spam_words_dict.items(), key=lambda item: item[1]))

    pylab.subplot(2, 2, 4)
    pylab.bar(range(len(most_frequent_spam_words_dict)), height=most_frequent_spam_words_dict.values(), color='orange')
    pylab.xticks(np.arange(len(most_frequent_spam_words_dict)), most_frequent_spam_words_dict.keys(), rotation='vertical')
    pylab.title('Spam frequencies')
    pylab.ylabel("frequency")

    pylab.show()