using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using System;
using UnityEngine.Networking;

public class ChallengeController : MonoBehaviour
{
    private TMP_Text pointsText;
    private Button[] classmate;
    private TMP_Text[] classmateText;

    void Start()
    {
        pointsText = GameObject.Find("PointsText").GetComponent<TMP_Text>();
        classmate = new Button[6];
        classmateText = new TMP_Text[6];
        for (int i=0;i<6;i++)
        {
            string s = string.Format("Classmate{0}",i);
            Button _classmate = GameObject.Find(s.ToString()).GetComponent<Button>();
            classmate[i] = _classmate;
            classmateText[i] = classmate[i].GetComponentInChildren<TMP_Text>();
            classmateText[i].text = s;
        }
        StartCoroutine(GetPoints("TODO"));

    }
    public void StartChallenge()
    {
        string classmateSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        //TODO
        //INITIALIZE QUIZ (Use QuizController and Scene?)
    }
    private IEnumerator GetPoints(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            PointsDetails pointsDets = JsonUtility.FromJson<PointsDetails>(webRequest.downloadHandler.text);
            pointsText.text = pointsDets.points;
        }

    }
}