from functools import cmp_to_key

def ccmp(elem1,elem2):
    if elem1[0]!=elem2[0]:
        return elem1[0]-elem2[0]
    return elem1[2]-elem2[2]

class NFA:

    def __init__(self,ch):
        self.head = 1
        self.tail = 2
        self.lines = [[1,ch,2]]

    def and_NFA(self,NFA_b):
        NFA_b.add_num(len(self)-1)
        for line in NFA_b.lines:
            self.lines.append(line)
        self.tail = NFA_b.tail

    def or_NFA(self,NFA_b):
        self.add_num(1)
        NFA_b.add_num(len(self)+1)
        for line in NFA_b.lines:
            self.lines.append(line)
        self.lines.append([1,'~',self.head])
        self.lines.append([1,'~',NFA_b.head])
        self.lines.append([self.tail,'~',NFA_b.tail+1])
        self.lines.append([NFA_b.tail,'~',NFA_b.tail+1])
        self.tail = NFA_b.tail+1
        self.head = 1

    def kleen_NFA(self):
        self.lines.append([self.head,'~',self.tail])
        self.lines.append([self.tail,'~',self.head])
        '''self.add_num(1)
        self.lines.append([1,'~',self.head])
        self.lines.append([self.tail,'~',self.tail+1])
        self.lines.append([self.tail,'~',self.head])
        self.lines.append([1,'~',self.tail+1])
        self.head = 1
        self.tail +=1'''

    def sort_NFA(self):
        self.lines.sort(key=cmp_to_key(ccmp))

    def show_NFA(self):
        self.sort_NFA()
        pre = ""
        cnt = 0
        for line in self.lines:
            now = line[0]
            if pre != now:
                if cnt != 0:
                    print("")
                cnt+=1
                if line[0]==self.head:
                    print("X",end="")
                elif line[0] == self.tail:
                    print("Y",end="")
                   # print(line[0]-2, end="")
                else:
                    print(line[0]-2, end="")
            pre = now
            if line[0]==self.head:
                print(str(" X-"+line[1]+"->"), end="")
            elif line[0]==self.tail:
                print(str(" Y-"+line[1]+"->"), end="")
            else:
                print(" "+str(line[0]-2)+"-"+line[1]+"->",end="")
            if line[2] == self.tail:
                print('Y', end="")
            elif line[2] == self.head:
                print('X', end="")
            else :
                print(line[2]-2, end="")
            

    def add_num(self, num):
        self.head+=num
        self.tail+=num
        for line in self.lines:
            line[0]+=num
            line[2]+=num

    def __len__(self):
        return self.tail-self.head+1

def calculate(ch,a,b):
    if ch == '.':
        a.and_NFA(b)
    elif ch == '|':
        a.or_NFA(b)
    elif ch == '*':
        a.kleen_NFA()
    return a

def parse(s):
    sign_stack = []
    nfa_stack = []
    for ch in s:
        if ch=='(':
            sign_stack.append(ch)
            
        elif ch == ')':
            while len(sign_stack) != 0 and sign_stack[-1] != '(':
                tmp = sign_stack[-1]
                sign_stack.pop()
                nfa_stack[-2] = calculate(tmp,nfa_stack[-2],nfa_stack[-1])
                nfa_stack.pop()
        elif ch == '*':
            nfa_stack[-1] = calculate(ch,nfa_stack[-1],None)
        elif ch == '|':
            while len(sign_stack) != 0 and sign_stack[-1] == '.':
                sign_stack.pop()
                nfa_stack[-2] = calculate('.',nfa_stack[-2],nfa_stack[-1])
                nfa_stack.pop()
            sign_stack.append(ch)
        elif ch == '.':
            sign_stack.append(ch)
        else :
            nfa_stack.append(NFA(ch))
    while len(nfa_stack)>1:
        ch = sign_stack[-1]
        sign_stack.pop()
        nfa_stack[-2] = calculate(ch,nfa_stack[-2],nfa_stack[-1])
        nfa_stack.pop()
    return nfa_stack[0]

def isCharacter(ch):
    if 'a'<=ch<='z' or '0'<=ch<='9' or 'A'<=ch<='Z':
        return True
    return False

def RegexToNFA(s):
    ret = s[0]
    for i in range(1,len(s)):
        pre = s[i-1]
        now = s[i]
        if isCharacter(pre) and isCharacter(now):
            ret +='.'
            ret += now
        elif isCharacter(pre) and now == '(':
            ret +='.'
            ret += now
        elif pre == ')' and isCharacter(now):
            ret +='.'
            ret += now
        elif pre == '*' and isCharacter(now):   
            ret +='.'
            ret += now
        elif pre == '*' and now == '(':
            ret +='.'
            ret += now
        else :
            ret += now
    return parse(ret)

if __name__ == "__main__":
    x = input()
    nfa = RegexToNFA(x)
    nfa.show_NFA()

