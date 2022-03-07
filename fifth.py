#!/usr/bin/env python3
import os
import time, sys
stack = []
program = []
words = {}
variables = {}
def load_program(file):
    global program
    return file.read().replace("\n"," ").split()
def load_builtins():
    return ['"', 'nl', '"', 'word', '10', 'emit', 'endword', '"', 'iterate', '"', 'word', '"', 'var', '"', 'set', '"', 'var', '"', 'get', 'get', '1', '+', '"', 'var', '"', 'get', 'set', 'endword']
def run(program):
    global stack
    global load_program
    global variables
    global words
    global interactive
    load_data = []
    load = False
    load_wait = False
    load_type = ""
    for x in program:
        try:
            if load == True:
                if x == "endword":
                    if load_type == "word":
                        load = False
                        data = " "
                        words.update({word_name: data.join(load_data[0:])})
                        load_data = []
                        continue
                    else:
                        raise Exception("Error: endword without word")
                if load_type == "loop":
                    if x == "endloop":
                        loop_amount = stack.pop()
                        load = False
                        for x in range(loop_amount):
                            run(load_data[0:])
                        load_data = []
                        continue
                if load_type == "string":
                    if x == '"':
                        stack.append(" ".join(load_data))
                        load = False
                        load_data = []
                        continue
                if load_type == "if":
                    if x == "endif":
                        if load_data[0] == "=":
                            if if1 == if2:
                                run(load_data[1:])
                        if load_data[0] == "!":
                            if if1 != if2:
                                run(load_data[1:])
                        if load_data[0] == "<":
                            if if1 < if2:
                                run(load_data[1:])
                        if load_data[0] == ">":
                            if if1 > if2:
                                run(load_data[1:])
                        load = False
                        load_data = []
                        continue
                load_data.append(x.replace("n:",""))
                continue
            if x in words:
                run(words[x].split(" "))
            elif x == "+":
                stack.append(stack.pop() + stack.pop())
            elif x == "-":
                stack.append(stack.pop() - stack.pop())
            elif x == "*":
                stack.append(stack.pop() * stack.pop())
            elif x == "/":
                stack.append(stack.pop() / stack.pop())
            elif x == ".":
                print(stack.pop(), end=" ")
            elif x == "mod":
                stack.append(stack.pop() % stack.pop())
            elif x == "dup":
                x = stack.pop()
                stack.append(x)
                stack.append(x)
            elif x == "word":
                word_name = stack.pop()
                load = True
                load_type = "word"
            elif x == "loop":
                load_type = "loop"
                load = True
            elif x == "sleep":
                time.sleep(stack.pop()/1000)
            elif x == "emit":
                print(chr(stack.pop()), end="")
            elif x == '"':
                load_type = "string"
                load = True
            elif x == "stdin":
                stack.append(input())
            elif x == "toint":
                stack.append(int(stack.pop()))
            elif x == "if":
                load_type = "if"
                load = True
                if1 = stack.pop()
                if2 = stack.pop()
            elif x == "set":
                variables.update({stack.pop(): stack.pop()})
            elif x == "get":
                stack.append(variables[stack.pop()])
            elif x == "execute":
                run_program = stack.pop()
                try:
                    run(load_program(open(run_program)))
                except:
                    run(load_program(open("/usr/share/fifth/" + run_program)))
            elif x == "words":
                for x in words:
                    print(x)
            elif x == "pop":
                stack.pop()
            elif x == "bye" and interactive == True:
                print("Bye!")
                exit(0)
            elif x == "stack" and interactive == True:
                for i in stack:
                    print(i)
            else:
                stack.append(int(x))
        except:
            print("Something went wrong at instruction "+str(x))
            if interactive != True:
                exit(1)
            load = False
            load_data = []
interactive = False
run(load_builtins())
for x in sys.argv[1:]:
    if x == "interactive":
        interactive = True
        while True:
            print(">>> ", end="")
            run(input().split(" "))
            print("")
    if x == "install":
        if os.geteuid() != 0:
            print("You must be root to install!")
            exit(1)
        else:
            os.system("cp fifth.py /usr/bin/fifth")
            std = input("Would you like to install the standard word library? (y/n) ")
            if std == "y":
                try:
                    os.mkdir("/usr/share/fifth/")
                except:
                    pass
                os.system("cp std/std.fifth /usr/share/fifth/std.fifth")
            elif std == "n":
                print("Okay, I won't install the standard word library.")
            else:
                print("I don't understand that. And I won't install the standard word library.")
            print("Installed!")
            exit(0)
program = load_program(open(sys.argv[1]))
run(program)