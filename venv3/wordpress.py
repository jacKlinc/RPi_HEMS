if type(network.nodes[node].values[val].units) is not str:
    print("No str")

if type(network.nodes[node].get_sensor_value(val)) is not float:
    print("No float")

if type(node) is not int:
    print("No int")

                #     network.nodes[node].values[val].id_on_network,  # nw_id
            #network.nodes[node].get_switch_state(val),      # dev_state
        #     12,                                             # interval
                #     network.nodes[node].values[val].label,          # label

        # units = []
        # units.append(network.nodes[node].values[val].units)
        # print(units)
        # print("------------------------------------------------------------")

        # value = []
        # value.append(network.nodes[node].get_sensor_value(val))
        # print(value)
        # print("------------------------------------------------------------")

        # nodes = []
        # nodes.append(node)
        # print(nodes)