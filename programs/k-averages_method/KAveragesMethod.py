import csv
import math
import random
import re
import tkinter
from tkinter import filedialog
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk import PorterStemmer
from nltk.corpus import stopwords

if __name__ == '__main__':

    # Bayes's approach

    # staff for processing words
    porter = PorterStemmer()
    spec_chars = "[^a-zA-Z ]"
    stop_words = set(stopwords.words('english'))

    # function for choosing file
    def choose_file():
        filename = filedialog.askopenfilename()
        chosen_file.config(text='Chosen file: ' + filename)
        with open(filename, 'r') as read_file:
            lines = read_file.readlines()

            points = {}
            for line in lines:
                coordinates_string = line.strip().split()
                points[coordinates_string[0].strip()] = coordinates_string[1].strip()

            with open('points.csv', 'w', newline='') as dictionary:
                writer = csv.writer(dictionary)
                writer.writerow(['x', 'y'])

                for key, value in points.items():
                    writer.writerow([key, value])

            points = pd.read_csv('points.csv')
            figure = plt.Figure()
            scatter = FigureCanvasTkAgg(figure, master)
            scatter.get_tk_widget().grid(column=3, row=2)
            ax = figure.add_subplot(111)
            ax.scatter(points.x, points.y, color='b')
            ax.legend(['points'])

    # function for defining the type of the message
    def run_method():
        result.config(text='')

        points_dictionary = pd.read_csv('points.csv', index_col=0, squeeze=True).to_dict()
        x_list = list(points_dictionary.keys())
        y_list = list(points_dictionary.values())

        centroids = {}
        for i in range(int(number_of_clusters.get())):
            index = random.randint(0, len(points_dictionary))
            centroids[x_list[index]] = y_list[index]

        colors = []
        for i in range(int(number_of_clusters.get())):
            colors.append([random.random(), random.random(), random.random()])

        figure1 = plt.Figure()
        scatter1 = FigureCanvasTkAgg(figure1, master)
        scatter1.get_tk_widget().grid(column=3, row=2)
        ax1 = figure1.add_subplot(111)

        array_of_lists_of_points = []
        for i in range(int(number_of_clusters.get())):
            array_of_lists_of_points.append({})

        centroids = {int(k): int(v) for k, v in centroids.items()}
        sums_x = []
        sums_y = []
        for i in range(int(number_of_clusters.get())):
            sums_x.append(0)
            sums_y.append(0)

        for key, value in points_dictionary.items():
            d = math.sqrt(math.pow((int(key) - list(centroids.keys())[0]), 2) + math.pow((int(value) - list(centroids.values())[0]), 2))
            index_of_cluster = 0
            for index in range(1, int(number_of_clusters.get())):
                d1 = math.sqrt(math.pow((int(key) - list(centroids.keys())[index]), 2) + math.pow((int(value) - list(centroids.values())[index]), 2))
                if d1 < d:
                    index_of_cluster = index
            array_of_lists_of_points[index_of_cluster][key] = value

            sums_x[index_of_cluster] += int(key)
            sums_y[index_of_cluster] += int(value)
            average_x = sums_x[index_of_cluster] / len(array_of_lists_of_points[index_of_cluster])
            average_y = sums_y[index_of_cluster] / len(array_of_lists_of_points[index_of_cluster])
            centroids[list(centroids.keys())[index_of_cluster]] = average_x
            centroids[average_y] = centroids[list(centroids.keys())[index_of_cluster]]
            del centroids[list(centroids.keys())[index_of_cluster]]

        for i in range(int(number_of_clusters.get())):
            array_of_lists_of_points[i] = {int(k): int(v) for k, v in array_of_lists_of_points[i].items()}
            ax1.scatter(array_of_lists_of_points[i].keys(), array_of_lists_of_points[i].values(), color=colors[i])

        ax1.scatter(centroids.keys(), centroids.values(), color='r')
        ax1.legend(['points'])


    # INITIALIZATION
    # master
    master = tkinter.Tk()

    # labels
    tkinter.Label(master, text='Choose a file').grid(row=0)
    tkinter.Label(master, text='Number of clusters').grid(row=1)
    tkinter.Label(master, text='Result').grid(row=2)
    chosen_file = tkinter.Label(master)
    result = tkinter.Label(master)

    # spinbox
    number_of_clusters = tkinter.StringVar(value=1)
    number_of_clusters_entry = ttk.Spinbox(master, from_=1, to=1000, textvariable=number_of_clusters, wrap=False)

    # buttons
    button_for_file = tkinter.Button(master, text='Choose', command=choose_file)
    button_for_words = tkinter.Button(master, text='OK', command=run_method)

    # ADJUSTING LOCATION
    # textboxes
    number_of_clusters_entry.grid(column=1, row=1)

    # labels
    chosen_file.grid(column=1, row=0)
    result.grid(column=1, row=2)

    # buttons
    button_for_file.grid(column=2, row=0)
    button_for_words.grid(column=2, row=1)

    master.mainloop()
