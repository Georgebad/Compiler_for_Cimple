#Bantouvakis Georgios 4119, cse74119
#Tsapanidis Michail 4186, cse74186

import sys
import string

class Token:

    def __init__(self, tokenType , tokenString , lineNo):
        self.tokenType = tokenType
        self.tokenString = tokenString
        self.lineNo = lineNo

bound_words=['program','declare','if','else','while','switchcase','forcaase','incase','case','default','not','and','or',
             'function','procedure','call','return','in','inout','input','print']

letters=string.ascii_lowercase + string.ascii_uppercase 
numbers=[str(i) for i in list(range(0,9))]
symbols=['+','-','*','/']
operators=['<', '>', '=',':',';',',']
groupsymbols=['[',']','(',')','{','}']
lineNo=1
limit=(2**32 -1)
temp_value=0
programList=[[]]
programList.pop(0)
functions_procedures=[]
declarationss=[]
index=0
nextquad_number=0
name_check1=0
name_check2=0
secure=0
calling_check=0


file=open(sys.argv[1],'r')
string=sys.argv[1]
string=string.split('.')
out_int=string[0] + '.int'
out_c=string[0]+ '.c'
final_code=string[0]+ '.asm'

def getchar():
    char=file.read(1)
    return char

def lex():
    global tokenType
    global tokenString
    global lineNo
    global temp_value

    if temp_value == 0:
        char=getchar()    
    else:
        char=temp_value
        temp_value=0
    if char=='\n':
        lineNo +=1
        return lex()
    if char=='\t' or (char.isspace()==True):
        return lex()
    ########################################################### Comments
    elif char=='#':
        temp=getchar()
        while temp!='#':
            if temp=='\n':
                lineNo+=1
            elif temp is None:
                print("Program terminated without comments close at line:",lineNo)
                sys.exit()
            temp=getchar()
        return lex()
    ########################################################## Letters
    elif char in letters:
        ide=char
        temp=getchar()
        while temp in letters or temp in numbers:
            ide+=temp
            temp=getchar()
        if len(ide)>30:
            print("The identifier length is bigger than expected(30 charachters) at line:",lineNo)
            sys.exit()
        temp_value=temp
        tokenString=ide
        tokenType='keyword'
        return Token(tokenType,tokenString,lineNo)    
    ########################################################## Digits
    elif char in numbers:
        num=char
        temp=getchar()
        while temp in numbers:
            num+=temp
            temp=getchar()
        if int(num)<(-limit) or int(num)>limit:
            print("Error digit expected at line:",lineNo)
            sys.exit()
        temp_value=temp
        tokenString=num
        tokenType='number'
        return (Token(tokenType,tokenString,lineNo))
    ########################################################## Symbols
    elif char in symbols:
        if char =='+' or char=='-':
            tokenString=char
            tokenType='addOperator'
        if char == '*' or char=='/':
            tokenString=char
            tokenType='mulOperator'
        return (Token(tokenType,tokenString,lineNo))
    ########################################################## Operators
    elif char in operators:
        if char==',' or char==';':
            tokenString=char
            tokenType='delimiter'
        if char==':':
            temp=getchar()
            if temp=='=':
                tokenString=':='
                tokenType='assignment'
            elif temp != '=':
                print("Expecting = for assignment but instead",getchar(),"given at line:",lineNo)
                temp_value=temp
                sys.exit()
        if char=='<':
            realOp=char
            temp=getchar()
            if temp=='>' or temp=='=':
                realOp+=temp
            else:
                temp_value=temp    
            tokenString=realOp
            tokenType='realOperator'      
        if char=='>':
            realOp=char
            temp=getchar()
            if temp=='=':
                realOp+=temp
            else:
                temp_value=temp
            tokenString=char
            tokenType='realOperator'    
        if char=='=':
            tokenString=char
            tokenType='realOperator'
        return (Token(tokenType,tokenString,lineNo))
    ######################################################### GroupSymbols
    elif char in groupsymbols:
        tokenString=char
        tokenType='groupSymbol'
        return (Token(tokenType,tokenString,lineNo))
    ######################################################### Terminal 
    elif char=='.':
        tokenString=char
        tokenType='terminal'
        return (Token(tokenType,tokenString,lineNo))
    else:
        print("Unknown error at line:",lineNo)
        sys.exit()

def program():
    global token,name
    token=lex()
    if token.tokenString == 'program':
        token=lex()
        name=token.tokenString
        ID()
        block()
        genquad("halt","_","_","_")
        genquad("end_block",name,"_","_")
        token=lex()
        if token.tokenString !='.':
            print("'.'expected to terminate the program")
            sys.exit()
    else:
        print("the keyword 'program' expected at line:",token.lineNo)
        sys.exit()
        
def block():
    global token,name
    declarations()
    subprograms()
    genquad("begin_block",name,"_","_")
    statements()

def declarations():
    global token
    token=lex()
    if token.tokenString == 'declare':
        varlist()
        if token.tokenString !=';':
           print("';' expected at line:",token.lineNo)
           sys.exit()
        else:
            declarations() 

def varlist():
    global token
    token=lex()
    ID()
    declarationss.append(token.tokenString)
    token=lex()
    if token.tokenString == ',':
        varlist()

def subprograms():
    global token
    subprogram()
    while subprogram == 1:
        token=lex()    

def subprogram():
    global token,functions_procedures
    if token.tokenString == 'function':
        secure=1
        token=lex()
        id_=token.tokenString
        genquad("begin_block",id_,"_","_")
        functions_procedures.append(token.tokenString)
        ID()
        token=lex()
        if token.tokenString == '(':
            formalparlist()
            if token.tokenString==')':
                block()
                genquad("end_block",id_,"_","_")
                token=lex()
                return 1
            else:
                print("')' expected at line:",token.lineNo)
                sys.exit()
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
    elif token.tokenString == 'procedure':
        secure=1
        token=lex()
        id_=token.tokenString
        genquad("begin_block",id_,"_","_")
        functions_procedures.append(token.tokenString)
        ID()
        token=lex()
        if token.tokenString == '(':
            formalparlist()
            if token.tokenString==')':
                block()
                genquad("end_block",id_,"_","_")
                token=lex()
                return 1
            else:
                print("')' expected at line:",token.lineNo)
                sys.exit()
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
    else:
        return 0

def formalparlist():
    global token
    formalparitem()
    token=lex()
    while token.tokenString == ',':
        formalparitem()
        token=lex()

def formalparitem():
    global token,calling_check
    token=lex()
    if token.tokenString =='in':
        token=lex()
        if calling_check==1:
            genquad('par',token.tokenString,'CV','_')
            calling_check=0
        ID()
    elif token.tokenString == 'inout':
        token=lex()
        if calling_check==1:
            genquad('par',token.tokenString,'REF','_')
            calling_check=0
        ID()
    else:
        print("in or inout expected at line:",token.lineNo)
        sys.exit()

def statements():
    global token
    if token.tokenString != '{':
        statement()
        if token.tokenString != ';':
            print("';' expected at line:",token.lineNo)
            sys.exit()
    elif token.tokenString == '{':
        token=lex()
        if statement() ==False:
            print("Statement expected at line:",token.lineNo) 
            sys.exit()
        temp=token.tokenString
        token=lex()
        while(statement()==True): 
            if token.tokenString !=';' or temp!=';':
                print("'; ' expected at line:",token.lineNo,'instead of:',"'",token.tokenString,"'") 
                sys.exit()
            else:
                token=lex()
                      
        if token.tokenString != '}':
            print("'}' expected at line:",token.lineNo) 
            sys.exit()

def statement():
    global token
    if ifStat()==True:
        return True
    elif whileStat()==True:
        return True
    elif switchcaseStat()==True:
        return True
    elif forcaseStat()==True:
        return True
    elif incaseStat()==True:
        return True
    elif callStat()==True:
        return True
    elif returnStat()==True:
        return True
    elif inputStat()==True:
        return True
    elif printStat()==True:
        return True
    elif assignStat()==True:
        return True
    else:
        return False
    
def assignStat():
    global token
    if token.tokenString != '}':
        ID()
        id_=token.tokenString
        token=lex()
        if token.tokenType =='assignment':
            token=lex()
            expression()
            genquad(":=",E,"_",id_)
            return True
        else:
            return False
    else:
        return False
     
def ifStat():
    global token
    if token.tokenString == 'if':
        token=lex()
        if token.tokenString == '(':
            condition()
            if token.tokenString == ')':
                #backpatch(Btrue,nextquad())
                token=lex()
                statements()
                #ifList=makelist(nextquad())
                genquad("jump","_","_","_")
                #backpatch(Bfalse,nextquad())
                token=lex()
                elsepart()
                #backpatch(ifList,nextquad())
            else:
                print("')' expected at line:",token.lineNo)
                sys.exit()
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
        return True
    else:
        return False
        
def elsepart():
    global token
    if token.tokenString == 'else':
        token=lex()
        statements()

def whileStat():
    global token,rtrue,rfalse,nextquad_number
    if token.tokenString == 'while':
        token=lex()
        Bquad=nextquad()
        nextquad_number-=1
        if token.tokenString == '(':
            condition()
            if token.tokenString == ')':
                #backpatch(Btrue,nextquad())
                token=lex()
                statements()
                token=lex()
                genquad("jump","_","_",Bquad)
                #backpatch(Bfalse,nextquad())
            else:
                print("')' expected at line:",token.lineNo)
                sys.exit()
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
        return True
    else:
        return False

def switchcaseStat():
    global token,secure
    if token.tokenString == 'switchcase':
        secure=1
        #exitlist=emptylist()
        token=lex()
        while token.tokenString == 'case':
            token=lex()
            if token.tokenString == '(':
                condition()
                if token.tokenString == ')':
                    #backpatch(rtrue,nextquad())
                    token=lex()
                    statements()
                    token=lex()
                    #e=makelist(nextquad())
                    genquad('jump','_','_','_')
                    #mergelist(exitlist,e)
                    #backpatch(rfalse,nextquad())
                else:
                    print("')' expected at line:",token.lineNo)    
                    sys.exit()
            else:
                print("'(' expected at line:",token.lineNo)   
                sys.exit() 
        if token.tokenString == 'default':
            token=lex()
            if token.tokenString == ';':
                token=lex()
                if token.tokenString != ';':
                    print("';' expected at line:",token.lineNo)  
                    sys.exit()  
            else:
                statements()
            #backpatch(exitlist,nextquad())
        else:
            print("'default' expected at line:",token.lineNo)
            sys.exit()
        return True
    else:
        return False 

def forcaseStat():
    global token,secure
    if token.tokenString == 'forcase':
        secure=1
        #exitlist=emptylist()
        token=lex()
        while(token.tokenString=='case'):
            token=lex()
            if token.tokenString == '(':
                condition()
                if token.tokenString == ')':
                    #backpatch(rtrue,nextquad())
                    token=lex()
                    statements()
                    token=lex()
                    #e=makelist(nextquad())
                    genquad('jump','_','_','_')
                    #mergelist(exitlist,e)
                    #backpatch(rfalse,nextquad())
                else:
                    print("')' expected at line:",token.lineNo)  
                    sys.exit()   
            else:
                print("'(' expected at line:",token.lineNo)  
                sys.exit() 
        if token.tokenString == 'default':
            token=lex()
            if token.tokenString == ';':
                token=lex()
                if token.tokenString != ';':
                    print("';' expected at line:",token.lineNo)  
                    sys.exit()  
            else:
                statements()
            #backpatch(exitlist,nextquad())
        else:
            print("'default' expected at line:",token.lineNo)
            sys.exit() 
        return True
    else:
        return False

def incaseStat():
    global token,secure
    if token.tokenString == 'incase':
        secure=1
        #exitlist=emptylist()
        token=lex()
        while token.tokenString == 'case':
            token=lex()
            if token.tokenString == '(':
                condition()
                if token.tokenString == ')':
                    #backpatch(rtrue,nextquad())
                    token=lex()
                    statements()
                    token=lex()
                    #e=makelist(nextquad())
                    genquad('jump','_','_','_')
                    #mergelist(exitlist,e)
                    #backpatch(rfalse,nextquad())
                else:
                    print("')' expected at line:",token.lineNo)
                    sys.exit()     
            else:
                print("'(' expected at line:",token.lineNo)
                sys.exit()
        if token.tokenString == 'default':
            token=lex()
            if token.tokenString == ';':
                token=lex()
                if token.tokenString != ';':
                    print("';' expected at line:",token.lineNo)  
                    sys.exit()  
            else:
                statements()
            #backpatch(exitlist,nextquad())
        else:
            print("'default' expected at line:",token.lineNo)
            sys.exit() 
        return True
    else:
        return False     

def returnStat():
    global token
    if token.tokenString == 'return':
        token=lex()
        if token.tokenString == '(':
            token=lex()
            expression()
            if token.tokenString != ')':
                print("')' expected at line: edw?",token.lineNo)
                sys.exit() 
            else:
                genquad("retv",E,"_","_")
                token=lex()
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
        return True
    else:
        return False  

def callStat():
    global token
    if token.tokenString == 'call':
        token=lex()
        ID()
        temp_name=token.tokenString
        token=lex()
        if token.tokenString == '(':
            actualparlist()
            token=lex()
            genquad('call',temp_name,'_','_')
            if token.tokenString != ')':
                print("')' expected at line:",token.lineNo)
                sys.exit() 
        else:
           print("'(' expected at line:",token.lineNo)
           sys.exit()
        return True
    else:
        return False 

def printStat():
    global token
    if token.tokenString == 'print':
        token=lex()
        if token.tokenString == '(':
            token=lex()
            expression()
            if token.tokenString != ')':
                print("')' expected at line:",token.lineNo)
                sys.exit()
            else:
                genquad("out",E,"_","_")
                token=lex() 
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
        return True
    else:
        return False 

def inputStat():
    global token
    if token.tokenString == 'input':
        token=lex()
        if token.tokenString == '(':
            token=lex()
            id_=token.tokenString
            ID()
            token=lex()
            if token.tokenString != ')':
                print("')' expected at line:",token.lineNo)
                sys.exit()
            else:
                genquad("inp",id_,"_","_")
                token=lex()     
        else:
            print("'(' expected at line:",token.lineNo)
            sys.exit()
        return True
    else:
        return False 

def actualparlist():
    global token
    actualparitem()
    token=lex()
    while token.tokenString == ',':
        actualparitem()
        token=lex()

def actualparitem():
    global token
    token=lex()
    if token.tokenString == 'in':
        expression()
        genquad("par",E,'CV','_')
    elif token.tokenString == 'inout':
        token=lex()
        ID()
        genquad("par",token.tokenString,'CV','_')
    else:
        print(" in or inout expected at line:",token.lineNo)
        sys.exit() 

def condition():
    global token,Qtrue,Qfalse,Btrue,Bfalse
    boolterm()
    btrue=Qtrue
    bfalse=Qfalse
    while token.tokenString == 'or':
        boolterm()
        btrue=merge(btrue,Qtrue)
        bfalse=Qfalse
    Btrue=btrue
    Bfalse=bfalse

def boolterm():
    global token,rtrue,rfalse,Qtrue,Qfalse
    boolfactor()
    qtrue=rtrue
    qfalse=rfalse
    while token.tokenString == 'and':
        boolfactor()
        qfalse=merge(qfalse,rfalse)
        qtrue=rtrue
    Qtrue=qtrue
    Qfalse=qfalse
        
def boolfactor():
    global token,rtrue,rfalse,nextquad_number
    token=lex()
    rtrue=[]
    rfalse=[]
    if token.tokenString== 'not':
        token=lex()
        if token.tokenString == '[':
            condition()
            rtrue=Bfalse
            rfalse=Btrue
            if token.tokenString != ']':
                print("']' expected at line:",token.lineNo) 
                sys.exit()
        else:
            print("'[' expected at line:",token.lineNo) 
            sys.exit()  
    elif token.tokenString == '[':
        condition()
        if token.tokenString != ']':
            print("']' expected at line:",token.lineNo)
            sys.exit()  
    else:
        expression()
        e1=E
        REL_OP()
        relop=token.tokenString
        token=lex()
        expression() 
        e2=E 
        genquad(relop,e1,e2,"_")
        genquad("jump","_","_","_")

        rtrue=programList[-2:-1]
        rfalse.append(["jump",'_','_','_'])
        
def expression():
    global token,E,R
    add_checker=0
    optionalSign()
    term() 
    t1=R
    add_checker=ADD_OP()
    while add_checker==1:
        symbol=token.tokenString 
        token=lex()
        t2=token.tokenString 
        term()
        w=newtemp()
        genquad(symbol,t1,t2,w) 
        t1=w 
        if token.tokenString == ')' or token.tokenString==';':
            break
        if token.tokenString == ';':
            break
        token=lex()
        add_checker=ADD_OP()
    E=t1

def term():
    global token,E,R
    mul_checker=0
    f1=token.tokenString 
    factor()
    mul_checker=MUL_OP()
    while mul_checker == 1:
        symbol=token.tokenString 
        token=lex()
        f2=token.tokenString 
        factor()
        w=newtemp() 
        genquad(symbol,f1,f2,w) 
        f1=w 
        if token.tokenString ==')'or token.tokenString ==';':
            break
        token=lex()
        mul_checker=MUL_OP()
    R=f1

def factor():
    global token,calling_check
    int_checker=INTEGER()
    if int_checker==1:
        token=lex()
    elif token.tokenString == '(':
        token=lex()
        expression()
        if token.tokenString!=')':
            print("')' expected at line:",token.lineNo)
            sys.exit() 
    else:
        if token.tokenString in functions_procedures:
            temp_name=token.tokenString
            token=lex()
            if token.tokenString == '(':
                calling_check=1
                formalparlist()
                if token.tokenString==')':
                    w=newtemp()
                    genquad('par',w,'RET','_')
                    genquad('call',temp_name,'_','_')
                    token=lex()
                else:
                    print("')' expected at line:",token.lineNo)
                    sys.exit()
            else:
                print("'(' expected at line:",token.lineNo)
                sys.exit()
        else:
            ID()
            idtail()
        
def idtail():
    global token
    token=lex()
    if token.tokenString == '(':
        actualparlist()
        if token.tokenString != ')':
            print("')' expected at line:",token.lineNo)
            sys.exit() 
        else:
            token=lex()

def optionalSign():
    global token
    if ADD_OP()==1:
        token=lex()

def REL_OP():
    global token
    if token.tokenString == '=' or token.tokenString =='<=' or token.tokenString =='>='or token.tokenString =='>' or token.tokenString =='<' or token.tokenString =='<>':
        return 1

def ADD_OP():
    global token
    if token.tokenString == '+' or token.tokenString =='-':
        return 1
     
def MUL_OP():
    global token
    if token.tokenString == '*' or token.tokenString =='/':
        return 1

def INTEGER():
    global token
    if token.tokenType=='number':
        return 1

def ID():
    global token
    if token.tokenType != 'keyword':
        print("keyword expected at line:",token.lineNo,"instead of ","'",token.tokenString,"'")
        sys.exit() 
    elif token.tokenString in bound_words:
        print("the word ",token.tokenString,"is identifier and it cant be used at line:",token.lineNo)
        sys.exit() 

def nextquad():
    global nextquad_number
    nextquad_number+=1
    return nextquad_number

def genquad(op,x,y,z):
    programList.append([nextquad(),op,x,y,z])

def newtemp(): 
    global index 
    index+=1
    return (str("T_"+str(index)))

def emptylist():
    elist=[[]]
    elist.pop(0)
    return elist

def makelist(x):
    new_list=emptylist()
    new_list.append(x)
    return new_list

def merge(list1,list2):
    m_list=emptylist()
    m_list.append(list1)
    m_list.append(list1)
    return m_list

def backpatch(mylist,z):
    for i in mylist:
        i[3]=str(z)

def create_c():
    global secure
    integers=[]
    if secure==0:
        f_out_c=open(out_c,'w')
        f_out_c.write("int main(){\n")
        f_out_c.write('\tint ')
        commas=len(declarationss)
        for i in declarationss:
            if commas>1:
                f_out_c.write(i +',')
            else:
                if index == 0:
                    f_out_c.write(i)
                else:
                    f_out_c.write(i+',')
            commas-=1
        for i in range(index):
            if i==index:
                f_out_c.write(str("T_"+str(i)))
            else:
                f_out_c.write(str("T_"+str(i)) + ',')
        f_out_c.write(';'+'\n')
        for i in programList:
            l='L_'+ str(i[0]) +': '
            exp=' '
            comment='('
            if i[1]== ':=':
                if i[3] == '_':
                    integers.append(i[4])
                    exp = i[4] + ' = ' + i[2]
                else:
                    exp='if(' + i[2] + i[1] + i[3] + ") goto " + i[4]
            elif i[1] in symbols:
                exp = i[4] + ' = ' + i[2] + i[1] + i[3]
            elif i[1]=='<' or i[1]=='<=' or i[1]=='<>' or i[1]=='>=' or i[1]=='>':
                exp = 'if(' + i[2] + i[1] + i[3] + ") goto " + i[4]
            elif i[1]=='jump':
                exp = 'goto' + ' L_'+str(i[4])
            elif i[1]=='out':
                exp='printf ("%d",' + i[2] +')'
            elif i[1]=='RETV':
                exp='return ("%d",' + i[2] +')'
            elif i[1]=='inp':
                exp='scanf ("%d",&' + i[2] +')'
            elif i[1]=='halt':
                f_out_c.write('\t' + l + '{}\n')
            for j in i:
                comment+= str(j) + " ,"
            if exp!=' ':
                comments=comment[:-1]
                comments+=")"
                line= '\t' + l + exp + ';' + "\t//" + comments
                f_out_c.write(line)
                f_out_c.write('\n')
        f_out_c.write('}')
        f_out_c.close()

        
program()
create_c()
#print result at the .int file 
f_out_int=open(out_int,'w')
for i in programList:
    check=len(i)
    for j in i:
        check-=1
        f_out_int.write(str(j))
        if check!=0:
            f_out_int.write(" ")
    f_out_int.write("\n")
f_out_int.close()

##Create the final code
relops=['=','<=','>=','>','<','<>']
fint=open(out_int,'r')
f_open_int=open(final_code,'w')
while(1):
    line=fint.readline()
    if not line:
        break
    line=line[:-1]
    line=line.split(' ')
    #jump
    if line[1]=='jump':
        temp_line='\tb '+line[4]+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    #relop
    elif line[1] in relops:
        if line[1]=='=':
            branch='beq'
        elif line[1]=='<':
            branch='blt'
        elif line[1]=='>':
            branch='bgt'
        elif line[1]=='<=':
            branch='ble'
        elif line[1]=='>=':
            branch='bge'
        else:
            branch='bne'
        temp_line='\tloadvr('+line[2]+',$t1)\n\tloadvr('+line[2]+',$t2)\n\t'+branch+',$t1,$t2,'+line[4]+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line) 
    #assignments
    elif line[1]==':=':
        temp_line='\tloadvr('+line[2]+', $t1)\n\tstorerv($t1,'+line[4]+')'+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    #symbols
    elif line[1] in symbols:
        if line[1]=='+':
            op='add'
        elif line[1]=='-':
            op='sub'
        elif line[1]=='*':
            op='mul'
        elif line[1]=='/':
            op='div'
        temp_line='\tloadvr('+line[2]+', $t1)\n\tloadvr(,'+line[3]+',$t2)\n\t'+op+'$t1,$t1,$t2\nstorerv($t1,'+line[4]+')'+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    #out
    elif line[1]=='out':
        temp_line='\tli $v0,1\n\tloadvr('+line[4]+',$a0)\n\tsyscall'+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    #in
    elif line[1]=='in':
        temp_line='\tli $v0,5\n\tsyscall\n\tstorerv($v0,'+line[4]+')'+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    #retv
    elif line[1]=='retv':
        temp_line='\tloadvr('+line[4]+', $t1)\n\tlw $t0,-8($sp)\n\tsw $t1,($t0)'+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    #par
    elif line[1]=='par':
        if line[3]=='CV':
            temp_line='\tloadvr('+line[2]+', $t0)\n\tsw $t0, -(12+4i)($fp)'+'\n'
            number='L'+line[0]+':'+'\n'
            f_open_int.write(number)
            f_open_int.write(temp_line)
        elif line[3]=='REF':
            temp_line='\tgnlvcode('+line[2]+')\n\tlw $t0,($t0)\n\tsw $t0,-(12+4i)($fp)'+'\n'
            number='L'+line[0]+':'+'\n'
            f_open_int.write(number)
            f_open_int.write(temp_line)
        else:
            temp_line='\taddi $t0,$sp,-offset\n\tsw $t0,-8($fp)'+'\n'
            number='L'+line[0]+':'+'\n'
            f_open_int.write(number)
            f_open_int.write(temp_line)
    #call
    elif line[1]=='call':
        temp_line='\tlw $t0,-4($sp)\n\tsw $t0,-4($fp)'+'\n'
        number='L'+line[0]+':'+'\n'
        f_open_int.write(number)
        f_open_int.write(temp_line)
    else:
        continue
fint.close()
f_open_int.close()