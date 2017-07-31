using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class Single : MonoBehaviour {

	// Use this for initialization
	void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    void Update()
    {
        if (CommonInformation.isGameBegin)
        {
            CommonInformation.isGameBegin = false;
            SceneManager.LoadScene("MainScene");
        }
    }
    private void OnClick()
    {
        if (NetworkHandler.getNetHandlerInstance() != null)
        {
            NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_BEGIN, null);
        }
    }
}
