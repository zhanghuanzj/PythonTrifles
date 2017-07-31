using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;


class NetworkHandler
{


    private TcpClient tcp_socket;
    private NetworkStream net_stream;
    private static NetworkHandler NetHandler = null;
    private string Host = "127.0.0.1";
    private int Port = 7777;

    private BinaryWriter bwriter;
    private BinaryReader breader;
    public static bool isQuit = false;

    public static NetworkHandler getNetHandlerInstance()
    {
        if (NetHandler == null)
        {
            NetHandler = new NetworkHandler();
        }
        return NetHandler;
    }

    private NetworkHandler()
    {
        if (isQuit)
        {
            return;
        }
        try
        {
            tcp_socket = new TcpClient(Host, Port);
            net_stream = tcp_socket.GetStream();
            bwriter = new BinaryWriter(net_stream);
            breader = new BinaryReader(net_stream);

            Debug.Log("Connected");
            Thread thread = new Thread(new ThreadStart(recvMSG));//从服务器接受消息
            thread.IsBackground = true;
            thread.Start();
        }
        catch (Exception e)
        {
            Debug.Log(e.ToString());
            NetHandler = null;
            Debug.Log("Time Out");
        }
       
    }

    private void recvMSG()
    {
        while (true)
        {
            if (!tcp_socket.Connected)//断开连接
            {
                NetHandler = null;
                Debug.Log("break connect");
                tcp_socket.Close();
                break;
            }
            try
            {
                if (isQuit)
                {
                    return;
                }
                int recvsize = breader.ReadInt32();
                Int16 command = breader.ReadInt16();
                int hid = breader.ReadInt32();
                Byte[] recvdata = breader.ReadBytes(recvsize - (sizeof(int) + sizeof(Int16) + sizeof(Int32)) );

                //System.Console.WriteLine(command);
                if (command == CommonInformation.MSG_SC_MOVETO || command == CommonInformation.MSG_SC_ROTATE || 
                    command == CommonInformation.MSG_SC_ATTACKED || command == CommonInformation.MSG_SC_FIRER || 
                    command == CommonInformation.MSG_SC_FIREL || command == CommonInformation.MSG_SC_MONEY ||
                    command == CommonInformation.MSG_SC_TRAPCREATE || command == CommonInformation.MSG_SC_TRAPBUY )
                {
                    if (CommonInformation.playersQueue.ContainsKey(hid))//鼠标移动信息传输
                    {
                        CommonInformation.playersQueue[hid].Enqueue(new Message(command, recvdata));
                    }
                }
                else if (command == CommonInformation.MSG_SC_CONFIRM)
                {
                    Debug.Log("********************:" + CommonInformation.userhid);
                    CommonInformation.userhid = hid;
                    if (!CommonInformation.playersQueue.ContainsKey(hid))
                    {
                        CommonInformation.playersQueue.Add(hid, new Queue());
                    }
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    Login.result = br.ReadInt32();
                    br.Close();
                } 
                else if(command == CommonInformation.MSG_SC_RCONFIRM)
                {
                    
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    Register.result = br.ReadInt32();
                    br.Close();
                }
                else if (command == CommonInformation.MSG_SC_ROOMS)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    CommonInformation.serverRooms = br.ReadString();
                    br.Close();
                }
                else if (command == CommonInformation.MSG_SC_CREATEROOM)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    CreateRoom.result = br.ReadInt32();
                    br.Close();
                }
                else if (command == CommonInformation.MSG_SC_ENTERROOM)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    EnterRoom.result = br.ReadInt32();
                    br.Close();
                }
                else if (command == CommonInformation.MSG_SC_PLAYERS)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    CommonInformation.serverPlayers = br.ReadString();
                    br.Close();
                }
                else if (command == CommonInformation.MSG_SC_BEGIN)
                {
                    CommonInformation.isGameBegin = true;
                    CommonInformation.isGameOver = false;
                    CommonInformation.isGameWin = false;
                    CommonInformation.playersQueue[hid].Enqueue(new Message(command, recvdata));

                }
                else if (command == CommonInformation.MSG_SC_ENEMYCREATE)
                {
                    CommonInformation.playersQueue[CommonInformation.userhid].Enqueue(new Message(command, recvdata));
                }
                else if (command == CommonInformation.MSG_SC_EMOVETO || command == CommonInformation.MSG_SC_ENEMYARRIVE ||
                    command == CommonInformation.MSG_SC_ENEMYATTACK || command == CommonInformation.MSG_SC_AIMED ||
                    command == CommonInformation.MSG_SC_AIMEDLEFT || command == CommonInformation.MSG_SC_TRAPATTACK)
                {
                    if (CommonInformation.enemysQueue.ContainsKey(hid))
                    {
                        CommonInformation.enemysQueue[hid].Enqueue(new Message(command, recvdata));
                    }
                }
                else if (command == CommonInformation.MSG_SC_GAMEOVER)
                {
                    CommonInformation.isGameOver = true;
                }
                else if (command == CommonInformation.MSG_SC_GAMEWIN)
                {
                    CommonInformation.isGameWin = true;
                }
                else if (command == CommonInformation.MSG_SC_COUNTDOWN)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                    CommonInformation.countDown = br.ReadInt32();
                    br.Close();
                }
            }
            catch (Exception e)
            {
                close();
                //断开连接
                Debug.Log(e.ToString());
                break;
            }
        }
    }

    public void sendMSG(Int16 command,ArrayList values)
    {
        if (isQuit)
        {
            return;
        }
        int size = sizeof(Int16) + sizeof(int);
        if (values != null)
        {
            foreach (object o in values)
            {
                if (o is int)
                {
                    size += sizeof(int);
                }
                else
                {
                    size += (o as string).Length + sizeof(Byte);
                }
            }
        }
        bwriter.Write(size);
        bwriter.Write(command);
        //Debug.Log("Size:"+size);
        if (values != null)
        {
            foreach (object o in values)
            {
                if (o is int)
                {
                    bwriter.Write((int)o);
                }
                else
                {
                    Debug.Log(o as string);
                    bwriter.Write(o as string);
                }
            }
        }
        bwriter.Flush();
    }

    public void close()
    {
        tcp_socket.Close();
        net_stream.Close();
        bwriter.Close();
        breader.Close();
        NetHandler = null;
        isQuit = true;
    }

}

struct Message
{
    public Int16 commandID;
    public Byte[] data;
    public Message(Int16 id, Byte[] data)
    {
        this.commandID = id;
        this.data = data;
    }
}
       


