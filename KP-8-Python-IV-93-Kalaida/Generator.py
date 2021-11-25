def new_line():
    return "\n"


def generator_help():
    return " " * 4


class Generator:
    def Generator(self, tokens):
        end = None
        variables = []
        variables_2 = []
        registers = [["eax", ["ebp+12"]], ["ebx", ["ebp+8"]]]
        data = []
        data_str = ""
        for t in tokens:
            for j in t:
                if j.name == "variable" and j.value not in data:
                    data.append(j.value)
        for i in data:
            data_str += "\n" + i + " dd ?"
        dict_regs = dict()

        flag = False
        result = ''
        name = ""
        parser_count = 0
        for t in range(len(tokens)):
            if tokens[t][0].name == "else":
                flag = True
        for t in range(len(tokens)):

            if tokens[t][0].name == "function" and "main" not in tokens[t][1].value:
                parser_count += 1
                function_name = tokens[t][1].value
                count = 0
                for j in tokens[t]:
                    if j.value not in variables and j.name == "variable":
                        variables.append(j)
                        if count == 2:
                            count = 0
                        dict_regs.update({j.value: registers[count]})

                        count += 1
                result += new_line() + name + tokens[t][1].value + " " + "proc"
                name = generator_help() * parser_count
                result += new_line() + name + "push" + " " + "ebp"
                result += new_line() + name + "mov" + " " + "ebp" + "," + " " + "esp"

                for k, j in dict_regs.items():
                    if new_line() + name + "mov" + " " + str(j[0]) + "," + " " + f"[{j[1][0]}]" not in result:
                        result += new_line() + name + "mov" + " " + str(j[0]) + "," + " " + f"[{j[1][0]}]"
                    result += new_line() + name + "mov" + " " + k + "," + " " + str(j[0])

            if tokens[t][0].name == "cycle":
                parser_count += 1

                result += new_line() + name + "@while:"
                name = generator_help() * parser_count
                result += new_line() + name + "cmp"
                for j in tokens[t]:
                    if j.name == "variable":
                        result += " " + dict_regs[j.value][0] + ','
                result = result[0:-1]
                for j in tokens[t]:
                    if j.value == '!=':
                        result += new_line() + name + "je finish"
                    if j.value == '>':
                        result += new_line() + name + "ja finish"
                    if j.value == '<':
                        result += new_line() + name + "jg finish"
                    if j.value == '==':
                        result += new_line() + name + "jne finish"
            if tokens[t][0].value == "if":
                result += new_line() + name + "cmp"

                for j in tokens[t]:
                    if j.name == "variable":
                        result += " " + dict_regs[j.value][0] + ','
                result = result[0:-1]
                for j in tokens[t]:
                    if j.value == '>':
                        end = []
                        end.append("@grater:")
                        end.append(tokens[t + 1])
                        result += new_line() + name + "ja @grater"
                    if j.value == '<':
                        end = []
                        end.append("@lesser:")
                        end.append(tokens[t + 1])
                        result += new_line() + name + "jl @lesser"
                    if j.value == '==':
                        end = []
                        end.append("@equel:")
                        end.append(tokens[t + 1])
                        result += new_line() + name + "je @equel"
                    if j.value == '!=':
                        end = []
                        end.append("@not_equel:")
                        end.append(tokens[t + 1])
                        result += new_line() + name + "jne @not_equel"

            if tokens[t][0].value == "else":

                for j in range(len(tokens[t + 1])):
                    if tokens[t + 1][j].value == "=":
                        else_result2 = dict_regs[tokens[t + 1][j - 1].value]
                        else_result = tokens[t + 1][j - 1].value
                        result += new_line() + name + "mov" + " " + str(else_result2[0]) + ", " + \
                                  tokens[t + 1][j - 1].value
                        help2 = new_line() + name + "mov" + " " + str(else_result2[0]) + ", " + \
                                tokens[t + 1][j - 1].value
                        for k in tokens[t + 1]:
                            if k.value == "/":
                                result2 = result.replace(help2, "")
                variables_else = []
                for j in range(len(tokens[t + 1])):
                    if tokens[t + 1][j].value == "*":
                        result += new_line() + name + "imul"
                        if len(variables_else) == 0:
                            result += " " + str(dict_regs[tokens[t + 1][j - 1].value][0]) + ", " + str(
                                dict_regs[tokens[t + 1][j + 1].value][0])
                            variables_else.append(tokens[t + 1][j - 1].value)
                        else:
                            if else_result2[0] != dict_regs[tokens[t + 1][j + 1].value][0]:
                                result += " " + else_result2[0] + ", " + str(
                                    dict_regs[tokens[t + 1][j + 1].value][0])
                            else:
                                result += " " + else_result2[0] + ", " + str(
                                    tokens[t + 1][j + 1].value)
                        if len(variables_else) == 0:
                            result += " " + str(dict_regs[tokens[t + 1][j - 1]][0]) + "," + str(
                                dict_regs[tokens[t + 1][j + 1]][0])
                    if tokens[t + 1][j].value == "/":

                        if len(variables_else) == 0:
                            if new_line() + name + "mov edx, 0" not in variables_else:
                                result += new_line() + name + "mov edx, 0 "
                                variables_else.append(new_line() + name + "mov edx, 0")
                                if help2 not in result:
                                    result += help2
                            result += new_line() + name + "div" + " " + str(
                                dict_regs[tokens[t + 1][j + 1].value][0])
                            variables_else.append(tokens[t + 1][j + 1].value)
                        else:
                            if new_line() + name + "mov edx, 0" not in variables_else:
                                result += new_line() + name + "mov edx, 0 "
                                variables_else.append(new_line() + name + "mov edx, 0")
                            if else_result2[0] != dict_regs[tokens[t + 1][j + 1].value][0]:
                                result += new_line() + name + "div" + " " + str(
                                    dict_regs[tokens[t + 1][j + 1].value][0])
                            else:
                                result += new_line() + name + "div" + " " + str(
                                    tokens[t + 1][j + 1].value)
                    if tokens[t + 1][j].value == "+":
                        result += new_line() + name + "add"
                        if len(variables_else) == 0:
                            result += " " + str(dict_regs[tokens[t + 1][j - 1].value][0]) + ", " + str(
                                dict_regs[tokens[t + 1][j + 1].value][0])
                            variables_else.append(tokens[t + 1][j - 1].value)
                        else:
                            if else_result2[0] != dict_regs[tokens[t + 1][j + 1].value][0]:
                                result += " " + else_result2[0] + ", " + str(
                                    dict_regs[tokens[t + 1][j + 1].value][0])
                            else:
                                result += " " + else_result2[0] + ", " + str(
                                    tokens[t + 1][j + 1].value)
                    if tokens[t + 1][j].value == "-":
                        result += new_line() + name + "sub"
                        if len(variables_else) == 0:
                            result += " " + str(dict_regs[tokens[t + 1][j - 1].value][0]) + ", " + str(
                                dict_regs[tokens[t + 1][j + 1].value][0])
                            variables_else.append(tokens[t + 1][j - 1].value)
                        else:
                            if else_result2[0] != dict_regs[tokens[t + 1][j + 1].value][0]:
                                result += " " + else_result2[0] + ", " + str(
                                    dict_regs[tokens[t + 1][j + 1].value][0])
                            else:
                                result += " " + else_result2[0] + ", " + str(
                                    tokens[t + 1][j + 1].value)
                result += new_line() + name + "mov" + " " + else_result + ", " + \
                          str(else_result2[0])
                if new_line() + name + "jmp" + " " + "@while" not in result:
                    result += new_line() + name + "jmp" + " " + "@while"
                flag = False

            if end is not None and tokens[t - 1][0].value != 'if' and flag != True:
                result += new_line() + name + end[0]
                for j in range(len(end[1])):
                    if end[1][j].value == "=":
                        if_result2 = dict_regs[end[1][j - 1].value]
                        if_result = end[1][j - 1].value
                        result += new_line() + name + "mov" + " " + str(if_result2[0]) + ", " + \
                                  end[1][j - 1].value
                        help = new_line() + name + "mov" + " " + str(if_result2[0]) + ", " + \
                               end[1][j - 1].value
                        for k in end[1]:
                            if k.value == "/":
                                result = result.replace(help, "")
                variables_if = []
                for j in range(len(end[1])):
                    if end[1][j].value == "*":
                        result += new_line() + name + "imul"
                        if len(variables_if) == 0:
                            result += " " + str(dict_regs[end[1][j - 1].value][0]) + ", " + str(
                                dict_regs[end[1][j + 1].value][0])
                            variables_if.append(end[1][j - 1].value)
                        else:
                            if if_result2[0] != dict_regs[end[1][j + 1].value][0]:
                                result += " " + if_result2[0] + ", " + str(
                                    dict_regs[end[1][j + 1].value][0])
                            else:
                                result += " " + if_result2[0] + ", " + str(
                                    end[1][j + 1].value)

                    if end[1][j].value == "/":

                        if len(variables_if) == 0:
                            if new_line() + name + "mov edx, 0" not in variables_if:
                                result += new_line() + name + "mov edx, 0 "
                                variables_if.append(new_line() + name + "mov edx, 0")
                                if help not in result:
                                    result += help
                            result += new_line() + name + "div" + " " + str(
                                dict_regs[end[1][j + 1].value][0])
                            variables_if.append(end[1][j + 1].value)
                        else:
                            if new_line() + name + "mov edx, 0" not in variables_if:
                                result += new_line() + name + "mov edx, 0 "
                                variables_if.append(new_line() + name + "mov edx, 0")
                            if if_result2[0] != dict_regs[end[1][j + 1].value][0]:
                                result += new_line() + name + "div" + " " + str(
                                    dict_regs[end[1][j + 1].value][0])
                            else:

                                result += new_line() + name + "div" + " " + str(
                                    end[1][j + 1].value)
                    if end[1][j].value == "+":
                        result += new_line() + name + "add"
                        if len(variables_if) == 0:
                            result += " " + str(dict_regs[end[1][j - 1].value][0]) + ", " + str(
                                dict_regs[end[1][j + 1].value][0])
                            variables_if.append(end[1][j - 1].value)
                        else:
                            if if_result2[0] != dict_regs[end[1][j + 1].value][0]:
                                result += " " + if_result2[0] + ", " + str(
                                    dict_regs[end[1][j + 1].value][0])
                            else:
                                result += " " + if_result2[0] + ", " + str(
                                    end[1][j + 1].value)
                    if end[1][j].value == "-":
                        result += new_line() + name + "sub"
                        if len(variables_if) == 0:
                            result += " " + str(dict_regs[end[1][j - 1].value][0]) + ", " + str(
                                dict_regs[end[1][j + 1].value][0])
                            variables_if.append(end[1][j - 1].value)
                        else:
                            if if_result2[0] != dict_regs[end[1][j + 1].value][0]:
                                result += " " + if_result2[0] + ", " + str(
                                    dict_regs[end[1][j + 1].value][0])
                            else:
                                result += " " + if_result2[0] + ", " + str(
                                    end[1][j + 1].value)
                result += new_line() + name + "mov" + " " + if_result + ", " + \
                          str(if_result2[0])
                end = None
            if tokens[t][0].name == "variable" and tokens[t - 1][0].name != "if" and tokens[t - 1][0].name != "else":
                if tokens[t][0].value not in variables and len(variables) <= 4:
                    variables.append(tokens[t][0])
                    variables_2.append(tokens[t][0])
                    count228 = 0
                    for j in tokens[t]:
                        if count228 == 0 and j.name == "variable":
                            print("mov" + " " + j.value + ", ")
                            result += new_line() + name + "mov" + " " + j.value + ", "
                            count228 += 1
                            var = j.value
                    for j in range(len(tokens[t])):

                        if tokens[t][j].value == "=":
                            result += dict_regs[tokens[t][j + 1].value][0]
                            dict_regs.update({var: dict_regs[tokens[t][j + 1].value][0]})
            if tokens[t][0].value == "return":
                name = name[0:int(len(name) / 2)]
                result += new_line() + name + "jmp @while"
                result += new_line() + name + "finish:"
                flag = 0
                for j in tokens[t]:
                    if j.name == "variable":
                        if j not in variables_2:
                            result += new_line() + name + "mov" + " " + j.value + ", " + dict_regs[j.value][0]
                for j in tokens[t]:
                    if j.value == "*" or j.value == "+" or j.value == "-" or j.value == "/":
                        flag = 1

                if flag == 0:
                    for k in tokens[t]:
                        if k.name == "variable":
                            result += new_line() + name + f'fn MessageBox, 0, str$({k.value}), "IV-93, 8, Kalaida", MB_OK'
                            result += new_line() + name + "ret"
                else:

                    res = []
                    for j in range(len(tokens[t])):
                        if tokens[t][j].value == "/":
                            if len(res) == 0:

                                count222323 = 0
                                for k in tokens[t]:
                                    if k.name == "variable":
                                        if count222323 == 0:
                                            result += new_line() + name + "mov" + " " + dict_regs[
                                                k.value] + ", " + k.value
                                            count222323 += 1
                                            res.append(dict_regs[k.value])
                                            flag228 = 0
                                            for o in tokens[t]:
                                                if o.value == "/":
                                                    flag228 = True
                                            if flag228 == True:
                                                result += new_line() + name + "mov " + "edx" + ", " + "0"

                                result += new_line() + name + "div" + " " + tokens[t][j + 1].value

                            else:
                                result += new_line() + name + "div" + " " + tokens[t][j + 1].value
                        if tokens[t][j].value == "*":
                            if len(res) == 0:
                                count222323 = 0
                                for k in tokens[t]:
                                    if k.name == "variable":
                                        if count222323 == 0:
                                            flag228 = 0
                                            for o in tokens[t]:
                                                if o.value == "/":
                                                    flag228 = True
                                            if flag228 == True:
                                                result += new_line() + name + "mov " + "edx" + ", " + "0"
                                            if k.value not in variables_2:
                                                result += new_line() + name + "mov" + " " + dict_regs[
                                                    k.value][0] + ", " + k.value
                                                res.append(dict_regs[k.value][0])
                                            else:
                                                result += new_line() + name + "mov" + " " + dict_regs[
                                                    k.value] + ", " + k.value
                                                res.append(dict_regs[k.value])
                                            count222323 += 1


                                result += new_line() + name + "imul" + " " + res[0] + ", " + tokens[t][
                                    j + 1].value
                            else:
                                result += new_line() + name + "imul" + " " + res[0] + ", " + tokens[t][j + 1].value
                        if tokens[t][j].value == "+":
                            if len(res) == 0:
                                count222323 = 0
                                for k in tokens[t]:
                                    if k.name == "variable":
                                        if count222323 == 0:
                                            flag228 = 0
                                            for o in tokens[t]:
                                                if o.value == "/":
                                                    flag228 = True
                                            if flag228 == True:
                                                result += new_line() + name + "mov " + "edx" + ", " + "0"

                                            if k.value not in variables_2:
                                                result += new_line() + name + "mov" + " " + dict_regs[
                                                    k.value][0] + ", " + k.value
                                                res.append(dict_regs[k.value][0])
                                            else:
                                                result += new_line() + name + "mov" + " " + dict_regs[
                                                    k.value] + ", " + k.value
                                                res.append(dict_regs[k.value])
                                            count222323 += 1


                                result += new_line() + name + "add" + " " + res[0] + ", " + tokens[t][
                                    j + 1].value
                            else:
                                result += new_line() + name + "add" + " " + res[0] + ", " + tokens[t][j + 1].value
                        if tokens[t][j].value == "-":
                            if len(res) == 0:
                                count222323 = 0
                                for k in tokens[t]:
                                    if k.name == "variable":
                                        if count222323 == 0:
                                            flag228 = 0
                                            for o in tokens[t]:
                                                if o.value == "/":
                                                    flag228 = True
                                            if flag228 == True:
                                                result += new_line() + name + "mov " + "edx" + ", " + "0"
                                            if k.value not in variables_2:
                                                result += new_line() + name + "mov" + " " + dict_regs[
                                                    k.value][0] + ", " + k.value
                                                res.append(dict_regs[k.value][0])
                                            else:
                                                result += new_line() + name + "mov" + " " + dict_regs[
                                                    k.value] + ", " + k.value
                                                res.append(dict_regs[k.value])
                                            count222323 += 1


                                result += new_line() + name + "sub" + " " + res[0] + ", " + tokens[t][
                                    j + 1].value
                            else:
                                result += new_line() + name + "sub" + " " + res[0] + ", " + tokens[t][j + 1].value
                    result += new_line() + name + f'fn MessageBox, 0, str$({res[0]}), "IV-93, 8, Kalaida", MB_OK'
                    result += new_line() + name + "ret"

        result += new_line() + function_name + " " + "endp"
        counter100 = 0
        for t in range(len(tokens)):
            if tokens[t][0].name == "function" and "main" in tokens[t][1].value:
                for j in tokens[t]:

                    if j.name == "function_name":
                        result += new_line() + j.value + ":"
            for j in tokens[t]:
                if j.name == "number":
                    if counter100 <= 1:
                        result += new_line() + "push" + " " + j.value
                        counter100 += 1
        result += new_line() + "invoke" + " " + function_name
        result += new_line() + "invoke ExitProcess, 0"
        for t in range(len(tokens)):
            if tokens[t][0].name == "function" and "main" in tokens[t][1].value:
                result += new_line() + "END" + " " + tokens[t][1].value


        return result, data_str
