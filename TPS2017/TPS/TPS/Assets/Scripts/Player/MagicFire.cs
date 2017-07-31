using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MagicFire : MonoBehaviour {
    public int hid;
    void OnTriggerEnter(Collider collider)
    {
        if (hid == CommonInformation.userhid && 1<<collider.gameObject.layer == LayerMask.GetMask("Enemy") )
        {
            int eid = collider.gameObject.GetComponent<EnemyNetwork>().eid;
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_AIMED, new ArrayList() { eid });
            }
            this.gameObject.SetActive(false);
        } 
    }
}
