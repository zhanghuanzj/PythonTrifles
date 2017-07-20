using UnityEngine;
using UnityEngine.UI;

public class EnemyHealth : MonoBehaviour
{
    public int startingHealth = 100;
    public int currentHealth;
    public float sinkSpeed = 2.5f;
    public int scoreValue = 10;
    public AudioClip deathClip;
    public Slider healthSlider;


    Animator mAnimator;
    AudioSource mEnemyAudio;
    ParticleSystem mHitParticles;
    CapsuleCollider mCapsuleCollider;
    bool mIsDead;
    bool mIsSinking;


    void Awake ()
    {
        mAnimator = GetComponent <Animator> ();
        mEnemyAudio = GetComponent <AudioSource> ();
        mHitParticles = GetComponentInChildren <ParticleSystem> ();
        mCapsuleCollider = GetComponent <CapsuleCollider> ();

        currentHealth = startingHealth;
    }


    void Update ()
    {
        if(mIsSinking)
        {
            transform.Translate (-Vector3.up * sinkSpeed * Time.deltaTime);
        }
    }


    public void TakeDamage (int amount, Vector3 hitPoint)
    {
        if(mIsDead)
            return;

        mEnemyAudio.Play ();

        currentHealth -= amount;
        healthSlider.value = currentHealth; //血条
        mHitParticles.transform.position = hitPoint;
        //mHitParticles.transform.Rotate(0,180,0);
        //mHitParticles.transform.LookAt(-GameObject.FindGameObjectWithTag("Player").transform.position);
        mHitParticles.Play();

        if(currentHealth <= 0)
        {
            Death ();
        }
    }


    void Death ()
    {
        mIsDead = true;

        mCapsuleCollider.isTrigger = true;

        mAnimator.SetTrigger ("Dead");

        mEnemyAudio.clip = deathClip;
        mEnemyAudio.Play ();
    }


    public void StartSinking ()
    {
        GetComponent <UnityEngine.AI.NavMeshAgent> ().enabled = false;
        GetComponent <Rigidbody> ().isKinematic = true;
        mIsSinking = true;
        ScoreManager.score += scoreValue;
        Destroy (gameObject, 2f);
    }
}
