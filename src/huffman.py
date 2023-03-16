class Node:
    def __init__(self, prob, symbol, left=None, right=None) -> None:
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = None

    def find_probabilities(self) -> None:
        # find frequency of letters
        dct = {}
        for i in self.message:
            try:
                dct[i] += 1
            except KeyError:
                dct[i] = 1
        for key, value in dct.items():
            dct[key] = value / len(self.message)
            print(key, ':', dct[key])
        keys = dct.keys()
        values = list(dct.values())
        print(values)
        self.keys = keys
        self.values = values
        self.dct = dct

    # def assign_code(self) -> None:
        # new_code = '' + 


class Huffman:
    def __init__(self, message) -> None:
        self.message = message
        self.keys = None
        self.values = None
        self.dct = None


    # def encode(self) -> str:

        

        # while len(self.dct) > 2:
        #     low1 = min(values)
        #     ind_low1 = values.index(low1)
        #     values.pop(ind_low1)
        #     low2 = min(values)
        #     ind_low2 = values.index(low2)
        #     values.pop(ind_low2)
        #     values.append(low1+low2)
        #     values = sorted(values)




        
        
        
    # def decode(self) -> str:
    #     pass


if __name__ == '__main__':
    huf = Huffman('acabacabab')
    huf.find_probabilities()
    huf.encode()
