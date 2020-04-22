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
    public GameObject settingsMenu;
    public GameObject pointsMenu;
    private TMP_Text pointsText;
    private Button[] classmate;
    private TMP_Text[] classmateText;
    private CourseList courseList;
    private int classIndexNo=0;
    public AudioSource mainTrack;
    public AudioSource clickSound;
    public AudioSource closeSound;

    void Start()
    {
        pointsText = GameObject.Find("PointsText").GetComponent<TMP_Text>();
        classmate = new Button[4];
        classmateText = new TMP_Text[4];
        for (int i=0;i<4;i++)
        {
            string s = string.Format("Classmate{0}",i);
            Button _classmate = GameObject.Find(s.ToString()).GetComponent<Button>();
            classmate[i] = _classmate;
            classmateText[i] = classmate[i].GetComponentInChildren<TMP_Text>();
        }
        StartCoroutine(GetPoints());
        StartCoroutine(GetClassmates());

    }
    void Update()
    {
        mainTrack.volume = PlayerPrefs.GetFloat("volume");
        clickSound.volume = PlayerPrefs.GetFloat("volume");
        closeSound.volume = PlayerPrefs.GetFloat("volume");        
    }
    public void StartChallenge()
    {
        string classmateSelected = EventSystem.current.currentSelectedGameObject.GetComponent<Classmates>().classmateId.ToString();
        PlayerPrefs.SetString("challengeID",classmateSelected);
        PlayerPrefs.SetInt("challenge",1);
        SceneManager.LoadScene("QuizScene");
    }
    private IEnumerator GetPoints()
    {
        string url = "http://127.0.0.1:5000/statistics/student_score?student_id=" + PlayerPrefs.GetString("userID");
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            PointsDetails pointsDets = JsonUtility.FromJson<PointsDetails>(webRequest.downloadHandler.text);
            float total_points = 0;
            foreach (PointQuizDetails quiz in pointsDets.students[0].quizzes)
            {
                total_points += quiz.score;
            }
            pointsText.text = total_points.ToString()+ " Points";
        }
    }
    private IEnumerator GetClassmates()
    {
        string url = "http://127.0.0.1:5000/courses/students/all?course_index=" + PlayerPrefs.GetString("userCourse");
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            courseList = JsonUtility.FromJson<CourseList>(webRequest.downloadHandler.text);
            updateClassmates();
        }
    }
    public void updateClassmates()
    {
        clickSound.Play();
        for (int i =0;i<4;i++)
        {
            if (courseList.students[classIndexNo].email == PlayerPrefs.GetString("userEmail"))
            {
                classIndexNo++;
                if (classIndexNo == courseList.students.Length)
                {
                    classIndexNo=0;
                }
            }
            classmateText[i].text = courseList.students[classIndexNo].name;
            classmate[i].GetComponent<Classmates>().classmateId = courseList.students[classIndexNo].id;
            classIndexNo++;
            if (classIndexNo == courseList.students.Length)
            {
                classIndexNo= 0;
            }
        }
    }
    public void Settings()
    {
        clickSound.Play();
        settingsMenu.SetActive(true);
        float volume = PlayerPrefs.GetFloat("volume");
        Slider slider = GameObject.Find("VolumeSlider").GetComponent<Slider>();
        slider.value = volume;
    }
    public void SettingsOut()
    {
        closeSound.Play();
        settingsMenu.SetActive(false);
    }
    public void SetVolume(float vol)
    {
        PlayerPrefs.SetFloat("volume",vol);
    }
    public void LogOut()
    {
        Application.Quit();
    }
    public void ReturnMain()
    {
        SceneManager.LoadScene("MainGame");
    }
    public void PointsClick()
    {
        clickSound.Play();
        pointsMenu.SetActive(true);
        TMP_Text pointsTitle = GameObject.Find("PointsTitle").GetComponent<TMP_Text>();
        StartCoroutine(UpdatePointsMenu());
    }
    private IEnumerator UpdatePointsMenu()
    {
        string url = "http://127.0.0.1:5000/statistics/leaderboard";
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            TMP_Text pointsContent = GameObject.Find("PointsContent").GetComponent<TMP_Text>();
            TMP_Text pointsNumbers = GameObject.Find("PointsNumbers").GetComponent<TMP_Text>();
            LeaderboardDetails leaderboard = JsonUtility.FromJson<LeaderboardDetails>(webRequest.downloadHandler.text);
            string displayText ="";
            string numberText = "";
            int i=1;
            foreach (LeaderboardScoresDetails student in leaderboard.scores)
            {
                displayText += i.ToString()+"."+student.name+"\n";
                numberText += student.score.ToString()+"\n";
                i++;
                if (i>17)
                {
                    break;
                }
            }
            pointsContent.text = displayText;
            pointsNumbers.text = numberText;
        }
    }
    public void PointsClickOut()
    {
        closeSound.Play();
        pointsMenu.SetActive(false);
    }
}
[Serializable]
public class CourseList
{
    public StudentDetails[] students;   
}
[Serializable]
public class StudentDetails
{
    public string email;
    public string name;
    public int id;
}