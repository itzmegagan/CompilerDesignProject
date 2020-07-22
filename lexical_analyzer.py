import os

keywords=['int','main','begin','for','to','do','if','endif','endfor','return','End']
operators=['(',')','[',']','=','-','>']
w=""

if os.stat("ques").st_size==0 :
    print("File is empty")
else:
    with open('ques','r') as f:
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
