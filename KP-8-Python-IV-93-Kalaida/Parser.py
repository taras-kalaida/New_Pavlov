import sys
def make_tree(tokens):
    result = ""
    count = 0
    for i in tokens:
        for j in i:
            result += "\n" + int(count/1.25) * "   " + "{" + f"'{j.value}'" + ":" + "{" + f"'{j.name}'"
            count += 1
    result+="\n"+ int(count/1.25) * "   "+"}"*int(count/1.45)
    print(result)
    count=0
    for j in tokens :
        count+=1
        for i in j:
            if i.name=="negative":
                error=""

                print("Syntax error", i.value, "Строка - " + str(count + 1))
                for k in j:
                    error+=k.value+" "
                print(error)
                sys.exit()
            if i.name == "string":
                error = ""

                print("Syntax error", i.value, "Строка - " + str(count + 1))
                for k in j:
                    error += k.value + " "
                print(error)
                sys.exit()
