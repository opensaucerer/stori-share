class Student:

    def __init__(self, first, last, age):
        self._first = first
        self._last = last
        self._age = age

    @property
    def firstname(self):
        return self._first

    @firstname.setter
    def firstname(self, name):
        self._first = name


stu = Student('Perfection', 'Loveday', 19)

print(stu.firstname)

stu.firstname = "Samperfect"

print(stu.firstname)
