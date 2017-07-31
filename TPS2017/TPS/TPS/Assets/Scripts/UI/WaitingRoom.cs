using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class WaitingRoom : MonoBehaviour {

    public Text player1;
    public Text player2;
    public Text player3;
    public GameObject beginGame;

    private float timer;
    private string players = null;
    void Start()
    {
        timer = 0.0f;
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;
        if (timer > 0.5f)
        {
            if (NetworkHandler.getNetHandlerInstance() != null)
            {
                NetworkHandler.getNetHandlerInstance().sendMSG(CommonInformation.MSG_CS_PLAYERS, null);
            }
            timer = 0.0f;
        }
        if (players != CommonInformation.serverPlayers)
        {
            players = CommonInformation.serverPlayers;
            if (players != null)
            {
                UpdatePlayers();
            }
        }
        if (CommonInformation.isGameBegin)
        {
            CommonInformation.isGameBegin = false;
            SceneManager.LoadScene("MainScene");
        }
    }

    private void UpdatePlayers()
    {
        string[] playerNames = players.Split('#');
        int index = 0;
        foreach (string player in playerNames)
        {
            if (player != null && player != "")
            {
                if (index == 0)
                {
                    player1.text = player;
                }
                else if (index == 1)
                {
                    player2.text = player;
                }
                else
                {
                    player3.text = player;
                }
            }
            ++index;
        }
        if (player1.text == CommonInformation.username)
        {
            beginGame.SetActive(true);
        }
        else
        {
            CommonInformation.isHost = false;
            beginGame.SetActive(false);
        }
    }
}
