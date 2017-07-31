using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Aim : MonoBehaviour {

    public Texture2D texture;
    public GameObject firePosition;
    private Camera mCamera;
    private Transform mPlayer;
    // Use this for initialization
    private void Start()
    {
        mCamera = this.GetComponent<Camera>();
        mPlayer = GameObject.FindGameObjectWithTag("Player").transform;
    }
    void OnGUI()
    {

        RaycastHit hitInfo = new RaycastHit();
        Physics.Raycast(mCamera.transform.position, mCamera.transform.forward, out hitInfo,100);
        //Debug.Log(hitInfo.point);
        CommonInformation.shootHit = hitInfo;

        //准心绘制
        Rect rect = new Rect(Screen.width/2 - (texture.width / 2),
        Screen.height/2 - (texture.height / 2),
        texture.width, texture.height);
        GUI.DrawTexture(rect, texture);
        

    }
}
