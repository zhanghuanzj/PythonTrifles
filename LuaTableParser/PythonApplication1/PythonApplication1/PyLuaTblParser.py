
NONE = "NONE"
BOOL = "BOOL" 
EXP = "EXP" #str | num
NAME = "NAME"
KEY = "KEY"
OTHER = "OTHER"

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
        #print '-------------------------------------------------------------------'
        self.tableString = s
        #for v in s:
        #    self.tableString += v.strip()
        self.length = len(self.tableString)
        self.index = 0
        self.table = self.process()
    
    def dump(self):#dict key handling
        def dump_aux(value):
            result = '{'
            if type(value) == dict:
                for k,v in value.items():
                    if type(k) in (str,int,float):
                        if isinstance(k,str):
                            if k.find("'") != -1 and k.find(r"\'") == -1 :
                                k = '"' + k + '"'
                            else:
                                k = "'" + k + "'"
                        result = result + '[' + str(k) + ']' + '=' + str(dump_aux(v)) + ','
            elif type(value) == list or type(value) == tuple:
                for v in value:
                    result += str(dump_aux(v)) + ','
            elif type(value) is bool:
                if value == True :
                    return 'true'
                elif value == False :
                    return 'false'
            elif value == None :
                return 'nil'
            else:
                if isinstance(value,str):
                    if value.find("'") != -1 and value.find(r"\'") == -1:
                        value = '"' + value + '"'
                    else:
                        value = "'" + value + "'"
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
                    if type(v) == tuple:
                        v = list(v)
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
        def get_block_str(value):
            if len(value)>1 and (value[0]=='=' and value[-1]=='='):
                return get_block_str(value[1,-1])
            elif len(value)>1 and (value[0]=='[' and value[-1]==']'):# ' " can all exist
                return value[1:-1],EXP
            else :
                raise Exception('Table format wrong')
        def get_val(value):
            value = value.strip()
            #print 'Handling :'+value
            if value == '' :
                return None,OTHER
            elif value == 'nil':
                return None,NONE
            elif value == 'false':
                return False,BOOL
            elif value == 'true':
                return True,BOOL
            elif len(value)>1 and ((value[0] =='"' and value[-1]=='"') or (value[0] =="'" and value[-1]=="'")):
                return value[1:-1],EXP
            elif value[0] =='[' and value[-1]==']':
                result = get_val(value[1:-1])
                if result[1] in (EXP,BOOL):
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
                    if value.find(' ') == -1:
                        return int(value),EXP
                    else :
                        return None,OTHER
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
        in_string = False 
        has_esc = 0
        while True:
            if self.index >= self.length:
                raise Exception('Table format wrong')
            if has_esc == 1:
                has_esc += 1
            if value != None:
                if value[1] == OTHER:
                    raise Exception('Table format wrong')  
                if op_stack.peek() == '=':
                    op_stack.pop()
                    key = val_stack.peek()
                    val_stack.pop()
                    if key == None or key[1]==NONE :
                        raise Exception('Table format wrong')
                    elif value[1] == NONE:
                        pass
                    else:
                        if (value[1]==EXP or value[1]==BOOL) and (key[1]==KEY or key[1]==NAME ):                            
                            map[key[0]] = value[0]
                            is_array = False
                        else :
                            raise Exception('Table format wrong')  
                else :
                    if is_array:
                        array.append(value[0])
                    elif value[1] != NONE :
                        map[map_index] = value[0]
                        map_index += 1  
                value = None 
                in_string = False
            if finish:
                if is_array or len(map)==0:
                    return array
                else:
                    return map               
            c = self.tableString[self.index]
            if c == '{' and not in_string :
                if is_first:
                    is_first = False
                else :
                    item = self.process()
                    value = (item,EXP)                   
            elif c == '}' and not in_string:
                if not is_first:
                    if val != '':
                        value = get_val(val)
                        val = ''
                    finish = True
                    continue
                else : #'{}'not match
                    raise Exception('Table format wrong')
            elif c == '=' and not in_string :
                if is_array:
                    is_array = False
                    for v in array:
                        if v != None:
                            map[map_index] = v
                            map_index += 1
                val_stack.push(get_val(val))
                op_stack.push('=')
                val = ''
            elif (c == ',' or c == ';') and not in_string:
                if val != '':
                    value = get_val(val)
                    val = ''
            elif (c == '"' or c == "'") and has_esc == 0: #not esc
                if in_string:
                    if(c == op_stack.peek()):# "" '' match
                        in_string = False
                        op_stack.pop()
                else:
                    in_string = True
                    op_stack.push(c)
                val = val + c
            elif c == '\\' and in_string and has_esc!=2: #esc
                has_esc = 1
                val = val + c
            elif (c in (' ','\n','\r','\t')) and not in_string and val == '':
                pass
            else :
                val = val + c
            self.index += 1
            if has_esc == 2:
                has_esc = 0
    

