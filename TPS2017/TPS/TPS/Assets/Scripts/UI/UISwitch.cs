using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UISwitch : MonoBehaviour {

    public GameObject currentObj;
    public GameObject nextObj;
	// Use this for initialization
	void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    private void OnClick()
    {
        currentObj.SetActive(false);
        nextObj.SetActive(true);
        
    }

}
