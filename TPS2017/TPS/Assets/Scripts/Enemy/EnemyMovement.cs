using UnityEngine;
using System.Collections;

public class EnemyMovement : MonoBehaviour
{
    private Transform mPlayer;
    private PlayerHealth mPlayerHealth;
    private EnemyHealth mEnemyHealth;
    UnityEngine.AI.NavMeshAgent mNav;


    void Awake ()
    {
        mPlayer = GameObject.FindGameObjectWithTag ("Player").transform;
        mPlayerHealth = mPlayer.GetComponent <PlayerHealth> ();
        mEnemyHealth = GetComponent <EnemyHealth> ();
        mNav = GetComponent <UnityEngine.AI.NavMeshAgent> ();
    }


    void Update ()
    {
        if(mEnemyHealth.currentHealth > 0 && mPlayerHealth.currentHealth > 0)
        {
            mNav.SetDestination (mPlayer.position);
        }
        else
        {
            mNav.enabled = false;
        }
    }
}
