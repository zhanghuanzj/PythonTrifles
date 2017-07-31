using System.Collections;
using System.IO;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float mSpeed = 3.0f;
    public GameObject RotateAxis;
    public bool isHost;
    private Animator mAnimator;
    private Rigidbody mRigidbody;
    private MouseLookView mouseLook = new MouseLookView();

    private long currentTime = System.DateTime.Now.Ticks;
    private bool isMove = false;
    void Awake()
    {
        mAnimator = this.GetComponent<Animator>();
        mRigidbody = this.GetComponent<Rigidbody>();  
    }

    void Start()
    {
        if (isHost)
        {
            mouseLook.Init(this.transform, RotateAxis.transform);
        }
        else
        {
            mouseLook.Init(this.transform, Camera.main.transform);
        }
        
    }

    void Update()
    {
        if (isHost)
        {
            Move();
            RotateView();
        }
        if(isMove)
        {
            mAnimator.SetBool("IsWalking", true);
            isMove = false;
        }
        else
        {
            mAnimator.SetBool("IsWalking", false);
        }
        
        long cur = System.DateTime.Now.Ticks;
        //Debug.Log(10000000 / (cur - currentTime)+"FPS");
        currentTime = cur;
    }

    void FixedUpdate()
    {
        mRigidbody.velocity = new Vector3(0, 0, 0);
    }
    void Move()
    {
        int h = 0;
        int v = 0;
        if (Input.GetKey(KeyCode.W))
        {
            v += 1;
        }
        if (Input.GetKey(KeyCode.S))
        {
            v -= 1;
        }
        if (Input.GetKey(KeyCode.A))
        {
            h -= 1;
        }
        if (Input.GetKey(KeyCode.D))
        {
            h += 1;
        }
        if(h!=0 || v!=0)
        {
            Vector3 moveDirection = (new Vector3(h, 0, v).normalized) * mSpeed * Time.deltaTime;
            moveDirection = transform.TransformDirection(moveDirection);
            Vector3 pos = transform.position + moveDirection;
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_MOVETO, new ArrayList() { CommonInformation.Amplify(pos.x), CommonInformation.Amplify(pos.z) });
            }
        }
    }

    private void RotateView()
    {
        //avoids the mouse looking if the game is effectively paused
        if (Mathf.Abs(Time.timeScale) < float.Epsilon) return;

        float yRot = mouseLook.LookRotation(RotateAxis.transform);
        if (System.Math.Abs(yRot) != float.Epsilon)//need syn
        {
            ArrayList data = new ArrayList() { CommonInformation.Amplify(yRot) };
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_ROTATE, data);
            }
        }
    }

    public void CommandMove(float x,float z)
    {
        isMove = true;
        Vector3 pos = new Vector3(x, transform.position.y, z);
        mRigidbody.transform.position = Vector3.Lerp(transform.position, pos, 40 * Time.deltaTime);
    }

    public void CommandRotate(float y)
    {
        mouseLook.playerRotate(y, this.transform);
    }
}

