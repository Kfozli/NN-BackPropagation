from itertools import product
from random import random
from matplotlib.pylab import plot
from supporting_functions import calculate_distance

NUMBER_OF_PLOT_DIMENSIONS = 2
MAXIMUM_NUMBER_OF_ITERATIONS = 5000


class Neuron(object):
    def __init__(self):
        self._neuron_location_parameters = []
        self._neighbours = []
        self._initialize_neuron_location()

    def _initialize_neuron_location(self):
        for _ in range(NUMBER_OF_PLOT_DIMENSIONS):
            self._neuron_location_parameters.append(random() * 0.05 + 0.4)  # temporary values choice!

    def set_neuron_neighbours(self, neighbours):
        self._neighbours = neighbours

    def get_neuron_neighbours(self):
        return self._neighbours

    def draw_neuron(self):
        plot(self._neuron_location_parameters[0], self._neuron_location_parameters[1], "ro", color="blue")

    def calculate_distance_from_data_point(self, data_point):
        neuron_location = self.get_neuron_location()
        return calculate_distance(data_point, neuron_location)

    def update_neuron_location(self, data_point, learning_rate):
        for parameter_index in range(len(self._neuron_location_parameters)):
            diffrence_from_data_point = data_point[parameter_index] - self._neuron_location_parameters[parameter_index]
            self._neuron_location_parameters[parameter_index] += learning_rate * diffrence_from_data_point

    def get_neuron_location(self):
        return self._neuron_location_parameters


class KohonenNetwork(object):
    def __init__(self, network_dimensions, learning_rate):
        self._network_dimensions = network_dimensions
        self._learning_rate = learning_rate
        self._number_of_neurons = self._calculate_number_of_network_neurons()
        self._network_neurons = {}
        self._initialize_network_neurons()
        for (neuron_indexes, neuron) in self._network_neurons.items():
            neighbours = self._find_neuron_neighbours(neuron_indexes)
            neuron.set_neuron_neighbours(neighbours)

    def _find_neuron_neighbours(self, neuron_indexes):
        neighbours_collection = []
        number_of_indexes = len(neuron_indexes)
        for increased_index_place in range(number_of_indexes):
            searched_indexes = list(neuron_indexes[:])
            searched_indexes[increased_index_place] += 1
            search_result = self._network_neurons.get(tuple(searched_indexes), None)
            if search_result is not None:
                neighbours_collection.append(search_result)
        return neighbours_collection

    def _initialize_network_neurons(self):
        neurons_indexes_by_network_dimensions = []
        for network_dimension in self._network_dimensions:
            neurons_indexes_by_network_dimensions.append(range(network_dimension))
        for neurons_indexes in product(*neurons_indexes_by_network_dimensions):
            self._network_neurons.update({neurons_indexes: Neuron()})

    def _calculate_number_of_network_neurons(self):
        number_of_neurons = 1
        for network_dimension in self._network_dimensions:
            number_of_neurons *= network_dimension
        return number_of_neurons

    def _draw_neurons(self):
        for neuron in self._network_neurons.values():
            neuron.draw_neuron()

    def _draw_neurons_connections(self):
        for neuron in self._network_neurons.values():
            for neuron_neighbour in neuron.get_neuron_neighbours():
                neuron_location = neuron.get_neuron_location()
                neuron_neighbour_location = neuron_neighbour.get_neuron_location()
                plot([neuron_location[0], neuron_neighbour_location[0]],
                     [neuron_location[1], neuron_neighbour_location[1]],
                     color="green")

    def draw_network(self):
        self._draw_neurons()
        self._draw_neurons_connections()

    def _get_neuron_with_smallest_distance_from_data_point(self, data_point):
        neurons = self._network_neurons.values()
        minimum_distance_neuron = neurons[0]
        minimal_distance = neurons[0].calculate_distance_from_data_point(data_point)
        for neuron in neurons[1:]:
            neuron_distance_from_data_point = neuron.calculate_distance_from_data_point(data_point)
            if neuron_distance_from_data_point < minimal_distance:
                minimal_distance = neuron_distance_from_data_point
                minimum_distance_neuron = neuron
        return minimum_distance_neuron

    def train_network(self, database):
        data_points = database.get_data_points()
        for number_of_iteration in range(MAXIMUM_NUMBER_OF_ITERATIONS):
            if number_of_iteration % 100 == 0:
                print "Iteration number: ", number_of_iteration
            for data_point in data_points:
                minimum_distance_neuron = self._get_neuron_with_smallest_distance_from_data_point(data_point)
                minimum_distance_neuron.update_neuron_location(data_point, self._learning_rate)
                for neighbour_neuron in minimum_distance_neuron.get_neuron_neighbours():
                    neighbour_neuron.update_neuron_location(data_point, self._learning_rate)
