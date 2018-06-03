import random
import argparse


class Node:
    def __init__(self, net, name):
        self.name = name
        self.data_received = False
        self.network = net

    def get_nodes(self, x):
        return self.network.get_nodes(node_requested=self, count=x)

    def start_gossip(self, x):
        if not self.data_received:
            self.data_received = True
            nodes_to_infect = self.get_nodes(x)
            for node in nodes_to_infect:
                node.start_gossip(x)


class Network:
    def __init__(self, nodes_count, gossip_count, x=4, my_algorithm=False):
        self.nodes = [Node(net=self, name=_) for _ in range(nodes_count)]
        self.gossip_count = gossip_count
        self.my_algorithm = my_algorithm
        self.x = x

    def get_nodes(self, node_requested, count):
        other_nodes = [node for node in self.nodes if node != node_requested]
        if self.my_algorithm:
            other_nodes = [node for node in other_nodes if not node.data_received]
            if len(other_nodes) < count:
                return other_nodes

        random_nodes = random.sample(other_nodes, count)
        return random_nodes

    def get_random_node(self):
        return random.choice(self.nodes)

    def all_nodes_infected(self):
        return all([node.data_received for node in self.nodes])

    def start_algorithm(self):
        success = 0

        for repeat in range(self.gossip_count):
            random_node = self.get_random_node()
            random_node.start_gossip(self.x)
            if self.all_nodes_infected():
                success += 1

            for node in self.nodes:
                node.data_received = False

        print('Success count: {}'.format(success))
        print('Total count: {}'.format(self.gossip_count))
        print('Percentage: {}%'.format(success / self.gossip_count * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evo test project')
    parser.add_argument('-n', type=int)
    parser.add_argument('-i', type=int)
    parser.add_argument('--my-algorithm', default=False, dest='my_algorithm', action='store_true')
    args = parser.parse_args()
    network = Network(nodes_count=args.n, gossip_count=args.i, my_algorithm=args.my_algorithm)
    network.start_algorithm()
