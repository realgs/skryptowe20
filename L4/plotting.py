#!/usr/bin/python3

import matplotlib.pyplot as pyplot

def plot_dictionary(data, description):
    pyplot.plot(list(data.keys()), list(data.values()))
    pyplot.title(description['title'])
    pyplot.xlabel(description['x_label'])
    pyplot.ylabel(description['y_label'])
    pyplot.legend(description['data_labels'])
    pyplot.show()

def plot_iterable(data, description):
    for x in data:
        pyplot.plot(list(x.keys()), list(x.values()))

    pyplot.title(description['title'])
    pyplot.xlabel(description['x_label'])
    pyplot.ylabel(description['y_label'])
    pyplot.legend(description['data_labels'])
    pyplot.show()
