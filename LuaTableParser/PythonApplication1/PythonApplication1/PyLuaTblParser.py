
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
        self.tableString = s.replace('\n','').replace('\r','')
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
            table_file = open(f)
            tableString = table_file.read()
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
            #print 'Handling :'+value
            if value == 'nil':
                return None
            elif value == 'false':
                return False
            elif value == 'true':
                return True
            elif value[0] =='"' and value[len(value)-1]=='"':
                return value[1:-1]
            elif not value[0].isdigit():
                return value
            else:
                try:
                    return int(value)
                except ValueError:
                    return float(value)

        val = ''
        val_stack = Stack()
        op_stack = Stack()
        map = {}
        array = []
        is_array = True
        is_first = True
        is_key = False
        map_index = 1

        while True:
            if self.index >= self.length:
                raise Exception('Table format wrong')
            c = self.tableString[self.index]
            if c == '{' :
                if is_first:
                    is_first = False
                else :
                    item = self.process()
                    if op_stack.peek() == '=':
                        if val_stack.peek() != None and item != None:
                            map[val_stack.peek()] = item
                        val_stack.pop()
                    else :
                        if is_array:
                            array.append(item)
                        elif item != None:
                            map[map_index] = item
                            map_index += 1
                             
            elif c == '}':
                if val != '':
                    temp = get_val(val)
                    val = ''
                    if op_stack.peek() == '=':
                        if val_stack.peek() != None and temp != None:
                            map[val_stack.peek()] = temp
                        val_stack.pop()
                    else :
                        if is_array:
                            array.append(temp)
                        elif temp != None:
                            map[map_index] = temp
                            map_index += 1
                if is_array or len(map)==0:
                    return array
                else:
                    return map
            elif c == '[' :
                op_stack.push(c)
            elif c == ']' and op_stack.peek() == '[':
                op_stack.pop()
                is_key = True
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
            elif c == ',':
                if val != '':
                    temp = get_val(val)
                    val = ''
                    if op_stack.peek() == '=':
                        if val_stack.peek() != None and temp != None:
                            if isinstance(val_stack.peek(),int) or isinstance(val_stack.peek(),float):
                                if is_key:
                                    is_key = False
                                else :
                                    raise Exception('Table format wrong')
                            map[val_stack.peek()] = temp
                        val_stack.pop()
                    else :
                        if is_array:
                            array.append(temp)
                        elif temp != None: 
                            map[map_index] = temp
                            map_index += 1
            elif c == ' ':
                pass
            elif c != ' ':
                val = val + c
            self.index += 1
    

