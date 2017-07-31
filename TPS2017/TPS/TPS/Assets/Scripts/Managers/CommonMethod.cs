using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CommonMethod  {

	public static void ShowMessage(Text message, string mess, GameObject current, GameObject messageCanvas)
    {
        message.text = mess;
        OK.preCanvas = current;
        current.SetActive(false);
        messageCanvas.SetActive(true);
    }
}
