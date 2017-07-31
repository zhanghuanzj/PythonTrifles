using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class EnterRoom : MonoBehaviour {

    public Dropdown dropdownItem;
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
            if (result == CommonInformation.ENTERROOM_SUCCESS)
            {
                currentCanvas.SetActive(false);
                wailtingCanvas.SetActive(true);
                Debug.Log("Enter Success");

            }
            else
            {
                Debug.Log("Enter Failed");
                CommonMethod.ShowMessage(message, "进入失败", currentCanvas, messageCanvas);
            }
            result = -1;
        }
    }
    private void OnClick()
    {
        if (dropdownItem.captionText.text != "")
        {
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_ENTERROOM, new ArrayList() { dropdownItem.captionText.text });
            }
        }
        
    }
}
