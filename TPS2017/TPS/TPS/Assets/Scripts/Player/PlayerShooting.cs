using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class PlayerShooting : MonoBehaviour
{
    public int damagePerShot = 20;
    public float timeBetweenBullets = 0.15f;
    public float range = 100f;
    public bool isHost;

    public ParticleSystem gunParticles;
    public GameObject firePosition;
    public GameObject magicFire;
    public Transform toward;

    float mFireTimer;
    float mMagicTimer;
    float mMagicCD = 5.0f;
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
        mFireTimer += Time.deltaTime;
        mMagicTimer += Time.deltaTime;
        if (isHost)
        {
            shootHit = CommonInformation.shootHit;
            if (Input.GetButton("Fire1") && mFireTimer >= timeBetweenBullets)
            {
                mFireTimer = 0f;
                if (NetworkHandler.getNetHandlerInstance()!=null)
                {
                    NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_FIREL, new ArrayList() { CommonInformation.Amplify(shootHit.point.x), CommonInformation.Amplify(shootHit.point.y), CommonInformation.Amplify(shootHit.point.z) });
                }
                
            }
            if (Input.GetButton("Fire2") && mMagicTimer >= mMagicCD)
            {
                mMagicTimer = 0f;
                if (NetworkHandler.getNetHandlerInstance() != null)
                {
                    NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_FIRER, new ArrayList() { CommonInformation.Amplify(shootHit.point.x), CommonInformation.Amplify(shootHit.point.y), CommonInformation.Amplify(shootHit.point.z) });
                }
            }
            CommonInformation.cd = mMagicTimer / mMagicCD;
        }
        if (mFireTimer >= timeBetweenBullets * effectsDisplayTime)
        {
            DisableEffects ();
        }

    }


    public void DisableEffects ()
    {
        gunLine.enabled = false;
        gunLight.enabled = false;
    }


    public void FireShoot (Vector3 target)
    {
        gunAudio.Play ();

        gunLight.enabled = true;

        gunParticles.Stop ();
        gunParticles.Play ();

        gunLine.enabled = true;
        gunLine.SetPosition (0, firePosition.transform.position);

        shootRay.origin = firePosition.transform.position;
        shootRay.direction = toward.transform.forward;
        if (isHost)
        {
            if (1 << shootHit.collider.gameObject.layer == LayerMask.GetMask("Enemy"))
            {
                int eid = shootHit.collider.gameObject.GetComponent<EnemyNetwork>().eid;
                if (NetworkHandler.getNetHandlerInstance() != null)
                {
                    NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_AIMEDLEFT, new ArrayList() { eid, CommonInformation.Amplify(target.x), CommonInformation.Amplify(target.y), CommonInformation.Amplify(target.z) });
                }
            }
        }
       
        gunLine.SetPosition(1, target);
        //gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);
        
    }

    public void MagicShoot(Vector3 target, int hid)
    {
        gunAudio.Play();

        float angle = 5.0f;
        float speed = 100.0f;
        GameObject fire1 = GameObject.Instantiate(magicFire, firePosition.transform.position, transform.rotation) as GameObject; //new Quaternion(0,0,0,0)
        GameObject fire2 = GameObject.Instantiate(magicFire, firePosition.transform.position, transform.rotation) as GameObject;
        GameObject fire3 = GameObject.Instantiate(magicFire, firePosition.transform.position, transform.rotation) as GameObject;

        fire1.GetComponent<Rigidbody>().AddForce((target - firePosition.transform.position) * speed);
        fire2.GetComponent<Rigidbody>().AddForce(Quaternion.AngleAxis(angle, new Vector3(0, 1, 0)) * (target - firePosition.transform.position) * speed);
        fire3.GetComponent<Rigidbody>().AddForce(Quaternion.AngleAxis(-angle, new Vector3(0, 1, 0)) * (target - firePosition.transform.position) * speed);

        fire1.GetComponent<MagicFire>().hid = hid;
        fire2.GetComponent<MagicFire>().hid = hid;
        fire3.GetComponent<MagicFire>().hid = hid;

        GameObject.Destroy(fire1, 3f);
        GameObject.Destroy(fire2, 3f);
        GameObject.Destroy(fire3, 3f);
    }
}
