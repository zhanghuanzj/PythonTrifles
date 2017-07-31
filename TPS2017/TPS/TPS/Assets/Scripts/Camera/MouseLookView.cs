using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseLookView {

    public float XSensitivity = 2f;
    public float YSensitivity = 2f;
    public bool clampVerticalRotation = true;
    public float MinimumX = -40F;
    public float MaximumX = 40F;
    public bool smooth = true;
    public float smoothTime = 5f;
    public bool lockCursor = true;  //flag to adjust the cursor


    private Quaternion m_CharacterTargetRot;
    private Quaternion m_CameraTargetRot;
    private bool m_cursorIsLocked = true;   //show the cursor is visible
    private float m_MaxDistance = 4.0f;
    private float m_MinDistance = 3.0f;


    public void Init(Transform character, Transform camera)
    {
        m_CharacterTargetRot = character.localRotation;
        m_CameraTargetRot = camera.localRotation;
    }


    public float LookRotation(Transform rotateAxis)
    {
        float yRot = Input.GetAxis("Mouse X") * XSensitivity;
        float xRot = Input.GetAxis("Mouse Y") * YSensitivity;

        m_CameraTargetRot *= Quaternion.Euler(-xRot, 0f, 0f); //positive is rotate down,left or right rotate with character

        if (clampVerticalRotation)
            m_CameraTargetRot = ClampRotationAroundXAxis(m_CameraTargetRot);

        if (!CommonInformation.isGameOver)
        {
            //非暂停，非死亡
            if (smooth)//rotate smoothly
            {
                rotateAxis.localRotation = Quaternion.Slerp(rotateAxis.localRotation, m_CameraTargetRot, smoothTime * Time.deltaTime);//Verticle
            }
            else
            {
                rotateAxis.localRotation = m_CameraTargetRot;
            }
        }
        return yRot; 
    }

    public void playerRotate(float yRot, Transform character)
    {
        m_CharacterTargetRot *= Quaternion.Euler(0f, yRot, 0f);
        if (smooth)//rotate smoothly
        {
            character.localRotation = Quaternion.Slerp(character.localRotation, m_CharacterTargetRot, smoothTime * Time.deltaTime);    
        }
        else
        {
            character.localRotation = m_CharacterTargetRot;
        }
    }

    Quaternion ClampRotationAroundXAxis(Quaternion q)
    {

        q.x /= q.w;
        //q.y /= q.w;
        q.z = 0.0f;
        q.w = 1.0f;

        float angleX = 2.0f * Mathf.Rad2Deg * Mathf.Atan(q.x);

        angleX = Mathf.Clamp(angleX, MinimumX, MaximumX);

        q.x = Mathf.Tan(0.5f * Mathf.Deg2Rad * angleX);

        return q;
    }

}
