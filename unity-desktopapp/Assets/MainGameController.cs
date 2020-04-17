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
    public GameObject settingsMenu;
    public GameObject challengerButton1;
    public GameObject challengerButton2;
    public GameObject challengerButton3;
    private TMP_Text pointsText;
    private Button[] crops;
    private TMP_Text[] cropsText;
    private string topicSelected;
    private string lessonSelected;
    public GameObject lessonMenu;
    private ProgressDetails studentProgress;
    private float time = 0.0f;
    public float interpolationPeriod = 10.0f;

    void Start()
    {
        cropMenu.SetActive(false);
        pointsMenu.SetActive(false);
        lessonMenu.SetActive(false);
        settingsMenu.SetActive(false);
        int i;
        crops = new Button[6];
        cropsText = new TMP_Text[6];
        pointsText = GameObject.Find("PointsText").GetComponent<TMP_Text>();
        for (i=0;i<6;i++)
        {
            string s = string.Format("Crop{0}",i+1);
            Button _crops = GameObject.Find(s.ToString()).GetComponent<Button>();
            crops[i] = _crops;
            cropsText[i] = crops[i].GetComponentInChildren<TMP_Text>();
            cropsText[i].text = i.ToString();
        }
        StartCoroutine(GetCropProgress());
        StartCoroutine(GetPoints());
        StartCoroutine(CheckChallenge());
        PlayerPrefs.SetInt("challenge",0);
    }
    void Update()
    {
        time += Time.deltaTime;

        if (time >= interpolationPeriod)
        {
            time = time - interpolationPeriod;
            StartCoroutine(CheckChallenge());
        }
    }

    public void CropClick()
    {
        cropMenu.SetActive(true);
        lessonMenu.SetActive(false);    
        topicSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        Button[] lessons = new Button[3];
        TMP_Text[] lessonText = new TMP_Text[3];
        for (int i=0;i<3;i++)
        {
            string s = string.Format("Lesson{0}",i);
            Button _lesson = GameObject.Find(s).GetComponent<Button>();
            lessons[i] = _lesson;
            lessonText[i] = lessons[i].GetComponentInChildren<TMP_Text>();
            lessonText[i].text = (i).ToString();
        }
    }
    public void LessonClick()
    {
        lessonMenu.SetActive(true);
        lessonSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        TMP_Text plantStats = GameObject.Find("PlantStats").GetComponent<TMP_Text>();
        TMP_Text pastAttempts = GameObject.Find("PastAttempts").GetComponent<TMP_Text>();
        string displayText = "";
        string attemptsText = "";
        if (Int32.Parse(lessonSelected)>studentProgress.topics[Int32.Parse(topicSelected)].completed_lessons)
        {
            displayText+="You have not completed the previous lesson to be able to access this lesson!";
        }
        else
        {
            displayText += "Completed Quizzes: "+studentProgress.topics[Int32.Parse(topicSelected)].lessons[Int32.Parse(lessonSelected)].completed_quizzes;
            displayText += "\nTotal Quizzes: "+studentProgress.topics[Int32.Parse(topicSelected)].lessons[Int32.Parse(lessonSelected)].total_quizes;
            if (Int32.Parse(studentProgress.topics[Int32.Parse(topicSelected)].lessons[Int32.Parse(lessonSelected)].quizzes[0].max_score)>0)
            {
                int i=1;
                foreach (ProgressQuizDetails quiz in studentProgress.topics[Int32.Parse(topicSelected)].lessons[Int32.Parse(lessonSelected)].quizzes)
                {
                    attemptsText += "Quiz "+i.ToString()+": "+quiz.max_score.ToString()+"/"+quiz.total_questions.ToString()+"\n";
                    i++;
                }
            }
        }
        plantStats.text = displayText;
        pastAttempts.text = attemptsText;
    }
    public void CropMenuClose()
    {
        cropMenu.SetActive(false);
    }
    public void LogOut()
    {
        Application.Quit();
    }
    public void Settings()
    {
        settingsMenu.SetActive(true);
        float volume = PlayerPrefs.GetFloat("volume");
        Slider slider = GameObject.Find("VolumeSlider").GetComponent<Slider>();
        slider.value = volume;
    }
    public void SettingsOut()
    {
        settingsMenu.SetActive(false);
    }
    public void PointsClick()
    {
        pointsMenu.SetActive(true);
        TMP_Text pointsTitle = GameObject.Find("PointsTitle").GetComponent<TMP_Text>();
        StartCoroutine(UpdatePointsMenu());
    }
    public void PointsClickOut()
    {
        pointsMenu.SetActive(false);
    }
    public void QuizStart()
    {
        int topicID = Int32.Parse(topicSelected) + 1;
        int lessonID = Int32.Parse(lessonSelected) +1;
        PlayerPrefs.SetString("topicID",topicID.ToString());
        PlayerPrefs.SetString("lessonID",lessonID.ToString());
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
    private IEnumerator GetCropProgress()
    {
        string url = "http://127.0.0.1:5000/progresses/?student_id=" + PlayerPrefs.GetString("userID");
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            studentProgress = JsonUtility.FromJson<ProgressDetails>(webRequest.downloadHandler.text);
            for (int i=0;i<6;i++)
            {
                crops[i].GetComponent<Crop>().topicID = i+1;
            }
        }
    }
    private IEnumerator CheckChallenge()
    {
        string url = "http://127.0.0.1:5000/challenges/?to_student_id=" + PlayerPrefs.GetString("userID");
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            ChallengerList challenges = JsonUtility.FromJson<ChallengerList>("{\"users\":" + webRequest.downloadHandler.text + "}");
            processChallenges(challenges);
        }
    }
    private void processChallenges(ChallengerList challenges)
    {
        int i = 0;
        Button[] challengers = new Button[3];
        TMP_Text[] challengersText = new TMP_Text[3];
        eventMenu.SetActive(true);
        challengerButton1.SetActive(true);
        challengerButton2.SetActive(true);
        challengerButton3.SetActive(true);
        challengers[0] = challengerButton1.GetComponent<Button>();
        challengers[1] = challengerButton2.GetComponent<Button>();
        challengers[2] = challengerButton3.GetComponent<Button>();
        for (i=0;i<3;i++)
        {
            challengersText[i] = challengers[i].GetComponentInChildren<TMP_Text>();
        }
        i = 0;
        foreach (ChallengerDetails challenge in challenges.users)
        {
            if (!challenge.is_completed)
            {
                if (i==3)
                {
                    break;
                }
                challengersText[i].text = "You received a challenge from "+ challenge.from_person_name;
                challengers[i].GetComponent<Challenger>().quizID = challenge.from_student_id;
                challengers[i].GetComponent<Challenger>().quizID = challenge.quiz_id;
                i++;
            }
        }
        if (i == 0)
        {
            eventMenu.SetActive(false);
        }
        else if (i<3)
        {
            for (int j=2;j>i-1;j--)
            {
                GameObject button = GameObject.Find(string.Format("Challenger{0}",j));
                button.SetActive(false);
            }
        }
    }
    public void SetVolume(float vol)
    {
        PlayerPrefs.SetFloat("volume",vol);
    }
    public void StartChallenge()
    {
        SceneManager.LoadScene("ChallengeScene");
    }
    public void LoginTwitter()
    {
        Application.OpenURL("https://twitter.com/login");
    }
    public void AcceptChallenge()
    {
        int quizID = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Challenger>().quizID;
        int challengerID = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Challenger>().challengerID;
        PlayerPrefs.SetInt("challenge",2);
        PlayerPrefs.SetInt("challengeQuizID",quizID);
        PlayerPrefs.SetInt("challengerID",challengerID);
        SceneManager.LoadScene("QuizScene");
    }
}
#region JSON Classes
[Serializable]
public class PointsDetails
{
    public PointStudentDetails[] students;
}
[Serializable]
public class PointStudentDetails
{
    public string id;
    public string name;
    public PointQuizDetails[] quizzes;
}
[Serializable]
public class PointQuizDetails
{
    public string id;
    public string name;
    public float score;
}
[Serializable]
public class LeaderboardDetails
{
    public LeaderboardScoresDetails[] scores;
}
[Serializable]
public class LeaderboardScoresDetails
{
    public string id;
    public string matriculation_num;
    public string name;
    public float score;
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
    public int completed_lessons;
    public ProgressLessonDetails[] lessons;
    public bool completion_status;
    public string topic_name;
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
    public string id;

}
[Serializable]
public class ChallengerDetails
{
    public string created_at;
    public int from_student_id;
    public string from_person_name;
    public bool is_completed;
    public int quiz_id;
    public int to_student_id;
    public int winner_id;
}
public class ChallengerList
{
    public ChallengerDetails[] users;
}
#endregion