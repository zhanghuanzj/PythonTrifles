
NONE = "NONE"
BOOL = "BOOL" 
EXP = "EXP" #str | num
NAME = "NAME"
KEY = "KEY"

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
        #self.tableString = self.remove_comment(s)
        self.tableString = s.strip()
        #if self.tableString[0] != '{':
        #    raise Exception('Table format wrong')
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
                            if (k.find("'") != -1 ) and (k.find('"') != -1) :
                                k = '[' + k + ']'
                            elif k.find("'") != -1:
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
            table_file = open(f)
            tableString = table_file.read()
            self.load(tableString)
            table_file.close()
        except IOError,e:
            raise IOError
    def dumpLuaTable(self, f):
        try :
            table_file = open(f,'w')
            table_file.write(self.dump())
            table_file.close()
        except IOError,e:
            raise IOError
    
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
        
    #def remove_comment(self,value):
    #    while True:
    #        length = len(value)
    #        index = value.find('--')
    #        if index == -1:
    #            return value.strip()
    #        else:
    #            beg = index + 2
    #            end,index = beg,beg
    #            BEG,START,MID,END,LINE = 0,1,2,3,4
    #            pivot = 0
    #            state = BEG
    #            while True:
    #                if index >= length:
    #                    raise Exception('Table format wrong')
    #                c = value[index]
    #                if state == BEG:
    #                    if c == '[':
    #                        state = START
    #                    else :
    #                        state = LINE
    #                elif state == START:
    #                    if c == '=':
    #                        pass
    #                    elif c == '[':
    #                        end = index
    #                        state = MID
    #                    else:
    #                        state = LINE
    #                elif state == MID:
    #                    if c == ']':
    #                        state = END
    #                        pivot = end
    #                        continue
    #                elif state == END:
    #                    if (value[pivot] == c and c == '=') or (value[pivot] == '[' and c == ']'):# match finish
    #                        if pivot == beg: #comment match over
    #                            value = value[:beg-2]+value[index+1:]
    #                            break
    #                        pivot -= 1
    #                    else:   # back to END
    #                        state = MID
    #                elif state == LINE:
    #                    line_index = value.find('\n',beg-2)
    #                    if line_index == -1:
    #                        value = value[:beg-2]
    #                    else:
    #                        value = value[:beg-2] + value[line_index+1:]
    #                    break
    #                index += 1
    def process(self):
        def remove_comment(value,index):
            while True:
                length = len(value)
                if index == -1:
                    return value.strip()
                else:
                    beg = index + 2
                    end,index = beg,beg
                    BEG,START,MID,END,LINE = 0,1,2,3,4
                    pivot = 0
                    state = BEG
                    while True:
                        if index >= length:
                            raise Exception('Table format wrong')
                        c = value[index]
                        if state == BEG:
                            if c == '[':
                                state = START
                            else :
                                state = LINE
                        elif state == START:
                            if c == '=':
                                pass
                            elif c == '[':
                                end = index
                                state = MID
                            else:
                                state = LINE
                        elif state == MID:
                            if c == ']':
                                state = END
                                pivot = end
                                continue
                        elif state == END:
                            if (value[pivot] == c and c == '=') or (value[pivot] == '[' and c == ']'):# match finish
                                if pivot == beg: #comment match over
                                    return index+1
                                pivot -= 1
                            else:   # back to END
                                state = MID
                        elif state == LINE:
                            line_index = value.find('\n',beg-2)
                            if line_index == -1:
                                return length
                            else:
                                return line_index + 1
                            break
                        index += 1
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
        
        # Number analysis
        def get_number(value,index):
            START,ZERO,BEG,POINT,EXPO,END,HEX = 0,1,2,3,4,5,6
            state = START
            result = ''
            flag = False
            if value[index] == '-':
                result += value[index]
                index += 1
                flag = True
            while True:
                c = value[index]
                if state == START:
                    if c == '0':
                        state = ZERO
                    elif c.isdigit():
                        state = BEG
                    elif c == '.':
                        state = POINT
                    elif flag and c in(' ','\n','\r','\t'):
                        pass
                    else:
                        if result == '-':
                            if c.isalpha():
                                raise Exception('Table format wrong -- Number analysis ')
                            elif c == '-':
                                raise Exception('Table format wrong -- Number analysis ')
                            elif c in '~!@#$%^%&*()_+\":':
                                raise Exception('Table format wrong -- Number analysis ')
                            else:
                                raise Exception('Table format wrong -- Number analysis ')
                        else:
                            raise Exception('Table format wrong -- Number analysis ')
                elif state == ZERO:
                    if c in 'xX':
                        state = HEX
                    elif c.isdigit():
                        state = BEG
                    elif c == '.':
                        state = POINT
                    else :
                        return 0,index
                elif state == BEG:
                    if c.isdigit():
                        pass
                    elif c == '.':
                        state = POINT
                    elif c in 'eE':
                        state = EXPO
                    else:
                        return int(result),index
                elif state == POINT:
                    if c.isdigit():
                        pass
                    elif c in 'eE':
                        state = EXPO
                    else:
                        return float(result),index
                elif state == EXPO:
                    if c in '+-' or c.isdigit():
                        state = END
                    else:
                        raise Exception('Table format wrong -- Number analysis')
                elif state == END:
                    if c.isdigit():
                        pass
                    else:
                        return float(result),index
                elif state == HEX:
                    if c.isdigit() or c in 'abcdefABCDEF':
                        pass
                    else:
                        return int(result,16),index
                result += c
                index += 1

        # [==[string]==] analysis
        def get_bracket_str(value,index):
            BEG,START,EQUAL,MID,END,NUMA,SPACE = 0,1,2,3,4,5,6
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
                        state = SPACE
                        continue
                    elif c.isdigit() or c in '.-':
                        state = SPACE
                        continue
                    elif c == '=':
                        state = EQUAL
                    elif c == '[':
                        end = index
                        state = MID
                    elif c in (' ','\n','\r','\t'):
                        state = SPACE
                    else:
                        raise Exception('Table format wrong')
                elif state == EQUAL:
                    if c == '=':
                        state = EQUAL
                    elif c == '[':
                        end = index
                        state = MID
                    else:
                        raise Exception('Table format wrong')
                elif state == MID:
                    if c == ']':
                        state = END
                        pivot = end
                        continue
                    else :
                        result += c
                elif state == END:
                    if (value[pivot] == c and c == '=') or (value[pivot] == '[' and c == ']'):# match finish
                        if pivot == beg:
                            return result,EXP,index+1
                        pivot -= 1
                    else:   # back to END
                        state = MID
                        result += value[index-(end-pivot):index+1]
                elif state == NUMA:
                    if c == ']':
                        return var[0],KEY,index+1
                    elif c in (' ','\n','\r','\t'):
                        pass
                    else:
                        raise Exception('Table format wrong')
                elif state == SPACE:
                    if c in (' ','\n','\r','\t'):
                        pass
                    elif c in ('"',"'"):
                        var = get_str(value,index)
                        index = var[1]
                        state = NUMA
                        continue
                    elif c.isdigit() or c in '.-':
                        var = get_number(value,index)
                        index = var[1]
                        state = NUMA
                        continue
                    elif c == '[':
                        var = get_bracket_str(value,index)
                        if var[1] == EXP:
                            state = NUMA
                            index = var[2]
                            continue
                        else:
                            raise Exception('Table format wrong')
                    else:
                        raise Exception('Table format wrong')
                index += 1   
       
        val = r''
        val_stack = Stack()
        op_stack = Stack()
        map = {}
        array = []
        is_array = True
        is_first = True
        map_index = 1
        need_store = False
        finish = False 
        while True:
            if self.index >= self.length:
                raise Exception('Table format wrong')
            if need_store:
                if not val_stack.is_empty():
                    value = val_stack.peek()
                    val_stack.pop()
                    if not op_stack.is_empty() and op_stack.peek() == '=':
                        op_stack.pop()
                        key = val_stack.peek()
                        val_stack.pop()
                        if key[1]==NONE :
                            raise Exception('Table format wrong')
                        elif value[1] == NONE:
                            pass
                        else:
                            if (value[1]==EXP or value[1]==BOOL) and (key[1]==KEY or key[1]==NAME ):                            
                                map[key[0]] = value[0]
                                is_array = False
                            else :
                                if value[1] == KEY:
                                    if key[1] == BOOL:
                                        raise Exception('Table format wrong')  
                                    elif key[1] == EXP:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == KEY:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NAME:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NONE:
                                        raise Exception('Table format wrong') 
                                    else:
                                        raise Exception('Table format wrong')  
                                elif value[1] == NAME:
                                    if key[1] == BOOL:
                                        raise Exception('Table format wrong')  
                                    elif key[1] == EXP:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == KEY:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NAME:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NONE:
                                        raise Exception('Table format wrong') 
                                    else:
                                        raise Exception('Table format wrong')    
                                elif value[1] == EXP:
                                    if key[1] == BOOL:
                                        raise Exception('Table format wrong')  
                                    elif key[1] == EXP:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == KEY:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NAME:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NONE:
                                        raise Exception('Table format wrong') 
                                    else:
                                        raise Exception('Table format wrong')  
                                elif value[1] == BOOL:
                                    if key[1] == BOOL:
                                        raise Exception('Table format wrong')  
                                    elif key[1] == EXP:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == KEY:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NAME:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NONE:
                                        raise Exception('Table format wrong') 
                                    else:
                                        raise Exception('Table format wrong')  
                                elif value[1] == NONE:
                                    if key[1] == BOOL:
                                        raise Exception('Table format wrong')  
                                    elif key[1] == EXP:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == KEY:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NAME:
                                        raise Exception('Table format wrong') 
                                    elif key[1] == NONE:
                                        raise Exception('Table format wrong') 
                                    else:
                                        raise Exception('Table format wrong')
                                else:  
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
                    val_stack.push((item,EXP))   
                    need_store = True                
            elif c == '}':
                if not is_first:
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
            elif (c == '"' or c == "'"):    # Get String
                v = get_str(self.tableString,self.index)
                val_stack.push((v[0],EXP))
                self.index = v[1]
                continue
            elif c == '-' and self.tableString[self.index+1] == '-':
                self.index = remove_comment(self.tableString,self.index)
                continue
            elif c.isdigit() or c in '-.':  # Get Number
                v = get_number(self.tableString,self.index)
                val_stack.push((v[0],EXP))
                self.index = v[1]
                continue
            elif c == '[':                  # Get [[]] or []
                v = get_bracket_str(self.tableString,self.index)
                val_stack.push((v[0],v[1]))
                self.index = v[2]
                continue
            elif c.isalpha() or c == '_': # Get Name , bool , None
                v = get_name(self.tableString,self.index)
                val_stack.push((v[0],v[1]))
                self.index = v[2]
                continue
            else : # Skip in (' ','\n','\r','\t')
                pass
            self.index += 1

    

