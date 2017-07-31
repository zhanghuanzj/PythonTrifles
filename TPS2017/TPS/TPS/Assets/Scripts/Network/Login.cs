using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Login : MonoBehaviour {

    public InputField uInputField;
    public InputField pInputField;
    public Text message;
    public GameObject messageCanvas;
    public GameObject gameModeCanvas;
    public GameObject currentCanvas;
    public static int result = -1;
	// Use this for initialization
	void Start ()
    {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    void Update()
    {
        if (result != -1)
        {
            if (result == CommonInformation.LOGIN_SUCCESS)
            {
                currentCanvas.SetActive(false);
                gameModeCanvas.SetActive(true);
                Debug.Log("Success");
            }
            else
            {
                Debug.Log("Failed");
                CommonMethod.ShowMessage(message, "登陆失败", currentCanvas, messageCanvas);
            }
            result = -1;
        }
    }

    private void OnClick()
    {
        string username = uInputField.text;
        string password = pInputField.text;
        CommonInformation.username = username;
        ArrayList loginInfo = new ArrayList() { username, password };
        if (NetworkHandler.getNetHandlerInstance() != null)
        {
            NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_LOGIN, loginInfo);
        }
    }


}
