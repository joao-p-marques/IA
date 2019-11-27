
from constraintsearch import *

def friends_constraint(friend1, tuple1, friend2, tuple2):
    u1, b1 = tuple1
    u2, b2 = tuple2

    # same object cant be shared by 2 friends
    if u1 == u2 or b1 == b1:
        return False

    # Umbrella and bike must belong to different friends
    if u1 == b1 or u2 == b2:
        return False

    # The one who takes Claudio's hat rides Bernardo's bike
    if u1 == 'Claudio' and b1 != 'Bernardo':
        return False

    return True


def make_constraint_graph(friends):
    # each 2 neighbour countries don't share the same color
    return { (X,Y):friends_constraint for X in friends for Y in friends if X!=Y }

def make_domains(friends):
    return { friend:[(u, b)] for u in friends
                             for b in friends
                             for friend in friends
                             if u!=b and friend!=u and friend!=b
            }

# map to store country neighbours
friends = [
        'André',
        'Bernardo',
        'Cláudio',
        ]

color_list = ['red', 'blue', 'green', 'yellow', 'white']

cs = ConstraintSearch(make_domains(friends), make_constraint_graph(friends))

print(cs.search())

