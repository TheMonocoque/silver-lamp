#!/usr/bin/env python3

# The recipe calls for:
dict_recipe = {
    "apples": 1,
    "beets": 2,
    "carrots": 3,
    # "bananas": 1,
}

# Store room has:
dict_inventory = {
    "apples": 5,
    "beets": 10,
    "carrots": 4,
    "bananas": 1
}

print("dict:", dict_recipe)
print("set:", set(dict_recipe)) # keys only
print("list:", list(set(dict_recipe))) # put keys into list

# Intersect of two dictionaries
# common_keys = list(set(dict_recipe).intersection(dict_inventory))
# common_keys = list(set(dict_inventory).intersection(dict_recipe))
common_keys = filter(lambda key: key in dict_recipe, dict_inventory)
for keyname in common_keys:
    # print("Key: {} has value {}".format(keyname, dict_inventory[keyname]))
    print("Operating on", keyname)
    dict_inventory[keyname] -= dict_recipe[keyname]
    if dict_inventory[keyname] < 0:
        raise RuntimeError("out of", keyname)
    elif dict_inventory[keyname] == 0:
        print("Ran out of", keyname)


print("Remaining:", dict_inventory)

# fibonnaci list comprehension
mylist = [ 0, 1]
n=20
[mylist.append(mylist[-2]+mylist[-1]) for n in range(n)]
print("Fibo:", mylist)

# list comprehension vs lambda
# https://www.digitalocean.com/community/tutorials/understanding-list-comprehensions-in-python-3
letters = list(map(lambda x: x, r'|human|'))
print("LAMBDA__:", letters)
print("ListComp:", [letter for letter in r'|human|'])

""" conditional """
number_list = [ x for x in range(20) if x % 2 == 0]
print(number_list)

""" with fish """
fish_tuple = ('blowfish', 'clownfish', 'catfish', 'octopus')
fish_list = [fish for fish in fish_tuple if fish != 'octopus']
print(fish_list)

"""
# Convert
my_list = []

for x in [20, 40, 60]:
    for y in [2, 4, 6]:
        my_list.append(x * y)

print(my_list)
"""
my_list = [x * y for x in [20, 40, 60] for y in [2, 4, 6]]
print("CONVERT:", my_list)