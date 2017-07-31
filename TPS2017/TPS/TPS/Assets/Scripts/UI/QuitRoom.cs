using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class QuitRoom : MonoBehaviour {

    public GameObject currentCanvas;
    public GameObject nextCanvas;
	// Use this for initialization
	void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    private void OnClick()
    {
        currentCanvas.SetActive(false);
        nextCanvas.SetActive(true);
        if (NetworkHandler.getNetHandlerInstance() != null)
        {
            NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_QUITROOM, null);
        }
    }
}
