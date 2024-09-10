from dataclasses import dataclass

from md2pdf.decode import lz77

class Huffman:
        '''
            Huffman encoding implementation.

            Params:
                - data: data to encode.

            Internal params:
                - data: original data to encode.
                - freq_list: list that contains all uniques characters in data and its frequency ordered by the frequency.
                - trad_map: map that contains all uniques characters in data and its assigned code.
        '''
        def __init__(self, data: str | list[lz77.LZ77.Pair | str], freq_list: list = [], trad_map: dict = {}, order_criteria: any = lambda x: x.freq):
            self.freq_list = freq_list
            self.data = data
            self.trad_map = trad_map
            self.order_criteria = order_criteria

        class ListItem:
            '''
                Items that stores freq_list

                Params:
                    - item: value to store
                    - freq: frequency of the item
            '''
            def __init__(self, item, freq):
                self.item = item
                self.freq = freq

            def __str__(self) -> str:
                return f'[{self.item}: {self.freq}]'
            
            def __repr__(self) -> str:
                return f'[{self.item}: {self.freq}]'

        class Node:
            '''
                Internal Huffman node.

                Params:
                    - label: label to identify the node
                    - freq: frequency of the node
                    - left: left child of the node. Can be str or other Node
                    - right: right child of the node. Can be str or other Node
            '''
            def __init__(self, label: str, freq: int, left=None, right=None):
                self.label = label
                self.freq = freq
                self.left = left
                self.right = right

            def __str__(self) -> str:
                return f'{self.label}: {self.left} - {self.right}'
            
            def __repr__(self) -> str:
                return f'{self.label}: {self.left} - {self.right}'
            
            def is_leaf(self) -> bool:
                return self.left is None and self.right is None
            
        @dataclass
        class HuffData:
            code: str
            code_length: int

        def load_freq_map(self) -> None:
            '''
                Creates a sorted list of frequencies for the original data.
            '''
            m = {}
            for c in self.data:
                if c not in m:
                    m[c] = 1
                else:
                    m[c] = m[c] + 1

            self.freq_list = [self.ListItem(x[0], x[1]) for x in m.items()]
            # Sort the items list by frequency in ascending order
            self.freq_list = sorted(self.freq_list, key=self.order_criteria)
                
        def build_tree(self) -> None:
            '''
                Creates the Huffman tree from the frequencies map.
                The result is the frequencies map containing only one entry, the root node, and its frequency.

                TODO: optimize data structures (Node, ListItem).
            '''
            while len(self.freq_list) > 1:
                # List of items is sorted by frequency in ascending order, so we take the first 2 elements
                a = self.freq_list.pop(0)
                b = self.freq_list.pop(0)

                a_label = ""
                b_label = ""
                af = a.freq
                bf = b.freq

                if type(a.item) == self.Node:
                    a_label = a.item.label
                elif type(a.item) == str:
                    a_label = a.item
                    a = self.Node(a_label, af)

                if type(b.item) == self.Node:
                    b_label = b.item.label
                elif type(b.item) == str:
                    b_label = b.item
                    b = self.Node(b_label, bf)

                newNode = self.Node(a_label+b_label, af+bf, a, b)
                newItem = self.ListItem(newNode, newNode.freq)
                # insert new item in list
                
                self.freq_list.append(newItem)
                # Sort again the list by frequency in ascending order
                self.freq_list = sorted(self.freq_list, key=self.order_criteria)

        def create_codes(self, node: Node, val: str, huff: str, d: dict[HuffData]) -> None:
            '''
                Process all the nodes of the tree and generates its codes

                Params:
                    - node: Node to process.
                    - val: code generated previously.
                    - huff: new bit to add to the code. If the new node to process is left, val = 0. Else, val = 1.
                    - d: map to store the codes and its character.
            '''
            newVal = val + huff
            if(node.left):
                if type(node.left) == self.ListItem:
                    self.create_codes(node.left.item, newVal, '0', d)
                elif type(node.left) == self.Node:
                    self.create_codes(node.left, newVal, '0', d)
            if(node.right):
                if type(node.right) == self.ListItem:
                    self.create_codes(node.right.item, newVal, '1', d)
                elif type(node.right) == self.Node:
                    self.create_codes(node.right, newVal, '1', d)

            if(not node.left and not node.right):
                d[node.label] = Huffman.HuffData(newVal, len(newVal))
        
        def code(self) -> str:
            '''
                Build Huffman tree, initialize the trad_map and invokes create_codes.

                Returns encoding of the original data.
            '''
            self.load_freq_map()
            self.build_tree()
            root = self.freq_list[0]
            self.trad_map = {}
            self.create_codes(root.item, '', '', self.trad_map)
            res = ''
            for c in self.data:
                res = res + self.trad_map[c].code
            return res
        
        def decode(self, data: str) -> str:
            '''
                Decodes the input data traveling it and the Huffman tree.

                Input:
                    - data: Huffman encoded data
            '''
            res = ''
            act_node = self.freq_list[0].item # Initial actual node is root node
            for c in data:
                if c == '0':
                    branch = act_node.left
                    if type(branch) == self.ListItem:
                        act_node = act_node.left.item
                    else:
                        act_node = act_node.left
                else:
                    branch = act_node.right
                    if type(branch) == self.ListItem:
                        act_node = act_node.right.item
                    else:
                        act_node = act_node.right

                if type(act_node) == self.Node and act_node.is_leaf():
                    res = res + act_node.label
                    act_node = self.freq_list[0].item
            return res