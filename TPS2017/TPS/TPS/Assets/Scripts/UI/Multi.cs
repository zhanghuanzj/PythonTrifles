using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class Multi : MonoBehaviour {

	// Use this for initialization
	void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    private void OnClick()
    {
        if (NetworkHandler.getNetHandlerInstance() != null)
        {
            NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_BEGIN, null);
        }
    }
}
