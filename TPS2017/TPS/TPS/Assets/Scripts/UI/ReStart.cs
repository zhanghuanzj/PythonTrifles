using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class ReStart : MonoBehaviour {

	// Use this for initialization
	void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
        if (!CommonInformation.isHost)
        {
            btn.gameObject.SetActive(false);
        }
    }

    private void OnClick()
    {
        Debug.Log("Click-------------------------------------------");
        if (NetworkHandler.getNetHandlerInstance() != null)
        {
            NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_BEGIN, null);
        }
    }
}
