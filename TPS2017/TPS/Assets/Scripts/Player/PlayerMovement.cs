using System.IO;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float mSpeed = 3.0f;
    public GameObject RotateAxis;
    private Animator mAnimator;
    private Rigidbody mRigidbody;
    private MouseLookView mouseLook = new MouseLookView();
    private int mAmplify = 100;

    long currentTime = System.DateTime.Now.Ticks;
    void Awake()
    {
        mAnimator = this.GetComponent<Animator>();
        mRigidbody = this.GetComponent<Rigidbody>();
        mouseLook.Init(this.transform, RotateAxis.transform);
    }

    void Update()
    {
        CommandHandle();
        Move();
        RotateView();
        
        long cur = System.DateTime.Now.Ticks;
        //Debug.Log(10000000 / (cur - currentTime)+"FPS");
        currentTime = cur;
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
            NetworkHandler.getNetHandlerInstance().sendMoveMSG(NetworkHandler.MSG_CS_MOVETO, (int)(pos.x * mAmplify), (int)(pos.z * mAmplify));

            mAnimator.SetBool("IsWalking", true);
        }
        else
        {
            mAnimator.SetBool("IsWalking", false);
        }
    }

    private void RotateView()
    {
        //avoids the mouse looking if the game is effectively paused
        if (Mathf.Abs(Time.timeScale) < float.Epsilon) return;

        mouseLook.LookRotation(this.transform, RotateAxis.transform);

    }

    private void CommandHandle()
    {
        //Debug.Log(CommonInformation.playerCommandQueue.Count > 0);
        if (CommonInformation.playerCommandQueue.Count>0)
        {
            Message msg = (Message)CommonInformation.playerCommandQueue.Dequeue();
            //Debug.Log(msg.commandID == NetworkHandler.MSG_SC_MOVETO);
            if(msg.commandID == NetworkHandler.MSG_SC_MOVETO)
            {
                BinaryReader br = new BinaryReader(new MemoryStream(msg.data));
                float x = (float)br.ReadInt32()/mAmplify;
                float z = (float)br.ReadInt32()/mAmplify;
                //Debug.Log("Queue"+x + " " + z);
                Vector3 pos = new Vector3(x, transform.position.y, z);
                mRigidbody.transform.position = Vector3.Lerp(transform.position, pos, 40 * Time.deltaTime);
                Debug.Log(40 * Time.deltaTime);
                //mRigidbody.MovePosition(pos);
            }
        }
        
    }
}

