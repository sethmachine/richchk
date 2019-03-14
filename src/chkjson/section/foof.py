"""

"""

from dataclasses import dataclass

@dataclass
class _ParentBase:
    name: str
    age: int

@dataclass
class _ParentDefaultsBase:
    ugly: bool = False

@dataclass
class _ChildBase(_ParentBase):
    school: str

@dataclass
class _ChildDefaultsBase(_ParentDefaultsBase):
    ugly: bool = True

# public classes, deriving from base-with, base-without field classes
# subclasses of public classes should put the public base class up front.

@dataclass
class Parent(_ParentDefaultsBase, _ParentBase):
    def print_name(self):
        print(self.name)

    def print_age(self):
        print(self.age)

    def print_id(self):
        print(f"The Name is {self.name} and {self.name} is {self.age} year old")

@dataclass
class Child(Parent, _ChildDefaultsBase, _ChildBase):
    pass

if __name__ == '__main__':
    pass
