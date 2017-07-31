using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Register : MonoBehaviour {

    public InputField uInputField;
    public InputField pInputField;
    public InputField pcInputField;
    public Text message;
    public GameObject messageCanvas;
    public GameObject currentCanvas;
    public static int result = -1;

    // Use this for initialization
    void Start()
    {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    void Update()
    {
        if (result != -1)
        {
            if (result == CommonInformation.REGISTER_SUCCESS)
            {
                Debug.Log("Register Success");
                message.text = "注册成功";    
            }
            else
            {
                Debug.Log("Register Failed");
                message.text = "注册失败";
            }
            CommonMethod.ShowMessage(message, message.text, currentCanvas, messageCanvas);
            result = -1;
        }
    }

    private void OnClick()
    {
        string username = uInputField.text;
        string password = pInputField.text;
        string pcheck = pcInputField.text;
        if(password == pcheck)
        {
            ArrayList loginInfo = new ArrayList() { username, password };
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_REGISTER, loginInfo);
            }
        }
        else
        {
            message.text = "密码不一致";
            messageCanvas.SetActive(true);
        }
    }
}
