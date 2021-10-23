import csv
import re
import tkinter
from tkinter import filedialog

import pandas as pd
from nltk import PorterStemmer
from nltk.corpus import stopwords

if __name__ == '__main__':

    # Bayes's approach

    # staff for processing words
    porter = PorterStemmer()
    spec_chars = "[^a-zA-Z ]"
    stop_words = set(stopwords.words('english'))

    # function for studying the program
    def start_study():
        filename = filedialog.askopenfilename()
        chosen_file.config(text='Chosen file: ' + filename)
        with open(filename, 'r', encoding='ISO-8859-1') as read_file:
            csv_reader = csv.reader(read_file)

            # extracting and processing ham and spam words
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

            # sorting ham and spam words by their lengths
            ham_array = dict(sorted(ham_array.items(), key=lambda item: item[1], reverse=True))
            spam_array = dict(sorted(spam_array.items(), key=lambda item: item[1], reverse=True))

            # writing extracted ham words into the file
            with open('sms-ham-dictionary.csv', 'w', newline='') as dictionary:
                writer = csv.writer(dictionary)
                writer.writerow(['word', 'frequency'])

                for key, value in ham_array.items():
                    writer.writerow([key, value])

            # writing extracted spam words into the file
            with open('sms-spam-dictionary.csv', 'w', newline='') as dictionary:
                writer = csv.writer(dictionary)
                writer.writerow(['word', 'frequency'])

                for key, value in spam_array.items():
                    writer.writerow([key, value])

    # function for defining the type of the message
    def process_words():
        result.config(text='')
        # reading hams and spams from the learnt files
        ham_dictionary = pd.read_csv('sms-ham-dictionary.csv', header=None, index_col=0, squeeze=True).to_dict()
        spam_dictionary = pd.read_csv('sms-spam-dictionary.csv', header=None, index_col=0, squeeze=True).to_dict()

        # getting words to process
        extracted_words = str(wordEntry.get())

        # processing words
        processed_words = []
        for word in re.sub(spec_chars, '', extracted_words).lower().split(" "):
            if word != '':
                if word not in stop_words:
                    processed_words.append(word)

        # initialization of necessary variables
        p_text_ham = 1
        p_text_spam = 1
        number_of_unknown_ham_words = 0
        number_of_unknown_spam_words = 0

        all_hams = 0
        all_spams = 0

        for frequency in ham_dictionary.values():
            all_hams += int(frequency)

        for frequency in spam_dictionary.values():
            all_spams += int(frequency)

        p_ham = all_hams / (all_spams + all_hams)
        p_spam = all_spams / (all_spams + all_hams)

        # calculating the number of the unknown ham and spam words
        for word in processed_words:
            if word not in ham_dictionary.keys():
                number_of_unknown_ham_words += 1
            if word not in spam_dictionary.keys():
                number_of_unknown_spam_words += 1

        # calculating the possibilities
        for word in processed_words:
            number_of_words_repeating = 0

            # CALCULATING THE POSSIBILITY OF THE HAM MESSAGE
            # calculating the number of word's repeating in the ham dictionary
            if word in ham_dictionary.keys():
                number_of_words_repeating = int(ham_dictionary[word])

            # calculating the possibility of the ham message
            p_text_ham *= (number_of_words_repeating + 1) / (len(ham_dictionary) + number_of_unknown_ham_words)

            # CALCULATING THE POSSIBILITY OF THE SPAM MESSAGE
            # calculating the number of word's repeating in the spam dictionary
            if word in spam_dictionary.keys():
                number_of_words_repeating = int(spam_dictionary[word])

            # calculating the possibility of the spam message
            p_text_spam *= (number_of_words_repeating + 1) / (len(spam_dictionary) + number_of_unknown_spam_words)

        p_text_ham *= p_ham
        p_text_spam *= p_spam

        #SHOW RESULT
        if p_text_ham > p_text_spam:
            result.config(text='HAM\n' + 'p(ham) = ' + str(p_text_ham) + '\np(spam) = ' + str(p_text_spam))
        else:
            result.config(text='SPAM\n' + 'p(ham) = ' + str(p_text_ham) + '\np(spam) = ' + str(p_text_spam))


    # INITIALIZATION
    # master
    master = tkinter.Tk()

    # labels
    tkinter.Label(master, text='Choose a study file').grid(row=0)
    tkinter.Label(master, text='Words').grid(row=1)
    tkinter.Label(master, text='Result').grid(row=2)
    chosen_file = tkinter.Label(master)
    result = tkinter.Label(master)

    # textboxes
    wordEntry = tkinter.Entry(master, width=100)

    # buttons
    button_for_file = tkinter.Button(master, text='Choose', command=start_study)
    button_for_words = tkinter.Button(master, text='OK', command=process_words)

    # ADJUSTING LOCATION
    # textboxes
    wordEntry.grid(column=1, row=1)

    # labels
    chosen_file.grid(column=1, row=0)
    result.grid(column=1, row=2)

    # buttons
    button_for_file.grid(column=2, row=0)
    button_for_words.grid(column=2, row=1)

    master.mainloop()
