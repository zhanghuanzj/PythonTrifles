using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

class CommonInformation
{

    public static Int16 MSG_CS_QUIT = 0x0000;
    public static Int16 MSG_CS_QUITROOM = 0x0001;

    public static Int16 MSG_CS_LOGIN = 0x1001;
    public static Int16 MSG_SC_CONFIRM = 0x2001;

    public static Int16 MSG_CS_REGISTER = 0x1003;
    public static Int16 MSG_SC_RCONFIRM = 0x2003;

    public static Int16 MSG_CS_MOVETO = 0x1002;
    public static Int16 MSG_SC_MOVETO = 0x2002;

    public static Int16 MSG_CS_ROTATE = 0x1004;
    public static Int16 MSG_SC_ROTATE = 0x2004;

    public static Int16 MSG_CS_FIREL = 0x1005;
    public static Int16 MSG_SC_FIREL = 0x2005;

    public static Int16 MSG_CS_FIRER = 0x1006;
    public static Int16 MSG_SC_FIRER = 0x2006;

    public static Int16 MSG_CS_ROOMS = 0x1007;
    public static Int16 MSG_SC_ROOMS = 0x2007;

    public static Int16 MSG_CS_CREATEROOM = 0x1008;
    public static Int16 MSG_SC_CREATEROOM = 0x2008;

    public static Int16 MSG_CS_ENTERROOM = 0x1009;
    public static Int16 MSG_SC_ENTERROOM = 0x2009;

    public static Int16 MSG_CS_PLAYERS = 0x1010;
    public static Int16 MSG_SC_PLAYERS = 0x2010;

    public static Int16 MSG_CS_BEGIN = 0x1020;
    public static Int16 MSG_SC_BEGIN = 0x2020;

    public static Int16 MSG_SC_ENEMYCREATE = 0x1030;
    public static Int16 MSG_SC_EMOVETO = 0x2030;

    public static Int16 MSG_SC_ENEMYARRIVE = 0x1040;
    public static Int16 MSG_SC_ENEMYATTACK = 0x2040;

    public static Int16 MSG_SC_ATTACKED = 0x1050;

    public static Int16 MSG_CS_AIMED = 0x1060;
    public static Int16 MSG_SC_AIMED = 0x2060;

    public static Int16 MSG_CS_AIMEDLEFT = 0x1070;
    public static Int16 MSG_SC_AIMEDLEFT = 0x2070;

    public static Int16 MSG_SC_GAMEOVER = 0x1080;
    public static Int16 MSG_SC_GAMEWIN = 0x2080;

    public static Int16 MSG_SC_MONEY = 0x1090;
    public static Int16 MSG_SC_COUNTDOWN = 0x2090;

    public static Int16 MSG_CS_TRAPCREATE = 0x1100;
    public static Int16 MSG_SC_TRAPCREATE = 0x2100;

    public static Int16 MSG_CS_TRAPATTACK = 0x1200;
    public static Int16 MSG_SC_TRAPATTACK = 0x2200;

    public static Int16 MSG_CS_TRAPBUY = 0x1300;
    public static Int16 MSG_SC_TRAPBUY = 0x2300;

    public static int LOGIN_SUCCESS = 0;
    public static int LOGIN_FAILED = 1;

    public static int REGISTER_SUCCESS = 2;
    public static int REGISTER_FAILED = 3;

    public static int FIRE_LEFT = 4;
    public static int FIRE_RIGHT = 5;

    public static int CREATEROOM_SUCCESS = 6;
    public static int CREATEROOM_FAILED = 7;

    public static int ENTERROOM_SUCCESS = 8;
    public static int ENTERROOM_FAILED = 9;

    public static int FIRE_TRAP = 10;
    public static int NEEDLE_TRAP = 11;

    public static int ENEMY_BEAR = 1;
    public static int ENEMY_BUNNY = 2;
    public static int ENEMY_ELEPHANT = 3;



    public static RaycastHit shootHit ;
    public static string serverRooms = null;
    public static string serverPlayers = null;
    public static Quaternion playerRotate;
    public static String username = "";
    public static int userhid = 0;
    public static Dictionary<int, Queue> playersQueue = new Dictionary<int, Queue>();
    public static Dictionary<int, Queue> enemysQueue = new Dictionary<int, Queue>();
    public static int hp = 100;
    public static float cd = 0.0f;
    public static bool isGameOver = false;
    public static bool isGameWin = false;
    public static bool isGameBegin = false;
    public static bool isHost = true;
    public static int score = 0;
    public static int maxhp = 0;
    public static int nextExp = 0;
    public static int exp = 0;
    public static int lv = 0;
    public static int momey = 0;
    public static int fire = 0;
    public static int needle = 0;
    public static bool isFireTrap = true;
    public static int countDown = -1;
    public static Vector3 startPoint = new Vector3(-6.8f, 0f, -22.8f);

    private static int mAmplify = 100;


    public static int Amplify(float value)
    {
        return (int)(value * mAmplify);
    }

    public static float DeAmplify(int value)
    {
        return ((float)value) / mAmplify;
    }

    public static bool IsLocal(int hostid)
    {
        return userhid == hostid;
    }

    public static void Clean()
    {
        serverRooms = null;
        serverPlayers = null;
        Queue q = playersQueue[userhid];
        playersQueue.Clear();
        playersQueue.Add(userhid, q);
        enemysQueue.Clear();
        hp = 100;
        cd = 0.0f;
        countDown = -1;
    }
}

