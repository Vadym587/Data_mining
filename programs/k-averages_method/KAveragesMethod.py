import csv
import math
import random
import tkinter
from tkinter import filedialog
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

if __name__ == '__main__':

    # function for choosing file
    def choose_file():
        global filename
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


    def get_average(clusters_count, coords_x, coords_y, points_count):
        averages_array = []

        start_point = np.random.choice(range(points_count), clusters_count, replace=False)
        centroid = coords_x[start_point]
        while True:
            prev_centroid = np.copy(centroid)
            for i in range(clusters_count):
                centroid[i] = np.mean(coords_x[coords_y == i], axis=0)
            for i in range(points_count):
                dist = np.sum((centroid - coords_x[i]) ** 2, axis=1)
                averages_array.append(min(dist))
                min_ind = np.argmin(dist)
                coords_y[i] = min_ind
            if np.array_equiv(centroid, prev_centroid):
                average = np.mean(averages_array)
                break
        averages_array.clear()
        return average


    # function for running method
    def run_method():
        colors = []
        array_of_lists_of_points = []
        array_of_lists_of_points_prev = []
        centroids = {}
        array_of_arrays_of_distances_from_points_to_centroids = []

        points_dictionary = pd.read_csv('points.csv', index_col=0, squeeze=True).to_dict()
        x_list = list(points_dictionary.keys())
        y_list = list(points_dictionary.values())

        for i in range(int(number_of_clusters.get())):
            index = random.randint(0, len(points_dictionary))
            centroids[x_list[index]] = y_list[index]
        print(centroids)

        for i in range(int(number_of_clusters.get())):
            colors.append([random.random(), random.random(), random.random()])

        centroids = {float(k): float(v) for k, v in centroids.items()}
        iteration = 0
        first_iteration = True
        equivalent_points = False

        while first_iteration or not equivalent_points:
            sums_x = []
            sums_y = []
            array_of_lists_of_points_to_work = []

            for index in range(len(centroids)):
                array_of_lists_of_points_to_work.append(
                    {list(centroids.keys())[index]: list(centroids.values())[index]})

            for index in range(len(centroids)):
                sums_x.append(list(centroids.keys())[index])
                sums_y.append(list(centroids.values())[index])

            try:
                for key, value in points_dictionary.items():
                    d = math.sqrt(math.pow(float(key) - list(centroids.keys())[0], 2) + math.pow(
                        float(value) - list(centroids.values())[0], 2))
                    index_of_cluster = 0
                    for index in range(1, len(centroids)):
                        d1 = math.hypot(float(key) - list(centroids.keys())[index],
                                        float(value) - list(centroids.values())[index])
                        if d1 < d:
                            d = d1
                            index_of_cluster = index
                    array_of_lists_of_points_to_work[index_of_cluster][key] = value
                    sums_x[index_of_cluster] += float(key)
                    sums_y[index_of_cluster] += float(value)
                print(iteration)
                iteration += 1

                for index_of_cluster in range(len(centroids)):
                    average_x = sums_x[index_of_cluster] / len(array_of_lists_of_points_to_work[index_of_cluster])
                    average_y = sums_y[index_of_cluster] / len(array_of_lists_of_points_to_work[index_of_cluster])
                    centroids[list(centroids.keys())[index_of_cluster]] = average_y
                    centroids[average_x] = centroids[list(centroids.keys())[index_of_cluster]]
                    del centroids[list(centroids.keys())[index_of_cluster]]

                if iteration > 100:
                    break
            except IndexError:
                print("try again")
                break

            if not first_iteration:
                array_of_lists_of_points_prev = array_of_lists_of_points.copy()
            array_of_lists_of_points = array_of_lists_of_points_to_work

            if not first_iteration:
                for index_of_list in range(len(array_of_lists_of_points_to_work)):
                    if sorted(array_of_lists_of_points_to_work[index_of_list]) == sorted(
                            array_of_lists_of_points_prev[index_of_list]):
                        equivalent_points = True
            else:
                first_iteration = False

        show_scatter(array_of_lists_of_points, colors)

        points_dictionary = pd.read_csv(filename, delimiter='\s+', header=None, names=["x", "y"]).iloc[:, [0, 1]].values
        y = np.zeros(len(points_dictionary))
        averages_squared = []
        avg = get_average(int(number_of_clusters.get()), points_dictionary, y, len(points_dictionary))
        averages_squared.append(avg)
        for i in range(1, int(number_of_clusters.get())):
            y = np.copy(y)
            avg = get_average(i, points_dictionary, y, len(points_dictionary))
            averages_squared.append(avg)
        averages_squared.sort(reverse=True)
        figure1 = Figure()
        plot = FigureCanvasTkAgg(figure1, master)
        plot.get_tk_widget().grid(column=1, row=2)
        ax = figure1.add_subplot(111)
        ax.plot(list(range(1, int(number_of_clusters.get()) + 1)), averages_squared)
        ax.scatter(list(range(1, int(number_of_clusters.get()) + 1)), averages_squared)


    # function to show scatter of points
    def show_scatter(array_of_lists_of_points, colors):
        figure1 = plt.Figure()
        scatter1 = FigureCanvasTkAgg(figure1, master)
        scatter1.get_tk_widget().grid(column=3, row=2)
        ax1 = figure1.add_subplot(111)
        for i in range(len(array_of_lists_of_points)):
            array_of_lists_of_points[i] = {float(k): float(v) for k, v in array_of_lists_of_points[i].items()}
            ax1.scatter(array_of_lists_of_points[i].keys(), array_of_lists_of_points[i].values(), color=colors[i])
        # ax1.scatter(centroids.keys(), centroids.values(), color='black')
        ax1.legend(['points'])


    # INITIALIZATION
    # master
    master = tkinter.Tk()

    # labels
    tkinter.Label(master, text='Choose a file').grid(row=0)
    tkinter.Label(master, text='Number of clusters').grid(row=1)
    tkinter.Label(master, text='Result').grid(row=2)
    chosen_file = tkinter.Label(master)

    # spinbox
    number_of_clusters = tkinter.StringVar(value=1)
    number_of_clusters_entry = ttk.Spinbox(master, from_=1, to=1000, textvariable=number_of_clusters, wrap=False)

    # buttons
    filename = ''
    button_for_file = tkinter.Button(master, text='Choose', command=choose_file)
    button_for_method = tkinter.Button(master, text='OK', command=run_method)

    # ADJUSTING LOCATION
    # spinbox
    number_of_clusters_entry.grid(column=1, row=1)

    # labels
    chosen_file.grid(column=1, row=0)

    # buttons
    button_for_file.grid(column=2, row=0)
    button_for_method.grid(column=2, row=1)

    master.mainloop()
