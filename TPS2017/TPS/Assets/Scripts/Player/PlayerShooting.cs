using UnityEngine;

public class PlayerShooting : MonoBehaviour
{
    public int damagePerShot = 20;
    public float timeBetweenBullets = 0.15f;
    public float range = 100f;

    public ParticleSystem gunParticles;
    public GameObject firePosition;
    public Transform toward;

    float timer;
    Ray shootRay;
    RaycastHit shootHit;
    int shootableMask;   
    LineRenderer gunLine;
    AudioSource gunAudio;
    Light gunLight;
    float effectsDisplayTime = 0.2f;


    void Awake ()
    {
        shootableMask = LayerMask.GetMask ("Shootable");
        gunLine = GetComponent <LineRenderer> ();
        gunAudio = GetComponent<AudioSource> ();
        gunLight = GetComponent<Light> ();
    }


    void Update ()
    {
        timer += Time.deltaTime;

        if(Input.GetButton ("Fire1") && timer >= timeBetweenBullets)
        {
            Shoot ();
        }

        if(timer >= timeBetweenBullets * effectsDisplayTime)
        {
            DisableEffects ();
        }
    }


    public void DisableEffects ()
    {
        gunLine.enabled = false;
        gunLight.enabled = false;
    }


    void Shoot ()
    {
        timer = 0f;

        gunAudio.Play ();

        gunLight.enabled = true;

        gunParticles.Stop ();
        gunParticles.Play ();

        gunLine.enabled = true;
        gunLine.SetPosition (0, firePosition.transform.position);

        shootRay.origin = firePosition.transform.position;
        shootRay.direction = toward.transform.forward;

        if(CommonInformation.shootable)
        {
            shootHit = CommonInformation.shootHit;
            EnemyHealth enemyHealth = shootHit.collider.GetComponent<EnemyHealth>();
            if (enemyHealth != null)
            {
                enemyHealth.TakeDamage(damagePerShot, shootHit.point);
            }
            gunLine.SetPosition(1, shootHit.point);
        }
        else
        {
            gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);
        }
        //if (Physics.Raycast (shootRay, out shootHit, range, shootableMask))
        //{
        //    EnemyHealth enemyHealth = shootHit.collider.GetComponent <EnemyHealth> ();
        //    if(enemyHealth != null)
        //    {
        //        enemyHealth.TakeDamage (damagePerShot, shootHit.point);
        //    }
        //    gunLine.SetPosition (1, shootHit.point);
        //}
        //else
        //{
        //    gunLine.SetPosition (1, shootRay.origin + shootRay.direction * range);
        //}
    }
}
