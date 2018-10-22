# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:26:04 2017
@author: Κωνσταντίνος

Title: Object-oriented Matrix Statics

"""
import math as m

class Structure(object):

    def __init__(self, Nodes=[], Elements=[]):
        self.__nodes = Nodes
        self.__elements = Elements
        self.__numnodes = len(Nodes)
        self.__numels = len(Elements)

    def __str__(self):
        return "Structure consists of " + str(self.__numnodes) + " nodes and " + str(self.__numels) + " elements."

    @property
    def nodes(self):
        return self.__nodes

    @property
    def elements(self):
        return self.__elements

    def add_node(self, node):
        self.__nodes.append(node)
        self.__numnodes += 1

    def add_element(self, element):
        self.__elements.append(element)
        self.__numels += 1


class Element(object):

    def __init__(self, start_node, end_node):
        self.__nodej = start_node
        self.__nodek = end_node
        dx1 = end_node.x1 - start_node.x1
        dx2 = end_node.x2 - start_node.x2
        self.__length = (dx1**2 + dx2**2)**0.5
        self.__theta = m.atan2(dx2, dx1)

    @property
    def node_j(self):
        return self.__nodej

    @property
    def node_k(self):
        return self.__nodek

    @property
    def L(self):
        return self.__length

    @property
    def theta(self):
        return self.__theta

class Node(object):

    def __init__(self, x1, x2, degrees_of_freedom):
        self.x1 = x1
        self.x2 = x2
        self.__freedom_deg = degrees_of_freedom

    @property
    def freedom_deg(self):
        return self.__freedom_deg

    @property
    def support(self):
        return self.__support

    @support.setter
    def support(self, support=None):
        self.__support = support


class Support(object):

    def __init__(self, supported_degrees=[False,False,False], angle=0):
        self.supported_deg = supported_degrees
        self.angle = angle


n1 = Node(0, 0, [1, 2, 3])
n2 = Node(2, 3, [4, 5, 6])
sup = Support([False,True,False])
n1.support = sup
print(n1.support.supported_deg)
nodes = [n1, n2]
e1 = Element(n1, n2)
elements = [e1]
S = Structure(nodes, elements)
print(S)