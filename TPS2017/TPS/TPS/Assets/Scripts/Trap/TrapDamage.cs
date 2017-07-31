using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapDamage : MonoBehaviour
{
    public bool isHost;
    public int mDamage;
    public int mSlowdown;

    private float mAttackTime = 0.2f;

    private float mCurrentTime;
    private Rigidbody mRigidbody;
    private TrapDetect mTrapDetect;
    // Use this for initialization
    void Start()
    {
        mRigidbody = this.transform.parent.GetComponent<Rigidbody>();
        mTrapDetect = this.GetComponent<TrapDetect>();
    }

    void Update()
    {
        mCurrentTime += Time.deltaTime;
    }

    void FixedUpdate()
    {
        mRigidbody.velocity = new Vector3(0, 0, 0);
    }

    void OnTriggerEnter(Collider collider)
    {
        if (isHost)
        {
            if (mTrapDetect.isLocated && 1 << collider.gameObject.layer == LayerMask.GetMask("Enemy"))
            {
                Debug.Log("------------------------------------------------------------------");
                mCurrentTime = 0;
                int eid = collider.gameObject.GetComponent<EnemyNetwork>().eid;
                if (NetworkHandler.getNetHandlerInstance() != null)
                {
                    NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_TRAPATTACK, new ArrayList() { eid, mDamage, mSlowdown });
                }
            }
        }
    }
}
