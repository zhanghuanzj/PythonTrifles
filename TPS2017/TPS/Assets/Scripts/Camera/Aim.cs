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
        Physics.Raycast(mCamera.transform.position, mCamera.transform.forward, out hitInfo);
        Vector3 pos = Camera.main.WorldToScreenPoint(hitInfo.point);
        if (Physics.Raycast(mCamera.transform.position, mCamera.transform.forward, out hitInfo, LayerMask.GetMask("Shootable")))
        {
            CommonInformation.shootable = true;
            CommonInformation.shootHit = hitInfo;
        }
        else
        {
            CommonInformation.shootable = false;
        }

        //准心绘制
        Rect rect = new Rect(pos.x - (texture.width / 2),
        Screen.height - pos.y - (texture.height / 2),
        texture.width, texture.height);
        GUI.DrawTexture(rect, texture);

    }
}
