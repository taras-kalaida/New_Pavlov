def func_new(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b -a
    return a

def func_main():
    func_new(25, 60)




