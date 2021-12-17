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