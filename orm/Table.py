# Exmaple for decorate class

# def add_method(cls):
#     cls.new_method = lambda self: "This is a new method"
#     return cls

# @add_method
# class MyClass:
#     def existing_method(self):
#         return "This is an existing method"

# # Usage
# obj = MyClass()
# print(obj.existing_method())  # Output: This is an existing method
# print(obj.new_method())       # Output: This is a new method

from dataclasses import dataclass


class Table:

    def __init__(self, *args, **kargs):
        self

    def __attrs__(self):
        print(self)


class User(Table):
    name: str
    age: int
    email: str


User(name="Ashish", age=23, email="ashish@stoira.com")
