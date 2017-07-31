using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NEnemyShoot : MonoBehaviour
{

    public GameObject firePosition;
    public ParticleSystem gunParticles;


    private Animator mAnim;
    private float mTimer;
    private LineRenderer mLineRender;
    private float mEffectsDisplayTime = 0.05f;


    void Awake()
    {
        mAnim = GetComponent<Animator>();
        mLineRender = GetComponent<LineRenderer>();
    }



    void Update()
    {
        mTimer += Time.deltaTime;
        if (mTimer >= mEffectsDisplayTime)
        {
            mLineRender.enabled = false;
        }

        //mAnim.SetTrigger("PlayerDead");
    }


    public void Shoot(object[] obj)
    {
        mTimer = 0f;
        Vector3 pos = new Vector3((float)obj[0], 0.5f, (float)obj[1]);
        //射击效果
        gunParticles.transform.position = firePosition.transform.position;
        gunParticles.Play();
        mLineRender.enabled = true;
        mLineRender.SetPosition(0, firePosition.transform.position);
        mLineRender.SetPosition(1, pos);
    }
}

