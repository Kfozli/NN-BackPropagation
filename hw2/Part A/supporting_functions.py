from pickle import dump, HIGHEST_PROTOCOL


def _gather_network_layer_weights(layer_neurons):
    weights_collection = []
    for neuron in layer_neurons:
        weights_collection.append(neuron.weights)
    return weights_collection


def _gather_network_weights(network, input_neurons):
    weights_collection = {}
    weights_collection.update({"input_neurons_weights": _gather_network_layer_weights(input_neurons)})
    weights_collection.update({"hidden_layer_weights": _gather_network_layer_weights(network.hidden_layer)})
    weights_collection.update({"output_layer_weights": _gather_network_layer_weights(network.output_layer)})
    return weights_collection


def training_neurons_network(network,
                             training_samples,
                             input_neurons,
                             network_learning_rate,
                             neurons_activation_func_name,
                             number_of_hidden_layer_neurons):
    epoch = 1
    stop_network_learning = False
    last_error_rate = 0
    while stop_network_learning is False:
        error_rate = 0
        for input in training_samples:
            expected_output_values = input[:]
            for input_neuron_index, input_field in zip(range(len(input_neurons)), input):
                input_neurons[input_neuron_index].value = input_field
            output_values = network.calculate_net_output(input_neurons)
            for output_value, expected_output_value in zip(output_values, expected_output_values):
                error_rate += (expected_output_value - output_value) ** 2
            network.calculate_neurons_error(expected_output_values)
            network.update_neurons_weights(input_neurons, network_learning_rate)
        is_first_learning_iteration = epoch == 1
        if is_first_learning_iteration is False:
            stop_network_learning = last_error_rate < error_rate
        last_error_rate = error_rate
        epoch += 1
        trained_network_weights_file_name = "hidden_size_" + str(number_of_hidden_layer_neurons)
        trained_network_weights_file_name += "_learning_rate_" + str(network_learning_rate)
        trained_network_weights_file_name += "_activation_func_" + neurons_activation_func_name + ".pickle"
        with open(trained_network_weights_file_name, 'wb') as results_file:
            dump(_gather_network_weights(network), results_file, protocol=HIGHEST_PROTOCOL)


def normailze_sample_data(data_row):
        normalized_data_row = []
        min_value = min(data_row)
        max_value = max(data_row)
        for field_index in range(len(data_row)):
            if min_value != max_value:
                data_row_values_max_difference = float(max_value - min_value)
                normalized_data_row.append((data_row[field_index] - min_value) / data_row_values_max_difference)
            else:
                data_norm = sqrt(sum(map(lambda x: x ** 2, data_row)))
                normalized_data_row.append(data_row[field_index] / data_norm)
        return normalized_data_row
