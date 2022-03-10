#!/usr/bin/env python3
import os
import time, sys, random
stack = []
program = []
words = {}
variables = {}
current_file = ""
def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()
def move (x, y):
    sys.stdout.write("\033[%d;%dH" % (y, x))
    sys.stdout.flush()
def load_program(file):
    global program
    return file.read().replace("\n"," ").split()
def load_builtins():
    return ['"', 'nl', '"', 'word', '10', 'emit', '.', 'endword', '"', 'iterate', '"', 'word', '"', 'var', '"', 'set', '"', 'var', '"', 'get', 'get', '1', '+', '"', 'var', '"', 'get', 'set', 'endword', '"', 'decrement', '"', 'word', '"', 'var', '"', 'set', '"', 'var', '"', 'get', 'get', '1', '-', '"', 'var', '"', 'get', 'set', 'endword']
def run(program):
    global stack
    global load_program
    global variables
    global words
    global interactive
    global current_file
    load_data = []
    load = False
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
                        if loop_amount == 0:
                            while True:
                                run(load_data[0:])
                        else:
                            for x in range(loop_amount):
                                run(load_data[0:])
                        load_data = []
                        continue
                if load_type == "while":
                    if x == "endwhile":
                        load = False
                        if load_data[0] == "=":
                            while stack.pop() == stack.pop():
                                run(load_data[1:])
                        if load_data[0] == "!":
                            while stack.pop() != stack.pop():
                                run(load_data[1:])
                        if load_data[0] == "<":
                            while stack.pop() < stack.pop():
                                run(load_data[1:])
                        if load_data[0] == ">":
                            while stack.pop() > stack.pop():
                                run(load_data[1:]) 
                        load_data = []
                        continue
                if load_type == "string":
                    if x == '"':
                        stack.append(" ".join(load_data))
                        load = False
                        load_data = []
                        continue
                if load_type == "ignore":
                    if x == ";":
                        load = False
                        load_data = []
                    continue
                if load_type == "if":
                    previous_if1 = if1
                    previous_if2 = if2
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
                if load_type == "else":
                    if x == "endif":
                        if previous_if1!=previous_if2 and if1==if2:
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
                if load_type == "for":
                    if x == "endfor":
                        for x in stack.pop():
                            stack.append(x)
                            run(load_data[0:])
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
                print(stack.pop(), end="")
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
                stack.append(chr(stack.pop()))
            elif x == '"':
                load_type = "string"
                load = True
            elif x == "stdin":
                stack.append(input())
            elif x == "toint":
                stack.append(int(stack.pop()))
            elif x == "tostr":
                stack.append(str(stack.pop()))
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
            elif x == "while":
                load_type = "while"
                load = True
            elif x == "else":
                load_type = "else"
                load = True
            elif x == "#":
                load_type="ignore"
                load=True
            elif x == "array_init":
                new_array = []
                stack.append(new_array)
            elif x == "array_add":
                stack[0].append(stack.pop())
            elif x == "array_pop":
                stack.append(stack[0].pop())
            elif x == "length":
                stack.append(len(stack.pop()))
            elif x == "for":
                load_type="for"
                load=True
            elif x == "index":
                pop1 = stack.pop()
                pop2 = stack.pop()
                stack.append(pop2[pop1])
            elif x == "change_index":
                pop1 = stack.pop()
                pop2 = stack.pop()
                pop3 = stack.pop()
                pop3[pop2] = pop1
                stack.append(pop3)
            elif x == "arln":
                stack.append(len(stack.pop()))
            elif x == "random":
                stack.append(random.randrange(stack.pop(), stack.pop()))
            elif x == "split":
                stack.append(stack.pop().split(stack.pop()))
            elif x == "pasp":
                pop1 = stack.pop()
                pop2 = stack.pop()
                pop3 = stack.pop()
                print_there(pop3, pop2, pop1)
            elif x == "move_cursor":
                move(stack.pop(), stack.pop())              
            elif x == "clear_screen":
                print("\033[2J")
            elif x == "open_file":
                file = stack.pop()
                current_file = file
                stack.append(open(file))
            elif x == "open_file_write":
                file = stack.pop()
                current_file = file
                stack.append(open(file, "w"))
            elif x == "read_file":
                stack.append(stack.pop().read())
            elif x == "write_file":
                stack.append(stack.pop().write(stack.pop()))
            elif x == "close_file":
                stack.append(stack.pop().close())
            elif x == "index_write":
                pop1 = stack.pop()
                pop2 = stack.pop()
                pop3 = stack.pop()
                pop3.close()
                with open(current_file) as f:
                    splitf = f.read().split(" ")
                    splitf[pop2] = pop1
                    final = ""
                for x in splitf:
                    final += str(x) + " "
                stack.append(open(current_file, "w"))
                pop3 = stack.pop()
                pop3.write(final)
            elif x == "start_timer":
                start_time = time.perf_counter()
            elif x == "end_timer":
                # Returns the time in seconds since the start_timer command was run rounded to 1 decimal place
                stack.append(round(time.perf_counter() - start_time, 1))
            elif x == "terminate":
                exit(0)
            elif x == "term_width":
                # Push the width of the terminal to the stack
                stack.append(os.get_terminal_size()[0])
            elif x == "term_height":
                # Push the height of the terminal to the stack
                stack.append(os.get_terminal_size()[1])
            elif x == "bye" and interactive == True:
                print("Bye!")
                exit(0)
            elif x == "stack" and interactive == True:
                for i in stack:
                    print(i)
            else:
                stack.append(int(x))
        except Exception as e:
            #Check if exception is keyboard interrupt
            if e == KeyboardInterrupt:
                print("KeyboardInterrupt")
                exit(0)
            print("Something went wrong at instruction "+str(x))
            if interactive != True:
                exit(1)
            load = False
            load_data = []
interactive = False
run(load_builtins())
for x in sys.argv[1:]:
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
    if x == "builtins":
        for x in load_builtins():
            print(x)
            exit(0)
    if x == "load-program":
        print(load_program(open(sys.argv[2])))
        exit(0)
program = load_program(open(sys.argv[1]))
run(program)