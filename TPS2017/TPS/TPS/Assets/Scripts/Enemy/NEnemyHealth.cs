using UnityEngine;
using UnityEngine.UI;

public class NEnemyHealth : MonoBehaviour
{
    public int startingHealth = 100;
    public int currentHealth;
    public float sinkSpeed = 2.5f;
    public AudioClip deathClip;
    public Slider healthSlider;
    public ParticleSystem mDeadParticles;


    Animator mAnimator;
    AudioSource mEnemyAudio;
    ParticleSystem mHitParticles;
    CapsuleCollider mCapsuleCollider;
    bool mIsDead;
    bool mIsSinking;


    void Awake()
    {
        mAnimator = GetComponent<Animator>();
        mEnemyAudio = GetComponent<AudioSource>();
        mHitParticles = GetComponentInChildren<ParticleSystem>();
        mCapsuleCollider = GetComponent<CapsuleCollider>();
    }


    void Update()
    {
        healthSlider.value = ((float)currentHealth)/startingHealth; //血条
        if (mIsSinking)
        {
            transform.Translate(-Vector3.up * sinkSpeed * Time.deltaTime);
        }
    }

    public void FireDamage(int hp, Vector3 hitPoint)
    {
        if (mIsDead)
            return;
        mHitParticles.transform.position = hitPoint;
        currentHealth = hp;
        mEnemyAudio.Play();
        //mHitParticles.transform.Rotate(0,180,0);
        //mHitParticles.transform.LookAt(-GameObject.FindGameObjectWithTag("Player").transform.position);
        mHitParticles.Play();

        if (currentHealth <= 0)
        {
            Death();
        }
    }

    public void MagicDamage(int hp)
    {
        
        if (mIsDead)
            return;

        currentHealth = hp;
        mEnemyAudio.Play();

        if (currentHealth <= 0)
        {
            Death();
        }
    }


    void Death()
    {
        mIsDead = true;

        mCapsuleCollider.isTrigger = true;

        mAnimator.SetTrigger("Dead");

        mEnemyAudio.clip = deathClip;
        mEnemyAudio.Play();
        mDeadParticles.Play();
        StartSinking();
    }


    public void StartSinking()
    {
        GetComponent<Rigidbody>().isKinematic = true;
        mIsSinking = true;
        //ScoreManager.score += scoreValue;
        Destroy(gameObject, 2f);
    }
}
