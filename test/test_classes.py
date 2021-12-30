class MyClass:
    def __init__(self, n):
        self.important_number = n

    def print_important_number(self):
        print(self.important_number)


my_class_1 = MyClass(92)
my_class_2 = MyClass(1123)
my_class_1.print_important_number()
my_class_2.print_important_number()
