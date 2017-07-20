using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class PlayerHealth : MonoBehaviour
{
    public int startingHealth = 100;
    public int currentHealth;
    public Slider healthSlider;
    //public Image damageImage;
    public AudioClip deathClip;
    public float flashSpeed = 5f;
    public Color flashColour = new Color(1f, 0f, 0f, 0.1f);


    private Animator mAnimator;
    private AudioSource mPlayerAudio;
    private PlayerMovement mPlayerMovement;
    private PlayerShooting mPlayerShooting;
    private bool mIsDead;
    private bool mDamaged;


    void Awake ()
    {
        mAnimator = GetComponent <Animator> ();
        mPlayerAudio = GetComponent <AudioSource> ();
        mPlayerMovement = GetComponent <PlayerMovement> ();
        mPlayerShooting = GetComponentInChildren <PlayerShooting> ();
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
    }


    public void TakeDamage (int amount) //受到攻击
    {
        mDamaged = true;

        currentHealth -= amount;

        healthSlider.value = currentHealth;

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
    }
}
