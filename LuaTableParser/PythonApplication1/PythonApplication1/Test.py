from PyLuaTblParser import PyLuaTblParser

def test(s):
    pl = PyLuaTblParser()
    pl.load(s)
    print '----------------------------'
    print 'str:',s
    print 'self:',pl.table
    print 'dump:',pl.dump()
    pl.load(pl.dump())
    print 'new:',pl.table

def test_f(fi,fo):
    pl = PyLuaTblParser()
    pl.testLuaTable('test.txt')
    pl.dumpLuaTable('out.txt')

test('''{
	x=1,
	y=2,
	z=3,
	{a=-1,a1=1},
	{b=-2,b1=2},
	{c=-3,c1=3},
}''')
test('{b=2,nil,"jfd",{nil,12,"jack"}}')
test('{bbb=23,"dsd",false,nil,"jfd"}')
test('{{["y"]=2,["x"]=true,},{["y"]=10,["x"]=3,},}')
test(' {{["y"]= 2}, {["x"]= 2}}')
test('{["\rjack"]=5}')
test('{}')
test('{nil}')
test('{jack = nil}')
test('{["x"] = 12, ["mutou"] = 99, [3] = "hello"}')
test('{x = 12, mutou = 99, [3] = "hello"}')
test(''' {
    {
        x = 1, 
        y = 2},
    {x = 3, y = 10}
}''')
test('{"45",23,5}')
test('{"45",23,5,true,false}')
test('{"45",23,5,{23,34,55}}')
test('{5,key="jack"}')
test('{"45",key="jack"}')
test('{array = {65,23,5,}}')
test('{43,54.33,false,9,string = "value",}')
test('{a = {5,},}')
test('{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}')

test('{_j3="f 45"}')
test(r'{a="\"f"}')
test(r'{["{}[] \"\\=-+,./?()"] = "jac=k[] \"{}\\"}')
test('{"{","j=45"}')
test('{["t"] = {6,},"j"}')

test('{[true]="g";"x","y";x=1,4,[30]=23;45}')

test('{["_jack2"]="g";"x","y";_x23yf=1,4,[30]=23;45}')

d= {"a" : ("apple",), "bo" : {"b" : "banana", "o" : "orange"}, "g" : ["grape","grapefruit"],"0x44":0x44}
pl = PyLuaTblParser()
pl.loadDict(d)
print pl.dump()
pl.load(pl.dump())
print pl.table
test('''{
    3,
    [2] = 5,
    ["jack"] = 3,
    tom = 3,
    [21] = "j",
    ["jack1"] = "j",
    tom1 = "j",
    [22] = true,
    ["jack2"] = true,
    tom2 = true,
    [23] = false,
    ["jack3"] = false,
    tom3 = false,
    [24] = 4.5,
    ["jack4"] = 4.5,
    tom4 = 4.5,
    [25] = {4.5},
    ["jack5"] = {4.5},
    tom = {4.5},
    [26] = nil,
    ["jack6"] = nil,
    tom6 = ,
}''')
print pl.table
print pl.dump()

test('''
{
    jack = 
    {
        {
            [3] = 
            {
                34,22,"f"
            }
        },
        key1 = "key1",
        "v2"
    }
}''')

test('{[0] = "Sunday","Monday","Thuesday","Wednesday"}')
test('''{23,aa=23,23,  
                {bbb=23,"dsd",false,nil,  
                    {32,ccc="23dd",  
                        {23,"sdfsdf",  
                            {234,addd="23233jjjjsdOK"}  
                        }  
                    }  
                },  
                {dd = "sd",23},  
            true  
            }  ''')

test('''{
    { port = 1234, address = "192.168.1.1", userdata = "liunx" },
    { port = 1235, address = "192.168.1.2", userdata = "liunx1" },
    { port = 1236, address = "192.168.1.3", userdata = "liunx2" }
}''')

test('''{
  STANDBY = {
    timeout = "10",
    mode = "0"
  },
  RTP = {
    minport = "10000",
    maxport = "10010"
  }
}''')

test('''{ 
    { 
        { 
            { X = -1, Y =  2, Z =  1 },
            { X =  0, Y =  2, Z =  1 },
            { X =  1, Y =  2, Z =  1 }
        },
        { 
            { X = -1, Y =  1, Z =  1 },
            { X =  0, Y =  1, Z =  1 },
            { X =  1, Y =  1, Z =  1 }
        },
        { 
            { X = -1, Y =  0, Z =  1 },
            { X =  0, Y =  0, Z =  1 },
            { X =  1, Y =  0, Z =  1 }
        },
        { 
            { X = -1, Y = -1, Z =  1 },
            { X =  0, Y = -1, Z =  1 },
            { X =  1, Y = -1, Z =  1 }
        }
    },
    { 
        { 
            { X =  1, Y =  2, Z = -1 },
            { X =  1, Y =  2, Z =  0 },
            { X =  1, Y =  2, Z =  1 }
        },
        { 
            { X =  1, Y =  1, Z = -1 },
            { X =  1, Y =  1, Z =  0 },
            { X =  1, Y =  1, Z =  1 }
        },
        {
            { X =  1, Y =  0, Z = -1 },
            { X =  1, Y =  0, Z =  0 },
            { X =  1, Y =  0, Z =  1 }
        },
        { 
            { X =  1, Y = -1, Z = -1 },
            { X =  1, Y = -1, Z =  0 },
            { X =  1, Y = -1, Z =  1 }
        }
    },
    { 
        { 
            { X = -1, Y =  2, Z = -1 },
            { X =  0, Y =  2, Z = -1 },
            { X =  1, Y =  2, Z = -1 }
        },
        { 
            { X = -1, Y =  1, Z = -1 },
            { X =  0, Y =  1, Z = -1 },
            { X =  1, Y =  1, Z = -1 }
        },
        { 
            { X = -1, Y =  0, Z = -1 },
            { X =  0, Y =  0, Z = -1 },
            { X =  1, Y =  0, Z = -1 }
        },
        { 
            { X = -1, Y = -1, Z = -1 },
            { X =  0, Y = -1, Z = -1 },
            { X =  1, Y = -1, Z = -1 }
        }
    },
    { 
        { 
            { X = -1, Y =  2, Z = -1 },
            { X = -1, Y =  2, Z =  0 },
            { X = -1, Y =  2, Z =  1 }
        },
        { 
            { X = -1, Y =  1, Z = -1 },
            { X = -1, Y =  1, Z =  0 },
            { X = -1, Y =  1, Z =  1 }
        },
        { 
            { X = -1, Y =  0, Z = -1 },
            { X = -1, Y =  0, Z =  0 },
            { X = -1, Y =  0, Z =  1 }
        },
        { 
            { X = -1, Y = -1, Z = -1 },
            { X = -1, Y = -1, Z =  0 },
            { X = -1, Y = -1, Z =  1 }
        }
    }
}''')

test('''{{{{}, {}, a={}, {}, {}, }, b={{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, }, {{{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, }, {{{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, }, {{{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, {{}, {}, {}, {}, {}, }, }, } ''')

test(r'''{jack = {jac="{}[] \"\*&^%$#@!~;\'=-+,./?()"}}''')

print '\''
test(r'''{
    {{["f\""]='j"\''}},
    abc = "'\'\"",
    ['"\'\"\\
    '] = 4
}''')