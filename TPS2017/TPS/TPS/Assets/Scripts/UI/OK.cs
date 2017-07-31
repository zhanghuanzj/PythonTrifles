using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class OK : MonoBehaviour {

    public GameObject messageCanvas;
    public Text messageText;

    public static GameObject preCanvas;
	// Use this for initialization
	void Start () {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(OnClick);
    }

    private void OnClick()
    {
        preCanvas.SetActive(true);
        messageCanvas.SetActive(false);
    }

}
