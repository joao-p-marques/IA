
# returns the size of a list recursively
def size(lst):
    if lst == []:
        return 0
    return size(lst[1:]) + 1

# returns the sum of the elements in a list recursively
def lst_sum(lst):
    if lst == []:
        return 0
    return lst_sum(lst[1:]) + lst[0]

# returns if element occurs in list
def occurs(lst, e):
    if lst == []:
        return False
    if lst[0] == e:
        return True
    return occurs(lst[1:], e)

# returns the concatenation of 2 lists
def lst_concat(l1, l2):
    if l1 == []:
        return l2
    if l2 == []:
        return l1

    l1.append(l2[0])
    return lst_concat(l1, l2[1:])

def inverse(lst):
    if lst == []:
        return []
    return inverse(lst[1:]) + [lst[0]]

l = [1, 2, 3, 4, 5]
print(size(l)) # 5
print(lst_sum(l)) # 15
print(occurs(l, 2)) # True
print(occurs(l, 6)) # False
ll = [6, 7]
print(lst_concat(l, ll)) # [1, 2, 3, 4, 5, 6, 7]
print(inverse(l))


