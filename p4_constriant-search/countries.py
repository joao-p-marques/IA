
from constraintsearch import *

def border_constraint(country1, color1, country2, color2):
    # if country2 in country_map[country1]:
    #     return False
    # return True
    return color1 != color2

def make_constraint_graph(countries):
    # each 2 neighbour countries don't share the same color
    return { (X,Y):border_constraint for X in countries.keys() for Y in countries[X] }

def make_domains(borders, color_list):
    return { country:color_list for country in borders.keys() }

# map to store country neighbours
country_map_a = {
        'A' : ['B', 'E', 'D'],
        'B' : ['A', 'E', 'C'],
        'C' : ['B', 'E', 'D'],
        'D' : ['A', 'E', 'C'],
        'E' : ['A', 'B', 'C', 'D']
        }

country_map_a = {
        'A' : ['B', 'E', 'D'],
        'B' : ['A', 'E', 'C'],
        'C' : ['B', 'E', 'D'],
        'D' : ['A', 'E', 'C'],
        'E' : ['A', 'B', 'C', 'D']
        }

color_list = ['red', 'blue', 'green', 'yellow', 'white']

cs = ConstraintSearch(make_domains(country_map_a, color_list), make_constraint_graph(country_map))

print(cs.search())

