using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NEnemyMove : MonoBehaviour {
    private Rigidbody mRigidbody;
    private Animator mAnimator;
    // Use this for initialization
    void Start () {
        mRigidbody = this.GetComponent<Rigidbody>();
        mAnimator = this.GetComponent<Animator>();
    }
	
	// Update is called once per frame
	void Update () {
        if (CommonInformation.isGameOver)
        {
            mAnimator.SetTrigger("PlayerDead");
        }
	}

    void FixedUpdate()
    {
        mRigidbody.velocity = new Vector3(0, 0, 0);
    }

    public void CommandMove(float x, float z)
    {
        Vector3 pos = new Vector3(x, transform.position.y, z);
        if ( pos != transform.position)
        {
            this.transform.forward = pos - transform.position;
        }
        mRigidbody.transform.position = Vector3.Lerp(transform.position, pos, 20 * Time.deltaTime);
    }
}
