from PyLuaTblParser import PyLuaTblParser

pl = PyLuaTblParser()
#pl.load('{["\rjack"]=5}')
#print pl.table
#print pl.dump()
#pl.load('{}')
#print pl.table
#print pl.dump()
#pl.load('{nil}')
#print pl.table
#print pl.dump()
#pl.load('{jack = nil}')
#print pl.table
#print pl.dump()
#pl.load('{["x"] = 12, ["mutou"] = 99, [3] = "hello"}')
#print pl.table
#print pl.dump()
#pl.load('{x = 12, mutou = 99, [3] = "hello"}')
#print pl.table
#print pl.dump()
#pl.load(''' {
# {x = 1, y = 2},
# {x = 3, y = 10}
#}''')
#print pl.table
#print pl.dump()
#pl.load('{"45",23,5}')
#print pl.table
#print pl.dump()
#pl.load('{"45",23,5,true,false}')
#print pl.table
#print pl.dump()
#pl.load('{"45",23,5,{23,34,55}}')
#print pl.table
#print pl.dump()
#pl.load('{5,key="jack"}')
#print pl.table
#print pl.dump()
#pl.load('{"45",key="jack"}')
#print pl.table
#print pl.dump()
#pl.load('{array = {65,23,5,}}')
#print pl.table
#print pl.dump()
#pl.load('{43,54.33,false,9,string = "value",}')
#print pl.table
#print pl.dump()
#pl.load('{a = {5,},}')
#print pl.table
#pl.load('{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}')
#print pl.table
#print pl.dump()

#pl.loadLuaTable('test.txt')
#print pl.table
#print pl.dump()
#pl.dumpLuaTable('out.txt')
#pl.loadDict(pl.table)
#print pl.dumpDict()

pl.load('{["\rroot"] = {65,23,5,},"jack"}')
print pl.table
#print pl.dump()