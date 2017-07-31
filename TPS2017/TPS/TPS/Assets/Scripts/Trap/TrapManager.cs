using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapManager : MonoBehaviour {

    public bool isHost;
    public GameObject fireTrap;
    public GameObject needleTrap;
    public Texture fireTexture2;
    public Texture needleTexture2;

    private GameObject trap;
    public Texture fireTexture1;
    public Texture needleTexture1;


    // Use this for initialization
    void Start () {

    }
	
	// Update is called once per frame
	void Update () {
        if (!isHost)
        {
            return;
        }
        if (this.transform.childCount == 0 )
        {
            if (Input.GetKeyDown(KeyCode.Tab))
            {
                CommonInformation.isFireTrap = !CommonInformation.isFireTrap;
            }
                if (Input.GetKeyDown(KeyCode.Q) && IsCurrentEnough())
            {
                Debug.Log("Create--------------------------------------------------------------------------------------------------------------");
                createTrap();
            }
           
        }
        else
        {
            if (Input.GetKeyDown(KeyCode.Q))
            {
                GameObject.Destroy(trap);
            }
            else if (Input.GetKeyDown(KeyCode.Tab))
            {
                CommonInformation.isFireTrap = !CommonInformation.isFireTrap;
                GameObject.Destroy(trap);
                createTrap();
            }
            else
            {
                if (trap.GetComponentInChildren<TrapDetect>().isCollide)
                {
                    ForbidTexture();
                }
                else
                {
                    NormalTexture();
                    if (Input.GetKeyDown(KeyCode.Space))
                    {
                        GameObject.Destroy(trap);
                        int trapType = CommonInformation.NEEDLE_TRAP;
                        if (CommonInformation.isFireTrap)
                        {
                            trapType = CommonInformation.FIRE_TRAP;
                        }
                        if (NetworkHandler.getNetHandlerInstance() != null)
                        {
                            NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_TRAPCREATE, new ArrayList() { trapType });
                        }
                    }
                }
            }  
        }
    }

    public void putTrap(int trapType, int damage, int slowdown,int hid)
    {
        if (damage == 0)
        {
            return;//no money
        }
        GameObject newTrap;
        if (trapType == CommonInformation.FIRE_TRAP)
        {
            newTrap = GameObject.Instantiate(fireTrap, this.transform.position, transform.rotation) as GameObject;
        }
        else
        {
            newTrap = GameObject.Instantiate(needleTrap, this.transform.position, transform.rotation) as GameObject;
        }
        newTrap.GetComponent<Rigidbody>().useGravity = true;
        newTrap.GetComponent<BoxCollider>().enabled = true;
        newTrap.GetComponentInChildren<TrapDetect>().isLocated = true;
        newTrap.GetComponentInChildren<TrapDamage>().mDamage = damage;
        newTrap.GetComponentInChildren<TrapDamage>().mSlowdown = slowdown;
    }

    private GameObject getCurrent()
    {
        if (CommonInformation.isFireTrap)
        {
            return fireTrap;
        }
        else
        {
            return needleTrap;
        }
    }

    private void createTrap()
    {
        trap = GameObject.Instantiate(getCurrent(), this.transform.position, transform.rotation) as GameObject;
        trap.transform.parent = this.transform;
    }

    private void ForbidTexture()
    {
        if (CommonInformation.isFireTrap)
        {
            trap.GetComponent<Renderer>().material.mainTexture =  fireTexture2;
        }
        else
        {
            trap.GetComponentInChildren<Renderer>().material.mainTexture =  needleTexture2;
        }
    }

    private void NormalTexture()
    {
        if (CommonInformation.isFireTrap)
        {
            trap.GetComponent<Renderer>().material.mainTexture =  fireTexture1;
        }
        else
        {
            trap.GetComponentInChildren<Renderer>().material.mainTexture = needleTexture1;
        }
    }

    private bool IsCurrentEnough()
    {
        if (CommonInformation.isFireTrap)
        {
            return CommonInformation.fire > 0;
        }
        else
        {
            return CommonInformation.needle > 0;
        }
    }
}
