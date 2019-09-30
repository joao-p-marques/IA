
def separar(list_of_tuples):
    if list_of_tuples == []:
        return [], []
    a, b = list_of_tuples[0]
    la, lb = separar(list_of_tuples[1:])
    return [a] + la, [b] + lb

def remove_e_conta(l, e):
    if l == []:
        return [], 0

    l2, c = remove_e_conta(l[1:], e)
    if l[0] == e:
        return l2, c+1
    else:
        return [l[0]] + l2, c

def juntar(l1, l2):
    if len(l1) != len(l2):
        return None
    if l1 == [] or l2 == []:
        return []

    return [(l1[0], l2[0])] + juntar(l1[1:], l2[1:])

l = [(1, 1.1), (2, 2.2), (3, 3.3), (4, 4.4), (5, 5.5)]
print(separar(l))
print(remove_e_conta([1, 6, 2, 5, 5, 2, 5, 2] , 2))

# l1, l2 = separar(l)
# print(juntar(l1, l2))

print(juntar(*separar(l))) # '*' separates elements of tuple
