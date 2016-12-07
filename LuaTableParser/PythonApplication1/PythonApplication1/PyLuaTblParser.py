
NONE = 0
BOOL = 1 
EXP = 2 #str | num
NAME = 3
KEY = 4
OTHER = 5

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items)==0

    def push(self,item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

class PyLuaTblParser:

    def load(self,s):
        print '-------------------------------------------------------------------'
        print s
        self.tableString = s
        self.length = len(self.tableString)
        self.index = 0
        self.table = self.process()
    
    def dump(self):#dict key handling
        def dump_aux(value):
            result = '{'
            if type(value) == dict:
                for k,v in value.items():
                    if isinstance(k,str):
                        k = '"' + k + '"'
                    result = result + '[' + str(k) + ']' + '=' + str(dump_aux(v)) + ','
            elif type(value) == list:
                for v in value:
                    result += str(dump_aux(v)) + ','
            elif value == True :
                return 'true'
            elif value == False :
                return 'false'
            elif value == None :
                return 'nil'
            else:
                if isinstance(value,str):
                    value = '"' + value + '"'
                return value
            result += '}'
            return result
        return dump_aux(self.table)
    
    def loadLuaTable(self, f):
        try :
            tableString = ''
            table_file = open(f)
            lines = table_file.readlines()
            for line in lines:
                tableString += line.strip()
            self.load(tableString)
        except IOError,e:
            print e
    def dumpLuaTable(self, f):
        try :
            table_file = open(f,'w')
            table_file.write(self.dump())
            table_file.close()
        except IOError,e:
            print e
    
    def loadDict(self,d):
        self.table = self.acquire(d)
          
    def dumpDict(self):
        return self.acquire(self.table)  

    def acquire(self,d):
        result = None
        if type(d) == dict:
            result = {}
            for k,v in d.items():
                if str(k).isdigit or isinstance(k,str) and v != None: #Check key&value is valid
                    if type(v) == dict or type(v) == list:
                        v = self.acquire(v)
                    result[k] = v
        if type(d) == list:
            result = []
            for v in d:
                if type(v) == dict or type(v) == list:
                    v = self.acquire(v)
                result.append(v)
        return result
    
    def process(self):
        def get_val(value):
            print 'Handling :'+value
            if value == '':
                return None,OTHER
            elif value == 'nil':
                return None,NONE
            elif value == 'false':
                return False,BOOL
            elif value == 'true':
                return True,BOOL
            elif len(value)>1 and value[0] =='"' and value[-1]=='"':
                return value[1:-1],EXP
            elif value[0] =='[' and value[-1]==']':
                result = get_val(value[1:-1])
                if result[1] == EXP:
                    return result[0],KEY
                else :
                    return None,OTHER
            elif value[0].isalpha() or value[0]== '_': 
                for c in value:
                    if c.isalnum() or c == '_':
                        pass
                    else :
                        return None,OTHER
                return value,NAME
            else:
                try:
                    return int(value),EXP
                except ValueError:
                    return float(value),EXP
                except Exception:
                    return None,OTHER
        
        val = ''
        val_stack = Stack()
        op_stack = Stack()
        map = {}
        array = []
        is_array = True
        is_first = True
        map_index = 1
        value = None
        finish = False
        while True:
            if self.index >= self.length:
                raise Exception('Table format wrong')
            if value != None:
                if op_stack.peek() == '=':
                    op_stack.pop()
                    key = val_stack.peek()
                    val_stack.pop()
                    if key == None or key[1]==NONE :
                        raise Exception('Table format wrong')
                    elif value[1] == NONE:
                        pass
                    else:
                        if value[1]==EXP and (key[1]==KEY or key[1]==NAME ):                            
                            map[key[0]] = value[0]
                            is_array = False
                        else :
                            raise Exception('Table format wrong')  
                else :
                    if is_array:
                        array.append(value[0])
                    elif value[1] != None :
                        map[map_index] = value[0]
                        map_index += 1  
                value = None 
            if finish:
                if is_array or len(map)==0:
                    return array
                else:
                    return map               
            c = self.tableString[self.index]
            if c == '{' :
                if is_first:
                    is_first = False
                else :
                    item = self.process()
                    value = (item,EXP)                   
            elif c == '}' and (val=='' or get_val(val)[1] != OTHER):#wrong
                if not is_first:
                    if val != '':
                        value = get_val(val)
                        val = ''
                        finish = True
                        continue
                else : #'{}'not match
                    raise Exception('Table format wrong')
            elif c == '=':
                if is_array:
                    is_array = False
                    for v in array:
                        if v != None:
                            map[map_index] = v
                            map_index += 1
                val_stack.push(get_val(val))
                op_stack.push('=')
                val = ''
            elif c == ',' or c == ';':
                if val != '':
                    value = get_val(val)
                    val = ''
            elif c == ' ':
                pass
            elif c != ' ':
                val = val + c
            self.index += 1
    

