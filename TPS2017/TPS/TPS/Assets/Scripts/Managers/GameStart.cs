using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameStart : MonoBehaviour {

    public GameObject PlayerMode;
    //public GameObject PlayerOther;
    public Image CD;
    public Slider healthSlider;
    public Slider expSlider;
    public GameObject gameOverCanvas;
    public Text enemyArrived;
    public Text momey;
    public Text fire;
    public Text needle;
    public Text lv;

    public Text gameResult;
    public Text count;

    public RawImage fireTrap;

    public RawImage needleTrap;


    private bool cursorIsLocked = true;
    private bool isShow = false;
    private float time = 0;
    void Awake()
    {
        CreatePlayer();
    }

    private void CreatePlayer()
    {
        GameObject player = GameObject.Instantiate(PlayerMode, CommonInformation.startPoint, transform.rotation) as GameObject;
        player.GetComponent<PlayerNetwork>().hid = CommonInformation.userhid;
        player.GetComponent<PlayerNetwork>().playername.text = CommonInformation.username;
    }
	// Use this for initialization
	void Start () {

    }
	
	// Update is called once per frame
	void Update () {
        CD.fillAmount = CommonInformation.cd;
        healthSlider.value = ((float)CommonInformation.hp)/ CommonInformation.maxhp;
        expSlider.value = ((float)CommonInformation.exp) / CommonInformation.nextExp;
        enemyArrived.text = "" + CommonInformation.score;
        momey.text = "$ " + CommonInformation.momey;
        fire.text = "X" + CommonInformation.fire;
        needle.text = "X" + CommonInformation.needle;
        lv.text = "LV:"+CommonInformation.lv;

        if (CommonInformation.isFireTrap)
        {
            fireTrap.GetComponent<RawImage>().color = Color.white;
            needleTrap.GetComponent<RawImage>().color = Color.grey;
        }
        else
        {
            fireTrap.GetComponent<RawImage>().color = Color.grey;
            needleTrap.GetComponent<RawImage>().color = Color.white;
        }


        InternalLockUpdate();
        if (CommonInformation.isGameOver && !isShow)
        {
            isShow = true;
            gameOverCanvas.SetActive(true);
        }
        if (CommonInformation.isGameWin && !isShow)
        {
            Debug.Log("WIN_______________________________________________________________");
            gameResult.text = "YOU WIN!";
            isShow = true;
            gameOverCanvas.SetActive(true);
        }

        if (CommonInformation.isGameBegin)
        {
            CommonInformation.isGameBegin = false;
            CommonInformation.Clean();
            SceneManager.LoadScene("Test");
        }
        TrapBuy();
        CountDown();
    }

    private void InternalLockUpdate()//cursor state adjust
    {

        if (Input.GetKeyUp(KeyCode.Escape) || CommonInformation.isGameOver || CommonInformation.isGameWin)
        {
            cursorIsLocked = false;
        }
        else if (Input.GetMouseButtonUp(0)) //left click
        {
            cursorIsLocked = true;
        }

        if (cursorIsLocked) //invisible
        {
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }
        else if (!cursorIsLocked)
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }
    }

    private void TrapBuy()
    {
        if (Input.GetKeyDown(KeyCode.E))
        {
            int ttype = CommonInformation.NEEDLE_TRAP;
            if (CommonInformation.isFireTrap)
            {
                ttype = CommonInformation.FIRE_TRAP;
            }
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_TRAPBUY, new ArrayList() { ttype });
            }
        }
    }

    private void CountDown()
    {
        if (CommonInformation.countDown >= 0)
        {
            count.gameObject.SetActive(true);
            count.text = "" + CommonInformation.countDown;
            time += Time.deltaTime;
            if (time >= 1.0)
            {
                time = 0;
                CommonInformation.countDown -= 1;
            }
        }
        else
        {
            time = 0;
            count.gameObject.SetActive(false);
        }
    }
}
