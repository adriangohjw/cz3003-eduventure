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
    public GameObject leaderboardButton;
    private TMP_Text pointsText;
    private Button[] crops;
    private TMP_Text[] cropsText;
    private int topicSelected;
    private int lessonSelected;
    public GameObject lessonMenu;
    private ProgressDetails studentProgress;
    private float time = 0.0f;
    public float interpolationPeriod = 10.0f;
    public AudioSource main_track;
    public AudioSource notification;
    public AudioSource clickSound;
    public AudioSource fieldSound;
    public AudioSource closeSound;
    public AudioSource acceptChallenge;

    void Start()
    {
        //Initialize all variables and perform starting checks for points and progress
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
        //set volume on all sounds and perform Challenge checks every 10seconds
        acceptChallenge.volume = PlayerPrefs.GetFloat("volume");
        main_track.volume = PlayerPrefs.GetFloat("volume");
        notification.volume = PlayerPrefs.GetFloat("volume");
        clickSound.volume = PlayerPrefs.GetFloat("volume");
        fieldSound.volume = PlayerPrefs.GetFloat("volume");
        closeSound.volume = PlayerPrefs.GetFloat("volume");
        time += Time.deltaTime;

        if (time >= interpolationPeriod)
        {
            time = time - interpolationPeriod;
            StartCoroutine(CheckChallenge());
        }
    }
    #region Crops and Topics
    public void CropClick()
    {
        //Open crop menu and show progress of the lessons
        fieldSound.Play();
        cropMenu.SetActive(true);
        lessonMenu.SetActive(false);    
        string topic = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        topicSelected = EventSystem.current.currentSelectedGameObject.GetComponent<Crop>().topicID;
        Button[] lessons = new Button[3];
        TMP_Text[] lessonText = new TMP_Text[3];
        TMP_Text plantTitle = GameObject.Find("PlantTitle").GetComponent<TMP_Text>();
        TMP_Text topicProgress = GameObject.Find("TopicProgress").GetComponent<TMP_Text>();
        topicProgress.text = "Completed: "+studentProgress.topics[topicSelected].completed_lessons.ToString()+"/"+studentProgress.topics[topicSelected].total_lessons.ToString()+" Lessons";
        plantTitle.text = topic;
        for (int i=0;i<3;i++)
        {
            string s = string.Format("Lesson{0}",i);
            Button _lesson = GameObject.Find(s).GetComponent<Button>();
            lessons[i] = _lesson;
            lessonText[i] = lessons[i].GetComponentInChildren<TMP_Text>();
            lessons[i].GetComponent<Lesson>().lessonID = i;
            lessonText[i].text = "Lesson "+ (i+1).ToString();
        }
    }
    public void LessonClick()
    {
        //Open lesson and display past attempts
        clickSound.Play();
        lessonMenu.SetActive(true);
        lessonSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Lesson>().lessonID;
        TMP_Text pastAttempts = GameObject.Find("PastAttempts").GetComponent<TMP_Text>();
        if (lessonSelected>studentProgress.topics[topicSelected].completed_lessons)
        {
            pastAttempts.text ="You have not completed the previous lesson to be able to access this lesson!";
        }
        else
        {
            int topic = topicSelected+1;
            int lesson = lessonSelected+1;
            int quizID = (lesson+3*(topic-1));
            StartCoroutine(GetPastAttempts(quizID));
        }
    }
    private IEnumerator GetPastAttempts(int quizID)
    {
        //Call API to get past attempts on particular quiz
        string url = string.Format("http://127.0.0.1:5000/quiz_attempts/list?student_id={0}&quiz_id={1}",PlayerPrefs.GetString("userID"),quizID);
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            AttemptDetail attemptDets = JsonUtility.FromJson<AttemptDetail>(webRequest.downloadHandler.text);
            TMP_Text pastAttempts = GameObject.Find("PastAttempts").GetComponent<TMP_Text>();
            if (attemptDets.error == null)
            {
                string attemptsText = "\nLast 3 Attempts:";
                for (int i =1;i<attemptDets.list.Length+1;i++)
                { 
                    attemptsText += "\n";
                    attemptsText += "  Done on: " + attemptDets.list[attemptDets.list.Length-i].created_at +"\n";
                    attemptsText += "  Score: " + attemptDets.list[attemptDets.list.Length-i].score.ToString() + "/3\n";
                    if (i>2)
                    {
                        break;
                    }
                }
                pastAttempts.text = attemptsText;
            }
            else
            {
                pastAttempts.text = "No previous attempts yet.";
            }
        }
    }
    public void QuizStart()
    {
        //Start quiz button
        clickSound.Play();
        int topicID = topicSelected + 1;
        int lessonID = lessonSelected +1;
        PlayerPrefs.SetString("topicID",topicID.ToString());
        PlayerPrefs.SetString("lessonID",lessonID.ToString());
        SceneManager.LoadScene("QuizScene");
    }
    public void CropMenuClose()
    {
        //Close the crops menu
        closeSound.Play();
        cropMenu.SetActive(false);
    }
    #endregion

    #region Settings
    public void Settings()
    {
        //Open the settings menu
        clickSound.Play();
        settingsMenu.SetActive(true);
        float volume = PlayerPrefs.GetFloat("volume");
        Slider slider = GameObject.Find("VolumeSlider").GetComponent<Slider>();
        slider.value = volume;
    }
    public void LogOut()
    {
        //Close the game
        Application.Quit();
    }
    public void SettingsOut()
    {
        //Close the settings menu
        closeSound.Play();
        settingsMenu.SetActive(false);
    }
    public void SetVolume(float vol)
    {
        //Take slider value and save it
        PlayerPrefs.SetFloat("volume",vol);
    }
    public void LoginTwitter()
    {
        //Open twitter login url
        Application.OpenURL("https://twitter.com/login");
    }
    #endregion
    
    #region Leadboard and Profile
    public void PointsClick()
    {
        //Get student profile and open Profile menu
        clickSound.Play();
        pointsMenu.SetActive(true);
        leaderboardButton.SetActive(true);
        TMP_Text pointsContent = GameObject.Find("PointsContent").GetComponent<TMP_Text>();
        TMP_Text pointsNumbers = GameObject.Find("PointsNumbers").GetComponent<TMP_Text>();
        TMP_Text pointsTitle = GameObject.Find("PointsTitle").GetComponent<TMP_Text>();
        RectTransform pointsText = GameObject.Find("PointsContent").GetComponent<RectTransform>();
        RectTransform pointsText2 = GameObject.Find("PointsNumbers").GetComponent<RectTransform>();
        pointsText.sizeDelta = new Vector2(666,707);
        pointsText2.sizeDelta = new Vector2(73,707);
        string displayText = "Progress:\n";
        string numberText = "\n";
        foreach (ProgressTopicDetails topic in studentProgress.topics)
        {
            displayText += "  "+topic.name +"\n";
            displayText += "    Completed Lessons:\n";
            numberText += "\n";
            numberText += topic.completed_lessons.ToString() + "/" + topic.total_lessons.ToString() +"\n";
            int i =1;
            foreach (ProgressLessonDetails lesson in topic.lessons)
            {
                displayText += "      Quiz "+i.ToString()+":\n";
                numberText += lesson.quizzes[0].max_score.ToString()+"/"+lesson.quizzes[0].total_questions.ToString()+"\n";
                i++;
            }
        }
        pointsTitle.text = "Student Profile";
        pointsContent.text = displayText;
        pointsNumbers.text = numberText;
    }
    public void PointsClickOut()
    {
        //Close profile/Leaderboard menu
        closeSound.Play();
        pointsMenu.SetActive(false);
    }
    public void LeaderboardClick()
    {
        //Open Leaderboard
        clickSound.Play();
        leaderboardButton.SetActive(false);
        StartCoroutine(UpdatePointsMenu());
    }
    private IEnumerator UpdatePointsMenu()
    {
        //Get leaderboard from API and display
        string url = "http://127.0.0.1:5000/statistics/leaderboard";
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            RectTransform pointsText = GameObject.Find("PointsContent").GetComponent<RectTransform>();
            RectTransform pointsText2 = GameObject.Find("PointsNumbers").GetComponent<RectTransform>();
            pointsText.sizeDelta = new Vector2(666,800);
            pointsText2.sizeDelta = new Vector2(73,800);
            TMP_Text pointsContent = GameObject.Find("PointsContent").GetComponent<TMP_Text>();
            TMP_Text pointsNumbers = GameObject.Find("PointsNumbers").GetComponent<TMP_Text>();
            TMP_Text pointsTitle = GameObject.Find("PointsTitle").GetComponent<TMP_Text>();
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
            pointsTitle.text = "Leaderboard";
            pointsContent.text = displayText;
            pointsNumbers.text = numberText;
        }
    }
    #endregion

    #region Challenge System
    public void StartChallenge()
    {
        //Open challenge scene
        SceneManager.LoadScene("ChallengeScene");
    }
    public void AcceptChallenge()
    {
        //Accept an incoming challenge
        int quizID = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Challenger>().quizID;
        int challengerID = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Challenger>().challengerID;
        acceptChallenge.Play();
        PlayerPrefs.SetInt("challenge",2);
        PlayerPrefs.SetInt("challengeQuizID",quizID);
        PlayerPrefs.SetInt("challengerID",challengerID);
        SceneManager.LoadScene("QuizScene");
    }
    #endregion

    #region Background/Initial Processes
    private IEnumerator GetPoints()
    {
        //Get user points to display on the top bar
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

    private IEnumerator GetCropProgress()
    {
        //Get users progress to display appropriate stage of crop
        string url = "http://127.0.0.1:5000/progresses/?student_id=" + PlayerPrefs.GetString("userID");
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            studentProgress = JsonUtility.FromJson<ProgressDetails>(webRequest.downloadHandler.text);
            for (int i=0;i<6;i++)
            {
                crops[i].GetComponent<Crop>().topicID = studentProgress.topics[i].id-1;
                cropsText[i].text = studentProgress.topics[i].name;
                if (studentProgress.topics[i].completed_lessons==0)
                    crops[i].GetComponent<Image>().sprite = crops[i].GetComponent<Crop>().zeroImage;
                else if (studentProgress.topics[i].completed_lessons==1)
                    crops[i].GetComponent<Image>().sprite = crops[i].GetComponent<Crop>().firstImage;
                else if (studentProgress.topics[i].completed_lessons==2)
                    crops[i].GetComponent<Image>().sprite = crops[i].GetComponent<Crop>().secondImage;
                else if (studentProgress.topics[i].completed_lessons==3)
                    crops[i].GetComponent<Image>().sprite = crops[i].GetComponent<Crop>().thirdImage;
            }
        }
    }
    private IEnumerator CheckChallenge()
    {
        //Check if any incoming challenge is received
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
        //Process any challenges that are received
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
                challengers[i].GetComponent<Challenger>().challengerID = challenge.from_student_id;
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
        if (i>0)
        {
            notification.Play();
        }
    }
    #endregion
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
    public int id;
    public int total_lessons;
    public int completed_lessons;
    public ProgressLessonDetails[] lessons;
    public bool completion_status;
    public string name;
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
    public int max_score;
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
[Serializable]
public class ChallengerList
{
    public ChallengerDetails[] users;
}
[Serializable]
public class AttemptDetail
{
    public AttemptDetails[] list;
    public string error;
}
[Serializable]
public class AttemptDetails
{
    public string created_at;
    public int id;
    public int quiz_id;
    public int score;
    public int student_id;
}
#endregion