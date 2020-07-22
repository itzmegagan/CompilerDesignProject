#!/usr/bin/python3

"""
int main()
begin
int L[num];
int maxval=L[num];
for i=num to n-num do
if L[i]>maxval
maxval=L[i];
endif
endfor
return(maxval)
end

"""

from ourrules import Consts
import sys
import os

#Lexical Analyser...This function identifies tokens
def lexical_analyser():
    keywords=['int','main','begin','for','to','do','if','endif','endfor','return','End']
    operators=['(',')','[',']','=','-','>']
    w=""

    if os.stat("question.txt").st_size==0 :
        print("File is empty")
    else:
        with open('question.txt','r') as f:
            for line in f:
                for word in line:
                    for character in word:
                        if character.isspace() or character==';':
                            if w=="":
                                continue;
                            elif w in keywords:
                                print("%s : Keyword"%(w))
                            else:
                                print("%s : Identifier"%(w))
                            w=""
                        elif character in operators:
                            print("%s : Operator"%(character))
                            if w=="":
                                continue
                            elif w in keywords:
                                print("%s : Keyword"%(w))
                            else:
                                print("%s : Identifier"%(w))
                            w=""
                        else:
                            w=w+character




# Tokenizer... This function converts the program string to token string
def tokenizer(program_string):
    tokens = Consts.tokens
    ip = 0
    program_string += '$'
    token_string = ""
    while program_string[ip] != '$':
        current_token = ""
        if program_string[ip].isalpha() or program_string[ip] == '_':
            current_token += program_string[ip]
            ip += 1
            while program_string[ip].isalnum() or program_string[ip] == '_':
                current_token += program_string[ip]
                ip += 1
            if current_token in tokens.keys():
                token_string += tokens[current_token]
            else:
                token_string += tokens['var']
        elif program_string[ip].isnumeric():
            current_token += program_string[ip]
            ip += 1
            while program_string[ip].isnumeric() or program_string[ip] == '.':
                current_token += program_string[ip]
                ip += 1
            token_string += tokens['num']
        else:
            if program_string[ip] in tokens:
                token_string += tokens[program_string[ip]]
                ip += 1
            else:
                nl_count = 1
                pointer_count = 0
                for _ in range(ip):
                    if program_string[_] == '\n':
                        nl_count += 1
                        pointer_count = 0
                    else:
                        pointer_count += 1
                print("Tokenizer: Error on line " + str(nl_count) + " on column " + str(pointer_count))

                exit()
    return token_string



# Syntax Analyser... This function analyses the correctness of the program in terms of the syntax
def syntax_analyser(token_string, new_line):
    # The rules
    rules = Consts.rules

    # Parse Table
    parse_table = Consts.parse_table

    token_string += "$"

    # Stack that is used for parsing

    stack = ['$', '0']

    # Parsing happens here

    ip = 0
    while True:
        print("token -> ", token_string[ip], "-> ", end="")
        print(stack)
        pivot = parse_table[stack[-1]][token_string[ip]]

        if pivot[0] == 'S':
            stack.append(token_string[ip])
            ip += 1
            stack.append(pivot[1:])
            continue
        elif pivot[0] == 'R':
            rule = rules[int(pivot[1:])]
            for _ in range(2*len(rule[1])):
                stack.pop()
            stack.append(rule[0])
            new_pivot = parse_table[stack[-2]][stack[-1]]
            if new_pivot != 'E':
                stack.append(new_pivot)
                continue
            else:
                break
        elif pivot[0] == 'A':
            print("Parsing Completed Successfully!!!\n No errors")
            exit()
        else:
            break
    line_count = 1
    for _ in range(ip):
        if token_string[_] == new_line:
            line_count += 1
    print("Parser: Error in line " + str(line_count))



# Main function
def main():
    file = open("question.txt", "r")
    program_string = file.read()
    print("\nProgram:\n")
    print(program_string)
    print("\nLexical Analysis:\n")
    lexical_analyser()
    print("\nTokens Generated:\n")
    # Tokenizing
    token_string = tokenizer(program_string)
    print(token_string)
    print("\n")

    print("(Mapping of tokens can be found in ourrules.py file)")
    print("\n\n")
    # Parsing
    syntax_analyser(token_string, Consts.tokens['\n'])


# Call to main() function
try:
    main()
except Exception as e:
    print("Compiler: Unknown compiler time Exception occured...")
