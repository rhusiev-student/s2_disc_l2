from tqdm import tqdm
import matplotlib.pyplot as plt
import time
class Node:
    """class for a node"""
    def __init__(self, symbol, prob, left=None, right=None) -> None:
        """
        store info about a node:
        symbol, probability, left and right children, code
        """
        self.symbol = symbol
        self.prob = prob
        self.code = ''
        self.left = left
        self.right = right

def assign_code(Node, parent_code='', dct = {}) -> dict:
    """
    assign new code to a node
    """
    new_code = parent_code + str(Node.code)
    if Node.left:
        assign_code(Node.left, new_code)
    if Node.right:
        assign_code(Node.right, new_code)
    if (not Node.left and not Node.right):
        Node.code = new_code
        dct[Node.symbol] = Node.code
    return dct


def find_probabilities(message) -> None:
    """find frequency of symbols"""
    dct = {}
    print('message=', message)
    for i in message:
        try:
            dct[i] += 1
        except KeyError:
            dct[i] = 1
    for key, value in dct.items():
        dct[key] = value / len(message)
    print('probabilities=', dct)
    return dct

class Huffman:
    def __init__(self, file_name: str) -> None:
        """
        stores some variables for huffman algo to use
        """
        self.file_name = file_name
        self.message = ''
        self.dct_prob = None
        self.dct_codes = {}
        self.encoded_message = ''
        self.tree = None

    def get_message(self) -> None:
        """
        read file and assign message into inint
        """
        with open(self.file_name, mode='r') as file:
            message = file.readlines()
            message = ''.join(i for i in message)
            self.message = message

    def encode(self) -> str:
        """encode using huffman method"""
        # find probabilities for each symbol
        self.dct_prob = find_probabilities(self.message)
        nodes = []
        # turn all symbols into a node object
        # add them to a nodes list
        for key, value in self.dct_prob.items():
            nodes.append(Node(key, value))

        # continue untill only one node remains
        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.prob)
        # pick two nodes with the lowest probability
            right = nodes[0]
            left = nodes[1]
        # assign code (0 if bigger probability, else - 1)
            right.code = '1'
            left.code = '0'
        # make a combined node
            nodes.append(Node(symbol=right.symbol+left.symbol, prob=right.prob+left.prob, left=left, right=right))
        # remove unneeded nodes
            nodes.remove(right)
            nodes.remove(left)
        # assign each node a code, working from the parent node
        self.dct_codes = assign_code(nodes[0])
        print('codes=', self.dct_codes)
        # encode a message using nodes codes
        encoded_message = ''
        for i in self.message:
            encoded_message += self.dct_codes[i]
        print('encoded message=', encoded_message)
        self.encoded_message = encoded_message
        self.tree = nodes[0]


    def decode(self) -> str:
        """decode a message using huffman tree created by nodes"""
        res = ''
        tree = self.tree
        child_tree = self.tree
        for i in self.encoded_message:
            if i == '0':
                child_tree = child_tree.left
            if i == '1':
                child_tree = child_tree.right
            try:
                if child_tree.left.symbol is None and child_tree.right.symbol is None:
                    pass
            except AttributeError:
                res += child_tree.symbol
                child_tree = tree
        print('decoded message == message:', res == self.message)
        return res

def compare_size(message, dct_codes):
    inicial= len(message)*8
    final = 0
    dct = {}
    for i in message:
        try:
            dct[i] += 1
        except KeyError:
            dct[i] = 1
    for key, value in dct.items():
        final += value*len(dct_codes[key])

    res = 100 - (final/inicial * 100)
    print('inicial size=', inicial)
    print('final size=', final)
    print('compression_effectivness', res, '%')
    return res

def find_time(file_name):
    """find the time of algorithm"""
    NUM_OF_ITERATIONS = 5
    time_taken = 0
    for i in tqdm(range(NUM_OF_ITERATIONS)):
        huf = Huffman(file_name)
        start = time.time()
        huf.get_message()
        huf.encode()
        huf.decode()
        end = time.time()
        time_taken += end - start
    return time_taken / NUM_OF_ITERATIONS


def graph_plotting():
    """"""
    # x-coordinates of left sides of bars
    names = ['small_input', 'big_input']
    # heights of bars
    func1 = find_time('to_encode.txt')
    func2 = find_time('ChornaRada.txt')
    height = [func1, func2]
    plt.bar(names, height, color ='maroon', width = 0.4)
    plt.xlabel('Input volume')
    plt.ylabel('Time')
    plt.title('Bar chart')
    plt.show()

if __name__ == '__main__':
    huf = Huffman('to_encode.txt')
    huf.get_message()
    huf.encode()
    huf.decode()
    compare_size(huf.message, huf.dct_codes)
