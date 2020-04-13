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
    public GameObject eventMenu;
    private TMP_Text pointsText;
    private Button[] crops;
    private TMP_Text[] cropsText;
    private string selected;
    public GameObject lessonMenu;

    // Start is called before the first frame update
    void Start()
    {
        cropMenu.SetActive(false);
        pointsMenu.SetActive(false);
        eventMenu.SetActive(false);
        lessonMenu.SetActive(false);
        int i;
        crops = new Button[6];
        cropsText = new TMP_Text[6];
        pointsText = GameObject.Find("PointsText").GetComponent<TMP_Text>();
        //either hardcode crops and location or replace with a dynamic way
        for (i=0;i<6;i++)
        {
            string s = string.Format("Crop{0}",i+1);
            Button _crops = GameObject.Find(s.ToString()).GetComponent<Button>();
            crops[i] = _crops;
            cropsText[i] = crops[i].GetComponentInChildren<TMP_Text>();
        }
        //StartCoroutine(GetCropProgress());
        //Instantiated Crops and Points Texts.
        //Update Crops Name/Level and Points Amount
        //StartCoroutine(GetPoints("TODO"));
    }

    public void CropClick()
    {
        //query database for statistic with Crop name
        selected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        cropMenu.SetActive(true);
        //StartCoroutine(UpdateCropsMenu(LessonID));
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
        //StartCoroutine(UpdatePointsMenu("TODO"));
    }
    public void PointsClickOut()
    {
        pointsMenu.SetActive(false);
    }
    public void QuizStart()
    {
        //from selected, get lessonID and start quiz scene
        //SceneManager.LoadScene("QuizScene");
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
    private IEnumerator UpdateCropsMenu(string topicID)
    {
        //TODO
        string url = "http://127.0.0.1:5000/lessons/?topic_id="+topicID; 
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            TMP_Text plantTitle = GameObject.Find("PlantTitle").GetComponent<TMP_Text>();
            //TMP_Text plantStats = GameObject.Find("PlantContent").GetComponent<TMP_Text>();

            CropMenuDetails cropmenu = JsonUtility.FromJson<CropMenuDetails>(webRequest.downloadHandler.text);
            
            plantTitle.text = cropmenu.title;
            //plantStats.text = cropmenu.stats;
        }
    }
    private IEnumerator GetCropProgress(int id)
    {
        string url = "http://127.0.0.1:5000/progresses/?student_id=" + UserController.userID.ToString();
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            ProgressDetails progressDets = JsonUtility.FromJson<ProgressDetails>(webRequest.downloadHandler.text);
            for (int i=0;i<6;i++)
            {
                float progress = (float.Parse(progressDets.topics[i].completed_lessons)/float.Parse(progressDets.topics[i].total_lessons));
                cropsText[i].text = progressDets.topics[i].id +" "+progress.ToString();
            }
        }
    }
    public void LessonClick(){
        string cropSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        //StartCoroutine(UpdateLessonMenu(cropSelected));
    }
    private IEnumerator UpdateLessonMenu(string cropSelected)
    {
        string url = string.Format("http://127.0.0.1:5000/lesson/?topic_id={0}+&lesson_id={1}",selected,cropSelected)
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            ProgressLessonDetails lessonDets = JsonUtility.FromJson<ProgressLessonDetails>(webRequest.downloadHandler.text);
            lessonMenu.SetActive(True);
            TMP_Text plantStats = GameObject.Find("PlantStats").GetComponent<TMP_Text>();
            plantStats.text = string.Format("Number of quizzes available: {0}\nNumber of quizzes completed: {1}",lessonDets.total_quizes,lessonDets.completed_quizzes);
            //TODO update selected
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
[Serializable]
public class ProgressDetails
{
    public string error;
    public ProgressTopicDetails[] topics;
}
[Serializable]
public class ProgressTopicDetails
{
    public string id;
    public string total_lessons;
    public string completed_lessons;
    public ProgressLessonDetails[] lessons;
    public bool completion_status;
}
[Serializable]
public class ProgressLessonDetails
{
    public string id;
    public string total_quizes;
    public string completed_quizzes;
    public ProgressQuizDetails[] quizzes;
    public bool completion_status;
}
[Serializable]
public class ProgressQuizDetails
{
    public string max_score;
    public bool completion_status;
    public string total_questions;

}