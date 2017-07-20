using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;


class NetworkHandler
{
    public static Int16 MSG_CS_LOGIN = 0x1001;
    public static Int16 MSG_SC_CONFIRM = 0x2001;

    public static Int16 MSG_CS_MOVETO = 0x1002;
    public static Int16 MSG_SC_MOVETO = 0x2002;

    private TcpClient tcp_socket;
    private NetworkStream net_stream;
    private static NetworkHandler NetHandler = null;
    private string Host = "127.0.0.1";
    private int Port = 7777;

    private BinaryWriter bwriter;
    private BinaryReader breader;

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
                int recvsize = breader.ReadInt32();
                //Debug.Log("size:" + recvsize);
                Int16 command = breader.ReadInt16();
                Byte[] recvdata = breader.ReadBytes(recvsize - 6);
                //BinaryReader br = new BinaryReader(new MemoryStream(recvdata));
                //System.Console.WriteLine(command);
                if (command == MSG_SC_MOVETO)
                {
                    CommonInformation.playerCommandQueue.Enqueue(new Message(command, recvdata));
                }  
            }
            catch (Exception e)
            {
                NetHandler = null;

                //断开连接
                Debug.Log(e.ToString());
                break;
            }
        }
    }

    public void sendMoveMSG(Int16 command,int x,int z)
    {
        //Debug.Log(x+" "+z);
        //Debug.Log("send");
        bwriter.Write(14);
        bwriter.Write(MSG_CS_MOVETO);
        bwriter.Write(x);
        bwriter.Write(z);
        bwriter.Flush();
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
       


