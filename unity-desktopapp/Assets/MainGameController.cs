using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using System;
using UnityEngine.Networking;


public class MainGameController : MonoBehaviour
{
    public GameObject cropMenu;
    public GameObject pointsMenu;
    private TMP_Text pointsText;
    private Button[] crops;
    private TMP_Text[] cropsText;

    // Start is called before the first frame update
    void Start()
    {
        cropMenu.SetActive(false);
        pointsMenu.SetActive(false);
        int i;
        crops = new Button[6];
        cropsText = new TMP_Text[6];
        pointsText = GameObject.Find("PointsText").GetComponent<TMP_Text>();
        //either hardcode crops and location or replace with a dynamic way
        string[] cropNames = new string[6];
        cropNames = CropManager.GetCropsNames(1);
        for (i=0;i<6;i++)
        {
            string s = string.Format("Crop{0}",i+1);
            Button _crops = GameObject.Find(s.ToString()).GetComponent<Button>();
            crops[i] = _crops;
            cropsText[i] = crops[i].GetComponentInChildren<TMP_Text>();
            cropsText[i].text = cropNames[i];
        }
        //Instantiated Crops and Points Texts.
        //Update Crops Name/Level and Points Amount
        StartCoroutine(GetPoints("TODO"));
    }

    public void CropClick()
    {
        //query database for statistic with Crop name
        string cropSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        cropMenu.SetActive(true);
        StartCoroutine(UpdateCropsMenu("TODO"));
    }
    public void CropMenuClose()
    {
        cropMenu.SetActive(false);
    }
    public void LogOut()
    {
        //TO DO
        //save the game to database or something
        Application.Quit();
    }
    public void PointsClick()
    {
        pointsMenu.SetActive(true);
        TMP_Text pointsTitle = GameObject.Find("PointsTitle").GetComponent<TMP_Text>();
        StartCoroutine(UpdatePointsMenu("TODO"));
    }
    public void PointsClickOut()
    {
        pointsMenu.SetActive(false);
    }
    public void QuizStart()
    {
        Debug.Log("TODO Go To Quiz Scene");
    }
    private IEnumerator GetPoints(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            PointsDetails pointsDets = JsonUtility.FromJson<PointsDetails>(webRequest.downloadHandler.text);
            pointsText.text = pointsDets.idontknow;
        }
    }
    private IEnumerator UpdatePointsMenu(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            TMP_Text pointsContent = GameObject.Find("PointsContent").GetComponent<TMP_Text>();
            LeaderboardDetails leaderboard = JsonUtility.FromJson<LeaderboardDetails>(webRequest.downloadHandler.text);
            pointsContent.text = leaderboard.idontknow;
        }
    }
    private IEnumerator UpdateCropsMenu(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            TMP_Text plantTitle = GameObject.Find("PlantTitle").GetComponent<TMP_Text>();
            TMP_Text plantStats = GameObject.Find("PlantContent").GetComponent<TMP_Text>();

            CropMenuDetails cropmenu = JsonUtility.FromJson<CropMenuDetails>(webRequest.downloadHandler.text);
            
            plantTitle.text = cropmenu.title;
            plantStats.text = cropmenu.stats;
        }
    }
}
[Serializable]
public class PointsDetails
{
    public string idontknow;
    public string points;
}
[Serializable]
public class LeaderboardDetails
{
    public string idontknow;
}
[Serializable]
public class CropMenuDetails
{
    public string title;
    public string stats;
}