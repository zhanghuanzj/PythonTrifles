from PyLuaTblParser import PyLuaTblParser

def test(s):
    pl = PyLuaTblParser()
    pl.load(s)
    print '----------------------------'
    print 'sstr:',s
    print 'self:',pl.table
    print 'dum1:',pl.dump()
    pl.load(pl.dump())
    print 'nnew:',pl.table
    print 'dum2:',pl.dump()
    pl.dumpLuaTable('test.txt')
    print 'dump to file'
    #f = open('test.txt','w')
    #f.write(s)
    #f.close()
    pl.loadLuaTable('test.txt')
    print 'load from file'
    print 'fnew:',pl.table
    print 'dum3:',pl.dump()

pl = PyLuaTblParser()
#pl.loadLuaTable('test.txt')
#print 'load from file'
#print 'fnew:',pl.table
#print 'dum3:',pl.dump()

test(r'''{"-- Copyright (c) 2012 Robert Forsman\n-- This work is made available under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license, http://creativecommons.org/licenses/by-nc-sa/3.0/\n-- ACmenu=raids/Throne of Thunder/Jin'rokh\n\n\nfunction GSL(sid)\n    local a={ EJ_GetSectionInfo(sid) }\n    return a[9]\nend\n\nlocal d = 1;\nlocal c=\"SAY\"\nif \"raid\" == ({IsInInstance()})[2] then\n    d = GetRaidDifficultyID()\n    c=\"RAID\"\nend\nif (IsInGroup(LE_PARTY_CATEGORY_INSTANCE)) then\n    c=\"INSTANCE_CHAT\"\nend\n\nEJ_SetDifficulty(d)\n\n\nlocal Implosion = GSL(7744)\nlocal StaticWound = GSL(7739)\nlocal FocusedLightning = GSL(7741)\nlocal ConductiveWater = GSL(7822)\nlocal LightningFissure = GSL(7743)\nlocal Fluidity = GSL(7735)\nlocal LightningStorm = GSL(7748)\nlocal ElectrifiedWaters = GSL(7737)\n\nSendChatMessage(\"Whenever the boss applies \"..StaticWound..\" to the tank, the other tank should take over immediately, even if they have a few stacks left.\", c);\nSendChatMessage(\"Kite the \"..FocusedLightning..\" to a grate and don't let it explode in \"..ConductiveWater..\".\", c);\nSendChatMessage(\"Under no circumstances let it touch a \"..LightningFissure..\" or the raid will be wiped by \"..Implosion, c);\n\nSendChatMessage(\"Stand in \"..ConductiveWater..\" to get \"..Fluidity..\", but get out when \"..LightningStorm..\" converts it to \"..ElectrifiedWaters..\".\")"}''')
test('''{23,aa=23,23,  
                {bbb=23,"dsd",false,nil,  --jfsdlkjf
                    {32,ccc="23dd",  
                        {23,"sdfsdf",  
                            {234,addd="23233jjjjsdOK"}  --fdsj
                        }  
                    }  --[=[jfdk
jsdlfjsal
fsldkjf
fjasd
]=]
                },  
                {dd = "sd",23},  
            true  
            }  ''')

test('{[3300.0]=45,[300.0]=45,[0.03]=45,}')
test('{3e2}')
test('{b=-2}')
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

test('{["true"]="g";"x","y";x=1,4,[30]=23;45}')

test('{["_jack2"]="g";"x","y";_x23yf=1,4,[30]=23;45}')

d= {"a" : ("apple",), "bo" : {"b" : "banana", "o" : "orange"}, "g" : ["grape","grapefruit"],"0x44":"0x44"}
pl = PyLuaTblParser()
pl.loadDict(d)
print 'dump:',pl.dump()
pl.load(pl.dump())
print pl.table
print '--------------'
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
    tom6 = 4,
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
print 'A'.isalnum()
s = r''' '"\'\"'''
print s.find(r'"')
print s.find(r'\"') 
print s.find(r"'") 
print s.find(r"\'") 
ss = s[:]
#for v in s:
#     ss += v
print ss.find(r'"')
print ss.find(r'\"') 
print ss.find(r"'") 
print ss.find(r"\'")
test(r'''{[['jf\"]]}''')
test(r'''{"'jf\""}''')
test(r'''{[['"\'\"\\']]}''')
test(r'''{[[\'\"\\']]}''')
test(r'''{[['\'\"\\']]}''')
test(r'''{[['"\'\"\\']]}''')
test(r'''{{{["f\""]='j"\''}},}''')
test(r'''{[1]=[['"\'\"\\']],[2]={{['f\"']=[[j"\']],},},['abc']=[['\'\"]],}''')
test(r'''{[['"\'\"\\']],
    {{["f\""]='j"\''}},
    abc = "'\'\"",
}''')

test('''{'[==[
     alo
     123"]==]',jack = 09}''')

print 3e+2
test('{[ 0x34 ]=45}')
test('''{[0x34]=45,[0X34]=45,[034]=45,[3e2]=45,[3e-2]=45,[3e+2]=45,[3.3e3]=45,
{{[0x34]=45.3,[0X34]=-45,[034]=+45e-3,[3e4]=0xabcdefABCEDF45,[3e-2]=45,[3e+2]=45,[3.3e3]=45,},}}
''')

test('{314.16e-2,.34,[.3e2]=.8,- 4,-43.4e3}')

pl = PyLuaTblParser()
comment = '''{23,aa=23,23,  
                {bbb=23,"dsd",false,nil,  --jfsdlkjf
                    {32,ccc="23dd",  
                        {23,"sdfsdf",  
                            {234,addd="23233jjjjsdOK"}  --fdsj
                        }  
                    }  --[=[jfdk
jsdlfjsal
fsldkjf
fjasd
]=]
                },  
                {dd = "sd",23},  
            true  
            }  '''

c0 = '''jack --jkd
-- coment'''
c1 = ''' --[[j
df]]
'''
#print pl.remove_comment(comment)

test('''{['jack' ]=4}''')

test('''{[ [=[4]=]] = 34}
''')

test(r'''{
	["profileKeys"] = {
		["Bambootay - Whisperwind"] = "Default",
	},
	["profiles"] = {
		["Default"] = {
			["commands"] = {
				{
					["script"] = "-- Copyright (c) 2012 Robert Forsman\n-- This work is made available under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license, http://creativecommons.org/licenses/by-nc-sa/3.0/\n-- ACmenu=raids/Throne of Thunder/Jin'rokh\n\n\nfunction GSL(sid)\n    local a={ EJ_GetSectionInfo(sid) }\n    return a[9]\nend\n\nlocal d = 1;\nlocal c=\"SAY\"\nif \"raid\" == ({IsInInstance()})[2] then\n    d = GetRaidDifficultyID()\n    c=\"RAID\"\nend\nif (IsInGroup(LE_PARTY_CATEGORY_INSTANCE)) then\n    c=\"INSTANCE_CHAT\"\nend\n\nEJ_SetDifficulty(d)\n\n\nlocal Implosion = GSL(7744)\nlocal StaticWound = GSL(7739)\nlocal FocusedLightning = GSL(7741)\nlocal ConductiveWater = GSL(7822)\nlocal LightningFissure = GSL(7743)\nlocal Fluidity = GSL(7735)\nlocal LightningStorm = GSL(7748)\nlocal ElectrifiedWaters = GSL(7737)\n\nSendChatMessage(\"Whenever the boss applies \"..StaticWound..\" to the tank, the other tank should take over immediately, even if they have a few stacks left.\", c);\nSendChatMessage(\"Kite the \"..FocusedLightning..\" to a grate and don't let it explode in \"..ConductiveWater..\".\", c);\nSendChatMessage(\"Under no circumstances let it touch a \"..LightningFissure..\" or the raid will be wiped by \"..Implosion, c);\n\nSendChatMessage(\"Stand in \"..ConductiveWater..\" to get \"..Fluidity..\", but get out when \"..LightningStorm..\" converts it to \"..ElectrifiedWaters..\".\")",
					["menulabel"] = "Jin'rokh",
				}, -- [1]
				{
					["sub"] = {
						{
							["sub"] = {
								{
									["script"] = "",
									["menulabel"] = "Jin'rokh",
								}, -- [1]
								{
									["script"] = "-- Copyright (c) 2012 Robert Forsman\n-- This work is made available under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license, http://creativecommons.org/licenses/by-nc-sa/3.0/\n-- ACmenu=raids/Throne of Thunder/Horridon.lua\n\n\nfunction GSL(sid)\n    local a={ EJ_GetSectionInfo(sid) }\n    return a[9]\nend\n\nlocal d = 1;\nlocal c=\"SAY\"\nif \"raid\" == ({IsInInstance()})[2] then\n    d = GetRaidDifficultyID()\n    c=\"RAID\"\nend\nif (IsInGroup(LE_PARTY_CATEGORY_INSTANCE)) then\n    c=\"INSTANCE_CHAT\"\nend\n\nEJ_SetDifficulty(d)\n\nlocal TriplePuncture = GSL()\nlocal DoubleSwipe = GSL()\nlocal Charge = GSL()\nlocal StoneGaze = GSL()\nlocal Sandtrap = GSL()\nlocal LivingPoison = GSL()\nlocal VenomousEffusion = GSL()\nlocal FrozenOrb = GSL()\nlocal AmaniWarbear = GSL()\nlocal Swipe = GSL()\nlocal LNTotem = GSL()\nlocal Dinomancer = GSL()\nlocal OrbOfControl = GSL()\nlocal WarGod = GSL()\n\nSendChatMessage(\"Tanks take turns to drop \"..TriplePuncture..\" stacks.  \"..DoubleSwipe..\" is a front and tail swipe, so let DPS be at his side.\", c)\nSendChatMessage(Charge..\" victim run close to Horridon and point his \"..DoubleSwipe..\" away from the raid.\", c)\nSendChatMessage(\"Don't let the tank get \"..StoneGaze..\".  Run out of \"..Sandtrap..\".\", c)\nSendChatMessage(\"Get out of \"..LivingPoison..\".  Kill the \"..VenomousEffusion..\".\", c)\nSendChatMessage(\"Run away from \"..FrozenOrb..\".\", c)\nSendChatMessage(\"Point \"..AmaniWarbear..\" away from the raid for \"..Swipe..\".  Run away from \"..LNTotem..\".\", c)\nSendChatMessage(\"Kill the \"..Dinomancer..\" and activate \"..OrbOfControl..\".\", c)\nSendChatMessage(\"Kill \"..WarGod..\", then finish Horridon.\", c)",
									["menulabel"] = "Horridon",
								}, -- [2]
								{
									["script"] = "-- Copyright (c) 2012 Robert Forsman\n-- This work is made available under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license, http://creativecommons.org/licenses/by-nc-sa/3.0/\n-- ACmenu=raids/Throne of Thunder/Horridon.lua\n\n\nfunction GSL(sid)\n    local a={ EJ_GetSectionInfo(sid) }\n    return a[9]\nend\n\nlocal d = 1;\nlocal c=\"SAY\"\nif \"raid\" == ({IsInInstance()})[2] then\n    d = GetRaidDifficultyID()\n    c=\"RAID\"\nend\nif (IsInGroup(LE_PARTY_CATEGORY_INSTANCE)) then\n    c=\"INSTANCE_CHAT\"\nend\n\nEJ_SetDifficulty(d)\n\nlocal FrigidAssault = GSL(7054)\nlocal Overload = GSL(7059)\nlocal Quicksand = GSL(7062)\nlocal Sandstorm = GSL(7065)\nlocal LivingSand = GSL(7066)\nlocal Fortified = GSL(7067)\nlocal BlessedLoaSpirit = GSL(7070)\nlocal ShadowedLoaSpirit = GSL(7072)\nlocal Sul = GSL(7049)\nlocal Marli = GSL(7050)\nlocal Garajal = GSL(7051)\n\nSendChatMessage(\"When \"..FrigidAssault..\" stacks to 15 the tank is frozen.  Heal it like you mean it.\", c)\nSendChatMessage(\"Beware of \"..Overload..\" (reflection) when Kara'jin is posessed.\", c)\nSendChatMessage(\"Stay out of \"..Quicksand..\".  During \"..Sandstorm..\" quickly kill \"..LivingSand..\" before they get \"..Fortified..\".\", c)\nSendChatMessage(\"Snare and do not let \"..BlessedLoaSpirit..\" live long enough to heal a boss.  Kill \"..ShadowedLoaSpirit..\" before it kills its victim.\", c)\nSendChatMessage(\"Kill order is \"..Sul..\", \"..Marli..\", whatever.  Tank Marli far from the other bosses.\", c)\nSendChatMessage(\"Whoever turns tall and purple has \"..Garajal..\".  Beat the purple out of them before he/she kills us.\", c)",
									["menulabel"] = "Council of Elders",
								}, -- [3]
							},
							["menulabel"] = "Throne of Thunder",
						}, -- [1]
						{
							["script"] = "function recurseSection(sid)\n    local title, description, headerType, abilityIcon, displayInfo, siblingID, nextSectionID, filteredByDifficulty, link, startsOpen, flag1 = EJ_GetSectionInfo(sid)\n    DEFAULT_CHAT_FRAME:AddMessage(\n        sid..\" \"..title ,\n        \n    1,0.7,0.5)\n    if nextSectionID then\n        recurseSection(nextSectionID)\n    end\n    if siblingID then\n        recurseSection(siblingID)\n    end\nend\n\n\neid = 816\nname, description, encounterID, rootSectionID, link = EJ_GetEncounterInfo(eid)\nrecurseSection(rootSectionID)",
							["menulabel"] = "list sections",
						}, -- [2]
					},
					["menulabel"] = "raids",
				}, -- [2]
				{
					["sub"] = {
						{
							["tooltip"] = "Player and NPC nameplates on",
							["script"] = "        SetCVar(\"UnitNameEnemyPlayerName\",\"1\")\n        SetCVar(\"UnitNameFriendlyPlayerName\",\"1\")\n        SetCVar(\"UnitNameNPC\",\"1\")\n    ",
							["menulabel"] = "PvP",
						}, -- [1]
						{
							["tooltip"] = "Player nameplates off, NPC nameplates on",
							["script"] = "        SetCVar(\"UnitNameEnemyPlayerName\",\"0\")\n        SetCVar(\"UnitNameFriendlyPlayerName\",\"0\")\n        SetCVar(\"UnitNameNPC\",\"1\")\n    ",
							["menulabel"] = "Solo",
						}, -- [2]
						{
							["tooltip"] = "Player and NPC nameplates off",
							["script"] = "        SetCVar(\"UnitNameEnemyPlayerName\",\"0\")\n        SetCVar(\"UnitNameFriendlyPlayerName\",\"0\")\n        SetCVar(\"UnitNameNPC\",\"0\")\n    ",
							["menulabel"] = "Raid/Healing",
						}, -- [3]
					},
					["menulabel"] = "Labels",
				}, -- [3]
				{
					["script"] = "    -- Frees up a keybinding for combat use\n    SetCVar(\"Sound_MasterVolume\",\"0.7\")",
					["menulabel"] = "Sound High",
				}, -- [4]
				{
					["script"] = "    -- Frees up a keybinding for combat use\n    SetCVar(\"Sound_MasterVolume\",\"0.1\")",
					["menulabel"] = "Sound Low",
				}, -- [5]
				{
					["script"] = "    -- Frees up a keybinding for combat use\n    local v = GetCVar(\"Sound_EnableMusic\")\n    v = (v==\"1\") and \"0\" or \"1\"\n    SetCVar(\"Sound_EnableMusic\",v)",
					["menulabel"] = "Toggle Music",
				}, -- [6]
				{
					["sub"] = {
						{
							["verbose"] = false,
							["script"] = "sRaidFrames:SetCurrentGroupSetup(\"By class\")",
							["menulabel"] = "sort by class",
						}, -- [1]
						{
							["verbose"] = false,
							["script"] = "sRaidFrames:SetCurrentGroupSetup(\"By group\")",
							["menulabel"] = "sort by group",
						}, -- [2]
					},
					["menulabel"] = "sRaidFrames",
				}, -- [7]
				{
					["verbose"] = false,
					["script"] = "    -- do the actual toggle\n    SLASH(\"/bb settings polyoutput raid\")\n    -- if it was toggled *on* then warn the silly rogues...\n    if BigBrother.db.profile.PolyOut[3] then\n        CHAT(\"ra\", \"CC-breaking shame mod enabled.  Improve your awareness!\")\n    end",
					["menulabel"] = "BB raid toggle",
				}, -- [8]
			},
		},
	},
}
''')

c = r'''-- "\nfjdklfjaee
'''
print c.find('\n')
