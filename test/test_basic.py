def add_values(n1, n2):
    return n1 + n2


def add_10_to_string(n):
    return str(add_values(int(n), 10))


num = add_10_to_string("10")
print(num)
