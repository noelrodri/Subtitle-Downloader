
class Sumper:
    # def __add__(self, other):
    #     print("sumper ", other)
    pass


class Number(Sumper):
    def __init__(self, start):  # On Number(start)
        self.data = start

    def __sub__(self, other):  # On instance - other
        return Number(self.data - other)

    def __or__(self, other):
        print("hey hey ", other.data)

    def __call__(self):
        print("function call")

    def __getattr__(self, attr):
        print("getattr", attr)

    # def __getattribute__(self, attribute):
    #     print("get attribute")

    def __setattr__(self, attr, value=None):
        print(f'object = {self}, attr = {attr}, value = {value}')
        # self.__dict__[attr] = value

        object.__setattr__(self, attr, value)

    def __getitem__(self, index):
        print(index)
        # return self.data[index]

    def __setitem__(self, index, value):
        print(index, value)


class Employee:
    def __init__(self, name, pay=0):
        self.name = name
        self.pay = pay

    def giveRaise(self, percent):
        self.pay = self.pay + (self.pay * percent)

    def work(self):
        print(self.name, "does stuff")

    def __repr__(self):
        return "<Employee: name=%s, salary=%s>" % (self.name, self.pay)


class Chef(Employee):
    def __init__(self, name):
        Employee.__init__(self, name, 50000)

    def work(self):
        print(self.name, "makes food")


class Server(Employee):
    def __init__(self, name):
        Employee.__init__(self, name, 40000)

    def work(self):
        print(self.name, "interfaces food")


class PizzaRobot(Chef):
    def __init__(self, name):
        Chef.__init__(self, name)

    def work(self):
        print(self.name, "makes food")


class Customer:
    def __init__(self, name):
        self.name = name

    def order(self, server):
        print(self.name, "orders from", server)

    def pay(self, server):
        print(self.name, "pays for item to", server)


class Oven:
    def bake(self):
        print("oven bakes")


class PizzaShop:
    def __init__(self):
        self.server = Server('Pat')  # Embed other objects
        self.chef = PizzaRobot('Bob')  # A robot named bob
        self.oven = Oven()

    def order(self, name):
        customer = Customer(name)  # Activate other objects
        customer.order(self.server)  # Customer orders from server
        self.chef.work()
        self.oven.bake()
        customer.pay(self.server)


# scene = PizzaShop()  # Make the composite
# scene.order('Homer')  # Simulate Homer's order
# print('...')
# scene.order('Shaggy')


class Sum:
    def __init__(self, val):  # Callable instances
        self.val = val

    def __call__(self, arg):
        return self.val + arg


class Product:
    def __init__(self, val):  # Bound methods
        self.val = val

    def method(self, arg):
        return self.val * arg


class Negate:
    def __init__(self, val):  # Classes are callables too
        self.val = -val  # But called for object, not work

    def __repr__(self):  # Instance print format
        return str(self.val)


class ListInstance:

    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__):
            result += f'\t{attr}={self.__dict__[attr]}\n'
        return result

    def __str__(self):
        return f'<Instance of {self.__class__.__name__}, address {id(self)}:\n{self.__attrnames()}>'


class C1(ListInstance):
    def __init__(self):
        self.x = 2
        self.y = 3

    def unbound():
        print("jhfbjhwebfjhweb")

    def meth1(self, x):
        print("qwdjkhbqwj", x)

    def meth2(self): print(self.__X)

    def __method(self):
        print("hellow")

    def yellow(self):
        print(self)
        print("yellow")


class MyList(list):
    def __getitem__(self, offset):

        return list.__getitem__(self, offset - 1)

    def __repr__(self):
        return list.__repr__(self) + "hi"


class Set(list):
    def __init__(self, value=[]):  # Constructor
        list.__init__([])  # Customizes list
        self.concat(value)  # Copies mutable defaults

    def intersect(self, other):  # other is any sequence
        res = []  # self is the subject

        for zeta in self:

            if zeta in other:  # Pick common items
                res.append(zeta)

        return Set(res)  # Return a new Set

    def union(self, other):  # other is any sequence
        res = Set(self)  # Copy me and my list
        res.concat(other)
        return res

    def concat(self, value):  # value: list, Set, etc.
        for x in value:  # Removes duplicates
            if not x in self:
                self.append(x)


def decorator_function(original_function):
    def wraper_function(*args, **kwargs):
        print("stuff inside")
        return original_function(*args, **kwargs)
    return wraper_function


@decorator_function
def display_function(x):
    print("display function", x)


# decorated_display = decorator_function(display_function)
# decorated_display()
# display_function(20)


class decorator_class:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):

        return self.original_function(*args, **kwargs)


# @decorator_class
# def hellow():
#     print("hellow")


# hellow = decorator_class(hellow)
# hellow()


subtitles = {}

movie_hash = "abs"

for i in range(20):
    subtitles.setdefault(movie_hash, []).append([i, 40, 50, 12])

for x in subtitles['abs']:
    print(x)
