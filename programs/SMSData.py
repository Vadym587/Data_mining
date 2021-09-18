import csv
import re
import pylab

import pandas as pd
from matplotlib import pyplot
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

        ham_array = dict(sorted(ham_array.items(), key=lambda item: len(item[0]), reverse=True))
        spam_array = dict(sorted(spam_array.items(), key=lambda item: len(item[0]), reverse=True))
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

    average_length = 0
    total_sum_length = 0
    words_amount = 0

    with open('sms-spam-dictionary.csv', 'r') as dictionary:
        reader = csv.reader(dictionary)
        for line in reader:
            if line[0] != 'word':
                total_sum_length += len(line[0]) * int(line[1].replace('\n', ''))
                words_amount += int(line[1].replace('\n', ''))

    with open('sms-ham-dictionary.csv', 'r') as dictionary:
        reader = csv.reader(dictionary)
        for line in reader:
            if line[0] != 'word':
                total_sum_length += len(line[0]) * int(line[1].replace('\n', ''))
                words_amount += int(line[1].replace('\n', ''))

    average_length = total_sum_length / words_amount

    # Creating plot with normalized words lengths and average length

    all_words = pd.read_csv('sms-all-words.csv')
    hams = all_words[all_words.type == 'ham']
    spams = all_words[all_words.type == 'spam']

    pylab.subplot(2, 2, 1)

    pylab.plot(range(len(hams)), hams.length / total_sum_length)
    pylab.plot(range(len(spams)), spams.length / total_sum_length)
    pylab.plot(range(len(hams)), hams.length * 0 + average_length / total_sum_length)
    pylab.title('Words lengths')
    pylab.ylabel("length")
    pylab.legend(['ham', 'spam', 'average'])

    # Getting ham and spam messages
    # and creating arrays of normalized messages lengths
    # and calculating average length of all messages

    all_messages = pd.read_csv('sms-spam-corpus.csv', encoding='ISO-8859-1')
    ham_messages = all_messages[all_messages.v1 == 'ham']
    spam_messages = all_messages[all_messages.v1 == 'spam']
    ham_messages_lengths = [len(m) for m in ham_messages.v2]
    spam_messages_lengths = [len(m) for m in spam_messages.v2]
    ham_messages_lengths = sorted(ham_messages_lengths, reverse=True)
    spam_messages_lengths = sorted(spam_messages_lengths, reverse=True)
    average_message_length = 0
    total_messages_length = 0
    number_of_messages = len(ham_messages) + len(spam_messages)

    for length in ham_messages_lengths:
        total_messages_length += length

    for length in spam_messages_lengths:
        total_messages_length += length

    for i, length in enumerate(ham_messages_lengths):
        ham_messages_lengths[i] = length / total_messages_length

    for i, length in enumerate(spam_messages_lengths):
        spam_messages_lengths[i] = length / total_messages_length

    average_message_length = total_messages_length / number_of_messages

    # Creating plot with normalized messages lengths and average length

    x = np.linspace(0, len(ham_messages), len(ham_messages))

    pylab.subplot(2, 2, 2)
    pylab.plot(range(len(ham_messages)), ham_messages_lengths)
    pylab.plot(range(len(spam_messages)), spam_messages_lengths)
    pylab.plot(x, x * 0 + average_message_length / total_messages_length)
    pylab.title('Messages lengths')
    pylab.ylabel("length")
    pylab.legend(['ham', 'spam', 'average'])

    ham_dictionary = pd.read_csv('sms-ham-dictionary.csv', header=None, index_col=0, squeeze=True).to_dict()
    ham_dictionary = sorted(ham_dictionary.items(), key=lambda item: int(item[1]), reverse=True)
    most_frequent_ham_words = list(ham_dictionary)[:20]
    most_frequent_ham_words_dict = {x[0]: x[1] for x in most_frequent_ham_words}
    most_frequent_ham_words_dict = dict(sorted(most_frequent_ham_words_dict.items(), key=lambda item: item[1]))

    pylab.subplot(2, 2, 3)
    pylab.bar(range(len(most_frequent_ham_words_dict)), height=most_frequent_ham_words_dict.values())
    pylab.xticks(np.arange(len(most_frequent_ham_words_dict)), most_frequent_ham_words_dict.keys(), rotation='vertical')
    pylab.title('Ham frequencies')
    pylab.ylabel("frequency")

    spam_dictionary = pd.read_csv('sms-spam-dictionary.csv', header=None, index_col=0, squeeze=True).to_dict()
    spam_dictionary = sorted(spam_dictionary.items(), key=lambda item: int(item[1]), reverse=True)
    most_frequent_spam_words = list(spam_dictionary)[:20]
    most_frequent_spam_words_dict = {x[0]: x[1] for x in most_frequent_spam_words}
    most_frequent_spam_words_dict = dict(sorted(most_frequent_spam_words_dict.items(), key=lambda item: item[1], reverse=True))

    pylab.subplot(2, 2, 4)
    pylab.bar(range(len(most_frequent_spam_words_dict)), height=most_frequent_spam_words_dict.values(), color='orange')
    pylab.xticks(np.arange(len(most_frequent_spam_words_dict)), most_frequent_spam_words_dict.keys(), rotation='vertical')
    pylab.title('Spam frequencies')
    pylab.ylabel("frequency")

    pylab.show()
    