class AutoAdder(type):

    def __new__(cls, name, bases, dct):
        def add_one(self):
            return self.value + 1

        dct["add_one"] = add_one

        return super().__new__(cls, name, bases, dct)


class MyClass(metaclass=AutoAdder):

    def __init__(self, value):
        self.value = value


my_instance = MyClass(10)

print(my_instance.add_one())


# Завдання 2
class AttributeValidator(type):
    required_attribute = ["name", "age"]

    def __new__(cls, name, bases, dct):
        for attr in cls.required_attribute:
            if attr not in dct:
                raise ValueError(f"Відсутній атрибут: {attr}")

        for attr in cls.required_attribute:
            if not callable(attr):
                raise TypeError(f"Атрибут {attr} не може бути методом")

        return super().__new__(cls, name, bases, dct)


class Person(metaclass=AttributeValidator):
    name = "Joee"
    age = 20


print(Person.name)
print(Person.age)


# Завдання 4
class AutoRegister(type):
    registry = {}

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)

        cls.registry[name] = new_class

        return new_class


class MyClass(metaclass=AutoRegister):
    pass


class BaseClass1(metaclass=AutoRegister):
    pass


class BaseClass2(metaclass=AutoRegister):
    pass


print(AutoRegister.registry)


# Завдання 3

class BaseClass1:
    def print(self):
        print("Hello!!!")


class BaseClass2:
    def print(self):
        print("Hellooo!!!")


class InheritanceController(type):
    forbidden_bases = (BaseClass2, BaseClass1)

    def __new__(cls, name, bases, dct):
        if len(bases) > 1:
            first_print_method = getattr(bases[0], "print", None)
            if first_print_method:
                print(f"Першим буде викликано метод `print` з класу `{bases[0].__name__}`")

        for base in bases:
            if base in cls.forbidden_bases:
                raise TypeError(f"Спадкування від {base.__name__} заборонено")

        return super().__new__(cls, name, bases, dct)


class MySubClass(BaseClass1, BaseClass2, metaclass=InheritanceController):
    value = 1


print(MySubClass.value)
