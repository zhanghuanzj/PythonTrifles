using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapDetect : MonoBehaviour {

    public bool isCollide = false;
    public bool isLocated = false;
    public bool isHost;
	// Use this for initialization

    void Update()
    {

    }

    void OnTriggerStay(Collider other)
    {
        if (isHost && !isLocated)
        {
            if (other.tag == "Trap")
            {
                isCollide = true;
            }
            
        }
        
    }

    void OnTriggerExit(Collider other)
    {
        if (isHost && !isLocated)
        {
            if (other.tag == "Trap")
            {
                isCollide = false;
            }
        }
        
    }
}
