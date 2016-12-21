# PythonTrifles
##1.Basic
python 小程序
##2.Lua Table Parser
完成lua table构造式的存储转换，将字符串转换成python中的结构，以及支持dump出构造式字符串，文件导入导出，结构访问更新等
##3.ChatServer
1. 客户端可以账户名、密码登陆进入游戏大厅						
2. 可以注册新用户											
3. 支持聊天
	- 	chatall:所有人可见
	- 	chatroom:房间内可见
	- 	chatto:私聊												
4. 账户有在线时长的属性，需要存盘，下线再上不会丢失数据							
5. 有创建房间(createroom id)，进入房间(enterroom id)，退出房间(quitroom)功能		
6. 每个房间，每逢半点（8点半，9点，9点半等），会随机生成4个1到10内的数，发布在房间内，所有人可以看到;玩家可以用+,-,*,/和括号参与21点游戏										
