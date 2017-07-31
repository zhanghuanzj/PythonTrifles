using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;

public class PlayerNetwork : MonoBehaviour {

    private PlayerMovement mPlayerMovement;
    private PlayerHealth mPlayerHealth;
    private PlayerShooting mPlayerShoot;
    private TrapManager mTrapManager;
    public GameObject mEllephant;
    public GameObject mBear;
    public GameObject mBunny;
    public GameObject Player;
    public int hid;
    public Text playername;
	// Use this for initialization
	void Start () {
        mPlayerMovement = GetComponent<PlayerMovement>();
        mPlayerHealth = GetComponent<PlayerHealth>();
        mPlayerShoot = GetComponentInChildren<PlayerShooting>();
        mTrapManager = GetComponentInChildren<TrapManager>();

    }
	
	// Update is called once per frame
	void Update () {
        if (CommonInformation.playersQueue.ContainsKey(hid))
        {
            while (CommonInformation.playersQueue[hid].Count > 0)
            {
                Message msg = (Message)CommonInformation.playersQueue[hid].Dequeue();
                if (msg.commandID == CommonInformation.MSG_SC_MOVETO)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    float x = CommonInformation.DeAmplify(br.ReadInt32());
                    float z = CommonInformation.DeAmplify(br.ReadInt32());
                    br.Close();
                    //Debug.Log(x +" " + z);
                    mPlayerMovement.CommandMove(x, z);
                }
                else if (msg.commandID == CommonInformation.MSG_SC_ROTATE)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    float y = CommonInformation.DeAmplify(br.ReadInt32());
                    mPlayerMovement.CommandRotate(y);
                    br.Close();
                }
                else if (msg.commandID == CommonInformation.MSG_SC_BEGIN)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int uid = br.ReadInt32();
                    string name = br.ReadString();
                    int maxhp = br.ReadInt32();
                    int hp = br.ReadInt32();
                    int lv = br.ReadInt32();
                    int nextExp = br.ReadInt32();
                    int exp = br.ReadInt32();
                    int money = br.ReadInt32();
                    int fire = br.ReadInt32();
                    int needle = br.ReadInt32();
                    br.Close();
                    CreatePlayer(uid, name, maxhp, hp, nextExp, exp, lv, money, fire, needle);

                }
                else if (msg.commandID == CommonInformation.MSG_SC_ENEMYCREATE)
                {
                    //eid, etype, x, z, hp
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int eid = br.ReadInt32();
                    int type = br.ReadInt32();
                    int x = br.ReadInt32();
                    int z = br.ReadInt32();
                    int hp = br.ReadInt32();
                    br.Close();
                    CreateEnemy(eid, type, CommonInformation.DeAmplify(x), CommonInformation.DeAmplify(z), hp);
                }
                else if (msg.commandID == CommonInformation.MSG_SC_ATTACKED)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int hp = br.ReadInt32();
                    br.Close();
                    mPlayerHealth.TakeDamage(hp);
                }
                else if (msg.commandID == CommonInformation.MSG_SC_FIRER)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    float x = CommonInformation.DeAmplify(br.ReadInt32());
                    float y = CommonInformation.DeAmplify(br.ReadInt32());
                    float z = CommonInformation.DeAmplify(br.ReadInt32());
                    br.Close();
                    mPlayerShoot.MagicShoot(new Vector3(x, y, z), hid);
                }
                else if (msg.commandID == CommonInformation.MSG_SC_FIREL)
                {
                    //Debug.Log("FireLeft------------------------------------------------------------------------" + hid);
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    float x = CommonInformation.DeAmplify(br.ReadInt32());
                    float y = CommonInformation.DeAmplify(br.ReadInt32());
                    float z = CommonInformation.DeAmplify(br.ReadInt32());
                    br.Close();
                    mPlayerShoot.FireShoot(new Vector3(x,y,z));
                }
                else if (msg.commandID == CommonInformation.MSG_SC_MONEY)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    CommonInformation.momey = br.ReadInt32();
                    CommonInformation.nextExp = br.ReadInt32();
                    CommonInformation.exp = br.ReadInt32();
                    CommonInformation.lv = br.ReadInt32();
                    br.Close();
                }
                else if (msg.commandID == CommonInformation.MSG_SC_TRAPCREATE)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int trapType = br.ReadInt32();
                    int damage = br.ReadInt32();
                    int slowdown = br.ReadInt32();
                    CommonInformation.fire = br.ReadInt32();
                    CommonInformation.needle = br.ReadInt32();
                    mTrapManager.putTrap(trapType, damage, slowdown, hid);
                    br.Close();
                }
                else if (msg.commandID == CommonInformation.MSG_SC_TRAPBUY)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    CommonInformation.momey = br.ReadInt32();
                    CommonInformation.fire = br.ReadInt32();
                    CommonInformation.needle = br.ReadInt32();
                    br.Close();
                }
            }
        }
        
    }

    private void CreatePlayer(int uid, string name, int maxhp, int hp, int nextExp, int exp, int lv, int money, int fire, int needle)
    {
        if (uid == hid) //self
        {
            CommonInformation.hp = maxhp;
            CommonInformation.maxhp = maxhp;
            CommonInformation.nextExp = nextExp;
            CommonInformation.exp = exp;
            CommonInformation.lv = lv;
            CommonInformation.momey = money;
            CommonInformation.fire = fire;
            CommonInformation.needle = needle;
            return; 
        }
        //Debug.Log(uid +"===================================="+ name);//new player
        GameObject player = GameObject.Instantiate(Player, CommonInformation.startPoint, transform.rotation) as GameObject;
        player.GetComponent<PlayerNetwork>().hid = uid;
        player.GetComponent<PlayerNetwork>().playername.text = name;
        player.GetComponent<PlayerHealth>().startingHealth = maxhp;
        CommonInformation.playersQueue.Add(uid, new Queue());
    }

    private void CreateEnemy(int eid, int etype, float x, float z, int hp)
    {
        //Debug.Log("Create Enemy----------------------------------");//new player
        GameObject enemy = null;
        if (etype == CommonInformation.ENEMY_BEAR)
        {
            enemy = GameObject.Instantiate(mBear, new Vector3(x, 0, z), transform.rotation) as GameObject;
        }
        else if (etype == CommonInformation.ENEMY_BUNNY)
        {
            enemy = GameObject.Instantiate(mBunny, new Vector3(x, 0, z), transform.rotation) as GameObject;
        }
        else
        {
            enemy = GameObject.Instantiate(mEllephant, new Vector3(x, 0, z), transform.rotation) as GameObject;
        }
        enemy.GetComponent<EnemyNetwork>().eid = eid;
        enemy.GetComponent<NEnemyHealth>().startingHealth = hp;
        enemy.GetComponent<NEnemyHealth>().currentHealth = hp;
        CommonInformation.enemysQueue.Add(eid, new Queue());
    }
}
