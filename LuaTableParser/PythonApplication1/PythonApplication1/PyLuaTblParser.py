
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
        if self.is_empty():
            raise Exception('Table format wrong')
        else:
            return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

class PyLuaTblParser:

    def load(self,s):
        #print '-------------------------------------------------------------------'
        self.tableString = s.strip()
        #for v in s:
        #    self.tableString += v.strip()
        self.length = len(self.tableString)
        self.index = 0
        self.table = self.process()
        if self.index != self.length-1:
            raise Exception('Table format wrong')
    
    def dump(self):#dict key handling
        def dump_aux(value):
            result = '{'
            if type(value) == dict:
                for k,v in value.items():
                    if type(k) in (str,int,float):
                        if isinstance(k,str):
                            #if (k.find("'") != -1 and k.find(r"\'") == -1) and (k.find('"') != -1 and k.find(r'\"') == -1) :
                            #    k = '[' + k + ']'
                            #el
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
                    #print value.find(r'"')
                    #print value.find(r'\"') 
                    #print value.find(r"'") 
                    #print value.find(r"\'")
                    if (value.find("'") != -1) and (value.find('"') != -1 ) :
                        value = '[[' + value + ']]'
                    elif value.find("'") != -1 :
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
        #String Analysis
        def get_str(value,index):
            result = ''
            in_string = False
            has_esc = False
            quote = ''
            while True:
                if index >= self.length:
                    raise Exception('Table format wrong -- string analysis')
                c = value[index]
                index += 1
                if (c == '"' or c == "'") and not has_esc: #begin or end
                    if in_string:
                        if(c == quote):# end -- string analyse finish
                            return result,index
                    else:
                        in_string = True
                        quote = c
                        continue
                elif c == '\\' and not has_esc: #esc
                    has_esc = True
                else :
                    has_esc = False
                result += c
        # Name ,Bool and nil analysis
        def get_name(value,index):
            result = ''
            while True:
                c = value[index]
                
                if c.isalnum() or c == '_':
                    result += c
                else:
                    if result in ('and','break','do','else','elseif','end','for','function','goto','if','in',
                                'local','not','or','repeat','return','then','until','while'):
                        raise Exception('Table format wrong -- key words conflict')
                    if result == 'true':
                        return True,BOOL,index
                    elif result == 'false':
                        return False,BOOL,index
                    elif result == 'nil':
                        return None,NONE,index
                    else: # seprate character
                        return result,NAME,index
                index += 1

        def get_bracket_str(value,index):
            BEG,START,EQUAL,MID,END,NUMA = 0,1,2,3,4,5
            beg = index
            end = index
            pivot = 0
            state = BEG
            result = ''
            var = None
            while True:
                c = value[index]
                if state == BEG:
                    state = START
                elif state == START:
                    if c in ('"',"'"):
                        var = get_str(value,index)
                        index = var[1]
                        state = NUMA
                        continue
                    elif c.isdigit():
                        #num analysis
                        pass
                    elif c == '=':
                        state = EQUAL
                    else:
                        raise Exception('Table format wrong')
                elif state == EQUAL:
                    if c == '=':
                        state = EQUAL
                    elif c == '[':
                        state = MID
                    else:
                        raise Exception('Table format wrong')
                elif state == MID:
                    
         
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
                
                if len(value)>2 and ((value[1] =='[' and value[-2]==']') or (value[1] =='[' and value[-2]==']')):
                    return get_block_str(value[1:-1])
                else:
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
        
        val = r''
        val_stack = Stack()
        op_stack = Stack()
        map = {}
        array = []
        is_array = True
        is_first = True
        map_index = 1
        finish = False 
        while True:
            if self.index >= self.length:
                raise Exception('Table format wrong')
            if need_store:
                if val_stack.is_empty():
                    pass
                value = val_stack.peek()
                val_stack.pop()
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
                need_store = False 
            if finish:# Finish and check
                if (not val_stack.is_empty()) or (not op_stack.is_empty()) :
                    raise Exception('Table format wrong -- remaining val or op')
                if is_array or len(map)==0:
                    return array
                else:
                    return map               
            c = self.tableString[self.index] # Next character
            if c == '{' :
                if is_first:
                    is_first = False
                else :
                    item = self.process()
                    val_stack.push(item,EXP)   
                    need_store = True                
            elif c == '}':
                if not is_first:
                    if not val_stack.is_empty():
                        need_store = True
                    finish = True
                    continue
                else : #'{}'not match
                    raise Exception('Table format wrong')
            elif c == '=' :
                if is_array:
                    is_array = False
                    for v in array:
                        if v != None:
                            map[map_index] = v
                            map_index += 1
                op_stack.push('=')
            elif (c == ',' or c == ';') :
                need_store = True
            elif (c == '"' or c == "'"): # Get String
                v = get_str(self.tableString,self.index)
                val_stack.push(v[0],EXP)
                self.index = v[1]
                continue
            elif c.isalpha() or c == '_': # Get Name , bool , None
                v = get_name(self.tableString,self.index)
                val_stack.push(v[0],v[1])
                self.index = v[2]
                continue
            elif c in (' ','\n','\r','\t'): # Skip
                pass
            else :
                val = val + c
            self.index += 1

    

