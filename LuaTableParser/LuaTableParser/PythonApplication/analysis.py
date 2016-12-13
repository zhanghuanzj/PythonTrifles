f = open("case2.txt")
lines = f.readlines()
of = open("HAHA2.txt",'w')
for line in lines:
    count = int(line)-1
    if count>=727 :
        count -= 1
    if count>=792 :
        count -= 1
    c = (count - 662)/2
    if c == 0:
        of.write(' ')
    elif c == 1 :
        of.write('!')
    elif c == 2:
        of.write('"')
    elif c == 3:
        of.write('#')
    elif c == 4:
        of.write('$')
    elif c == 5:
        of.write('%')
    elif c == 6:
        of.write('&')
    elif c == 7:
        of.write('\'')
    elif c == 8:
        of.write('(')
    elif c == 9:
        of.write(')')
    elif c == 10:
        of.write('*')
    elif c == 11:
        of.write('+')
    elif c == 12:
        of.write(',')
    elif c == 13:
        of.write('-')
    elif c == 14:
        of.write('.')
    elif c == 15:
        of.write('/')
    elif c == 16:
        of.write('0')
    elif c == 17:
        of.write('1')
    elif c == 18:
        of.write('2')
    elif c == 19:
        of.write('3')
    elif c == 20:
        of.write('4')
    elif c == 21:
        of.write('5')
    elif c == 22:
        of.write('6')
    elif c == 23:
        of.write('7')
    elif c == 24:
        of.write('8')
    elif c == 25:
        of.write('9')
    elif c == 26:
        of.write(':')
    elif c == 27:
        of.write(';')
    elif c == 28:
        of.write('<')
    elif c == 29:
        of.write('=')
    elif c == 30:
        of.write('>')
    elif c == 31:
        of.write('?')
            
    elif c == 32:
        of.write('@')
    elif c == 33:
        of.write('A')
    elif c == 34:
        of.write('B')
    elif c == 35:
        of.write('C')
    elif c == 36:
        of.write('D')
    elif c == 37:
        of.write('E')
    elif c == 38:
        of.write('F')
    elif c == 39:
        of.write('G')
    elif c == 40:
        of.write('H')
    elif c == 41:
        of.write('I')
    elif c == 42:
        of.write('J')
    elif c == 43:
        of.write('K')
    elif c == 44:
        of.write('L')
    elif c == 45:
        of.write('M')
    elif c == 46:
        of.write('N')
    elif c == 47:
        of.write('O')
    elif c == 48:
        of.write('P')
    elif c == 49:
        of.write('Q')
    elif c == 50:
        of.write('R')
    elif c == 51:
        of.write('S')
    elif c == 52:
        of.write('T')
    elif c == 53:
        of.write('U')
    elif c == 54:
        of.write('V')
    elif c == 55:
        of.write('W')
    elif c == 56:
        of.write('X')
    elif c == 57:
        of.write('Y')
    elif c == 58:
        of.write('Z')
    elif c == 59:
        of.write('[')
    elif c == 60:
        of.write('/')
    elif c == 61:
        of.write(']')
    elif c == 62:
        of.write('^')
    elif c == 63:
        of.write('_')

    elif c == 64:
        of.write('`')
    elif c == 65:
        of.write('a')
    elif c == 66:
        of.write('b')
    elif c == 67:
        of.write('c')
    elif c == 68:
        of.write('d')
    elif c == 69:
        of.write('e')
    elif c == 70:
        of.write('f')
    elif c == 71:
        of.write('g')
    elif c == 72:
        of.write('h')
    elif c == 73:
        of.write('i')
    elif c == 74:
        of.write('j')
    elif c == 75:
        of.write('k')
    elif c == 76:
        of.write('l')
    elif c == 77:
        of.write('m')
    elif c == 78:
        of.write('n')
    elif c == 79:
        of.write('o')
    elif c == 80:
        of.write('p')
    elif c == 81:
        of.write('q')
    elif c == 82:
        of.write('r')
    elif c == 83:
        of.write('s')
    elif c == 84:
        of.write('t')
    elif c == 85:
        of.write('u')
    elif c == 86:
        of.write('v')
    elif c == 87:
        of.write('w')
    elif c == 88:
        of.write('x')
    elif c == 89:
        of.write('y')
    elif c == 90:
        of.write('z')
    elif c == 91:
        of.write('{')
    elif c == 92:
        of.write('|')
    elif c == 93:
        of.write('}')
    elif c == 94:
        of.write('~')
    elif c == 95:
        of.write('\n')
    elif c == 96:
        of.write('\t')
    elif c == 97:
        of.write('\a')
    elif c == 98:
        of.write('\b')
    elif c == 99:
        of.write('\f')
    elif c == 100:
        of.write('\r')
    elif c == 101:
        of.write('\\')
    else:
        pass
        #of.write('?')
of.close()
