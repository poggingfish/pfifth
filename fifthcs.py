from io import TextIOWrapper 
import os, sys
from re import S
load = False
loadtype = ""
loadvalue = []
word_data = {}
def load_builtins():
    return ['"', 'nl', '"', 'word', '10', 'emit', '.', 'endword', '"', 'iterate', '"', 'word', '"', 'var', '"', 'set', '"', 'var', '"', 'get', 'get', '1', '+', '"', 'var', '"', 'get', 'set', 'endword', '"', 'decrement', '"', 'word', '"', 'var', '"', 'set', '"', 'var', '"', 'get', 'get', '1', '-', '"', 'var', '"', 'get', 'set', 'endword']
def reset_load():
    global load
    global loadtype
    global loadvalue
    load = False
    loadtype = ""
    loadvalue = []
def load_program(file):
    global program
    return file.read().replace("\n"," ").split()
def compile(file: TextIOWrapper, program: list):
    global load
    global loadtype
    global word_data
    iter = 0
    for x in program:
        iter+=1
        if load == True:
            x = x.replace("n:","")
            if loadtype == "while":
                if x == "=":
                    file.write("while (programstack.Pop == programstack.Pop) {\n")
                elif x == "!":
                    file.write("while (programstack.Pop != programstack.Pop) {\n")
                elif x == ">":
                    file.write("while (programstack.Pop > programstack.Pop) {\n")
                elif x == "<":
                    file.write("while (programstack.Pop < programstack.Pop) {\n")
                reset_load()
                continue
            if loadtype == "string":
                if x == '"':
                    file.write('programstack.Push("' + " ".join(loadvalue) + '");\n')
                    reset_load()
                    continue
            if loadtype == "word":
                if x == "endword":
                    word_data.update({word_name: loadvalue})
                    reset_load()
                    continue
            loadvalue.append(x)
            continue
        if x in word_data:
            compile(file, word_data[x])
        elif x == "execute":
            file.write("programstack.Pop();\n")
            execute = program[iter-3]
            try:(compile(file, load_program(open(execute))))
            except:(compile(file, load_program(open("/usr/share/fifth/"+execute))))
        elif x == ".":
            file.write(f"Console.Write(programstack.Pop());\n")      
        elif x == "+":
            file.write("programstack.Push((int)programstack.Pop() + (int)programstack.Pop());\n")
        elif x == "-":
            file.write("programstack.Push((int)programstack.Pop() - (int)programstack.Pop());\n")
        elif x == "*":
            file.write("programstack.Push((int)programstack.Pop() * (int)programstack.Pop());\n")
        elif x == "/":
            file.write("programstack.Push((int)programstack.Pop() / (int)programstack.Pop());\n)")
        elif x == '"':
            load = True   
            loadtype = "string"
        elif x == "word":
            file.write("programstack.Pop();\n")
            word_name = program[iter-3]
            loadtype="word"
            load = True
        elif x == "emit":
            file.write("programstack.Push( Convert.ToChar(programstack.Pop()) );\n")
        elif x == "dup":
            file.write("programstack.Push(programstack.Peek());\n")
        elif x == "set":
            file.write("name = (string)programstack.Pop();\n")
            file.write("value = programstack.Pop();\n")
            file.write("try{variables.Add((string)name, (object)value);}catch{variables[(string)name]=(object)value;}\n")
        elif x == "get":
            file.write("programstack.Push(variables[(string)programstack.Pop()]);\n")
        elif x == "while":
            load = True
            loadtype = "while"
        elif x == "loop":
            file.write("var loopcount = (int)programstack.Pop();\n")
            file.write("for (int i = 0; i < loopcount; i++){\n")
        elif x == "endwhile" or x == "endfor" or x == "endloop" or x == "endif":
            file.write("}\n")
        elif x == "words":
            for word in word_data:
                file.write(f"Console.WriteLine(\"{word}\");\n")
        elif x == "array_init":
            file.write("programstack.Push(new List<object>());\n")
        elif x == "array_add":
            file.write("temp = programstack.Pop();\n")
            file.write("temp2 = programstack.Pop();\n")
            file.write("programstack.Push(temp);\n")
            file.write("programstack.Push(temp2);\n")
            file.write("temp_list = (List<object>)programstack.Pop();\n")
            file.write("temp_list.Add(programstack.Pop());\n")
            file.write("programstack.Push(temp_list);\n")
        elif x == "array_pop":
            file.write("temp_list = (List<object>)programstack.Pop();\n")
            file.write("temp = temp_list[temp_list.Count()-1];\n")
            file.write("programstack.Push(temp);\n")
        elif x == "arln":
            # Get the length of the array
            file.write("temp_list = (List<object>)programstack.Pop();\n")
            file.write("programstack.Push((int)temp_list.Count());\n")
        elif x == "index":
            #swap the top two items on the stack
            file.write("temp = programstack.Pop();\n")
            file.write("temp2 = programstack.Pop();\n")
            file.write("programstack.Push(temp);\n")
            file.write("programstack.Push(temp2);\n")
            #index the list on the stack with the value on the stack 
            file.write("programstack.Push(((List<object>)programstack.Pop())[(int)programstack.Pop()]);\n")
        elif x == "for":
            file.write("foreach (var item in (List<object>)programstack.Pop()){\n")
            file.write("programstack.Push(item);\n")
        elif x == "pop":
            file.write("programstack.Pop();\n")
        elif x == "open_file":
            #Open the file with the name on the stack and push the file object to the stack
            file.write("programstack.Push(new StreamReader(new FileStream(programstack.Pop().ToString(), FileMode.Open)));\n")
        elif x == "open_file_write":
            file.write("programstack.Push(new StreamWriter(new FileStream(programstack.Pop().ToString(), FileMode.Create)));\n")
        elif x == "close_file":
            file.write("((StreamReader)programstack.Pop()).Close();\n")
        elif x == "read_file":
            file.write("programstack.Push(((StreamReader)programstack.Pop()).ReadLine());\n")
        else:
            x = int(x)
            file.write(f"programstack.Push({x});\n")
os.mkdir("output")
os.system("dotnet new console -o output")
with open("output/Program.cs", "w") as file:
    file.write("using System.IO;\n")
    file.write("namespace Program\n{\n")
    file.write("class Program\n{\n")
    file.write("static void Main(string[] args)\n{\n")
    file.write("Stack<object> programstack = new Stack<object>();\n")
    file.write("List<object> temp_list;")
    file.write("object temp;")
    file.write("object temp2;")
    file.write("string name = \"\";")
    file.write("object value;")
    file.write("Dictionary<String, object> variables = new Dictionary<String, object>();\n")
    compile(file, load_builtins())
    compile(file, load_program(open(sys.argv[1])))
    file.write("}\n}\n}")
os.system("rm output/output.csproj")
with open("output/output.csproj", "w") as csproj:
    csproj.write("""<Project Sdk="Microsoft.NET.Sdk">
<PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net6.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <PublishSingleFile>true</PublishSingleFile>
</PropertyGroup>
</Project>
""")
os.system("dotnet publish -r linux-x64 --self-contained false output/")
os.system("cp output/bin/Debug/net6.0/linux-x64/publish/output out.out")
os.system("cp output/Program.cs out.cs")
os.system("rm -rf output")