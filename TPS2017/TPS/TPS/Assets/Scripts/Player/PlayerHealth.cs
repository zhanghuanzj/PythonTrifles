using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class PlayerHealth : MonoBehaviour
{
    public int startingHealth = 100;
    public int currentHealth;
    public bool isHost;
    //public Image damageImage;
    public AudioClip deathClip;
    public float flashSpeed = 5f;
    public Color flashColour = new Color(1f, 0f, 0f, 0.1f);


    private Animator mAnimator;
    private AudioSource mPlayerAudio;
    private PlayerMovement mPlayerMovement;
    private PlayerShooting mPlayerShooting;
    private PlayerNetwork mPlayerNetwork;
    private bool mIsDead;
    private bool mDamaged;


    void Awake ()
    {
        mAnimator = GetComponent <Animator> ();
        mPlayerAudio = GetComponent <AudioSource> ();
        mPlayerMovement = GetComponent <PlayerMovement> ();
        mPlayerShooting = GetComponentInChildren <PlayerShooting> ();
        mPlayerNetwork = GetComponent<PlayerNetwork>();
        currentHealth = startingHealth;

    }


    void Update ()
    {
        //if(mDamaged)
        //{
        //    damageImage.color = flashColour;
        //}
        //else
        //{
        //    damageImage.color = Color.Lerp (damageImage.color, Color.clear, flashSpeed * Time.deltaTime);
        //}
        mDamaged = false;
        if (CommonInformation.isGameOver)
        {
            Death();
        }
    }


    public void TakeDamage (int hp) //受到攻击
    {
        //Debug.Log("HP:----------------------------------------" + hp);
        mDamaged = true;

        currentHealth = hp;

        if (isHost)
        {
            CommonInformation.hp = currentHealth;
        }
        

        mPlayerAudio.Play ();

        if(currentHealth <= 0 && !mIsDead)
        {
            Death ();
        }
    }


    void Death ()
    {
        mIsDead = true;

        mPlayerShooting.DisableEffects ();

        mAnimator.SetTrigger ("Die");

        mPlayerAudio.clip = deathClip;
        mPlayerAudio.Play ();

        mPlayerMovement.enabled = false;
        mPlayerShooting.enabled = false;
        mPlayerNetwork.enabled = false;
    }
}
