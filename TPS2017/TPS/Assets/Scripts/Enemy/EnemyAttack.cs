using UnityEngine;
using System.Collections;

public class EnemyAttack : MonoBehaviour
{
    public float timeBetweenAttacks = 0.5f;
    public int attackDamage = 10;


    private Animator mAnim;
    private GameObject mPlayer;
    private PlayerHealth mPlayerHealth;
    private EnemyHealth mEnemyHealth;
    private bool mPlayerInRange;
    private float mTimer;


    void Awake ()
    {
        mPlayer = GameObject.FindGameObjectWithTag ("Player");
        mPlayerHealth = mPlayer.GetComponent <PlayerHealth> ();
        mEnemyHealth = GetComponent<EnemyHealth>();
        mAnim = GetComponent <Animator> ();
    }


    void OnTriggerEnter (Collider other)
    {
        if(other.gameObject == mPlayer)
        {
            mPlayerInRange = true;
        }
    }


    void OnTriggerExit (Collider other)
    {
        if(other.gameObject == mPlayer)
        {
            mPlayerInRange = false;
        }
    }


    void Update ()
    {
        mTimer += Time.deltaTime;

        if(mTimer >= timeBetweenAttacks && mPlayerInRange/* && enemyHealth.currentHealth > 0*/)
        {
            Attack ();
        }

        if(mPlayerHealth.currentHealth <= 0)
        {
            mAnim.SetTrigger ("PlayerDead");
        }
    }


    void Attack ()
    {
        mTimer = 0f;

        if(mPlayerHealth.currentHealth > 0)
        {
            mPlayerHealth.TakeDamage (attackDamage);
        }
    }
}
