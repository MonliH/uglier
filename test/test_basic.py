def add_values(n1, n2):
    return n1 + n2


def add_input_to_n(n):
    user_input = int(input("Enter a number: "))
    return add_values(user_input, n)


user_added_10 = add_input_to_n(10)
print(user_added_10)

