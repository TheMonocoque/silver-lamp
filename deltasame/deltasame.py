#!/usr/bin/env python

import difflib

def print_differences(l1: list[str], l2: list[str]) -> None:
    l1sorted = list(l1)
    l2sorted = list(l2)
    l1sorted.sort()
    l2sorted.sort()
    diff = difflib.Differ()
    difference = diff.compare(l1sorted, l2sorted)
    print("Difference:")
    for line in difference:
        if line.startswith("+"):
            print(f"\tAdded: {line[2:]}")
        elif line.startswith("-"):
            print(f"\tRemoved: {line[2:]}")

def print_similarties(l1: list[str], l2: list[str]) -> None:
    same = set(l1) & set(l2)
    print("Identicals:")
    for identical in same:
        print(f"\t{identical}")

def main():
    print("Type in list of string to add to list:")
    list1: list[str] = input().split()
    # list1: list[str] = ["a", "b", "c"]
    list2: list[str] = ["x", "z", "b", "a"]
    print(f"{list1=}")
    print(f"{list2=}")
    print_differences(list1, list2)
    print_similarties(list1, list2)
    print(f"{list1=}")
    print(f"{list2=}")


if __name__ == "__main__":
    main()
