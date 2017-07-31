using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class EnemyNetwork : MonoBehaviour {
    public int eid;
    private NEnemyMove mEnemyMovement;
    private NEnemyHealth mEnemyHealth;
    // Use this for initialization
    void Start () {
		mEnemyMovement = GetComponent<NEnemyMove>();
        mEnemyHealth = GetComponent<NEnemyHealth>();
    }

    // Update is called once per frame
    void Update()
    {
        if (CommonInformation.enemysQueue.ContainsKey(eid))
        {
            while (CommonInformation.enemysQueue[eid].Count > 0)
            {
                Message msg = (Message)CommonInformation.enemysQueue[eid].Dequeue();
                if (msg.commandID == CommonInformation.MSG_SC_EMOVETO)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    float x = CommonInformation.DeAmplify(br.ReadInt32());
                    float z = CommonInformation.DeAmplify(br.ReadInt32());
                    //Debug.Log(x + " " + z);
                    mEnemyMovement.CommandMove(x, z);
                }
                else if (msg.commandID == CommonInformation.MSG_SC_ENEMYARRIVE)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int x = br.ReadInt32();
                    CommonInformation.score = x;
                    this.gameObject.SetActive(false);
                }
                else if (msg.commandID == CommonInformation.MSG_SC_ENEMYATTACK)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    float x = CommonInformation.DeAmplify(br.ReadInt32());
                    float z = CommonInformation.DeAmplify(br.ReadInt32());
                    this.transform.forward = new Vector3(x, 0, z);
                    if (this.gameObject.tag == "Bear")
                    {
                        this.gameObject.GetComponent<NEnemyShoot>().SendMessage("Shoot", new object[] { x, z });
                    }
                }
                else if (msg.commandID == CommonInformation.MSG_SC_AIMED || (msg.commandID == CommonInformation.MSG_SC_TRAPATTACK))
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int hp = br.ReadInt32();
                    mEnemyHealth.MagicDamage(hp);
                    Debug.Log("Trap attack------------------------------------------");
                }
                else if (msg.commandID == CommonInformation.MSG_SC_AIMEDLEFT)
                {
                    BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                    int hp = br.ReadInt32();
                    float x = CommonInformation.DeAmplify(br.ReadInt32());
                    float y = CommonInformation.DeAmplify(br.ReadInt32());
                    float z = CommonInformation.DeAmplify(br.ReadInt32());
                    mEnemyHealth.FireDamage(hp, new Vector3(x, y, z));
                }
            }
        }
       
    }
}
