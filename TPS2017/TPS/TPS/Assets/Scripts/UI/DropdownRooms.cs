using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DropdownRooms : MonoBehaviour {

    Dropdown dropdownItem;


    private float timer;
    private string rooms = null;
    void Awake()
    {
        timer = 0.0f;
        dropdownItem = GetComponent<Dropdown>();
        dropdownItem.options.Clear();
        dropdownItem.captionText.text = "";
    }
	
	// Update is called once per frame
	void Update () {
        timer += Time.deltaTime;
        if (timer > 0.5f)
        {
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_ROOMS, null);
            }
            timer = 0.0f;
        }
        if (rooms != CommonInformation.serverRooms)
        {
            rooms = CommonInformation.serverRooms;
            if (rooms != null)
            {
                updateRooms(rooms);
            }
        }
        //updateRooms("abc#def#");
    }

    private void updateRooms(string rooms)
    {
        string[] roomNames = rooms.Split('#');
        List<string> tempNames = new List<string>();
        foreach (string room in roomNames)
        {
            if (room != null && room != "")
            {
                tempNames.Add(room);
            }
        }
        dropdownItem.options.Clear();
        Dropdown.OptionData tempData;
        for (int i = 0; i < tempNames.Count; i++)
        {
            tempData = new Dropdown.OptionData();
            tempData.text = tempNames[i];
            dropdownItem.options.Add(tempData);
        }
        if (tempNames.Count>0)
        {
            dropdownItem.captionText.text = tempNames[0];
        }

    }
}
