def fib(n):
    # Slow recursive implementation
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


result = fib(30)
print(result)
