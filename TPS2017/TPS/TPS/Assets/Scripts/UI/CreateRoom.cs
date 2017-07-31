using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CreateRoom : MonoBehaviour {

    public InputField roomInputField;
    public static int result = -1;
    public Text message;
    public GameObject messageCanvas;
    public GameObject wailtingCanvas;
    public GameObject currentCanvas;
    // Use this for initialization
    void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    void Update()
    {
        if (result != -1)
        {
            if (result == CommonInformation.CREATEROOM_SUCCESS)
            {
                currentCanvas.SetActive(false);
                wailtingCanvas.SetActive(true);
                Debug.Log("Create Success");

            }
            else
            {
                Debug.Log("Create Failed");
                CommonMethod.ShowMessage(message, "创建失败", currentCanvas, messageCanvas);
            }
            result = -1;
        }
    }
    private void OnClick()
    {
        if (roomInputField.text !=null && roomInputField.text != "" )
        {
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_CREATEROOM, new ArrayList() { roomInputField.text });
            }
        }
        else
        {
            CommonMethod.ShowMessage(message, "请输入房间名！", currentCanvas, messageCanvas);
        }
    }
}
