using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using System;
using UnityEngine.Networking;
using UnityEngine.Video;

public class QuizController : MonoBehaviour
{
    public GameObject lesson;
    public GameObject endMenu;
    public GameObject retryButton;
    public GameObject settingsMenu;
    private TMP_Text quizTitle;
    private TMP_Text quizQuestion;
    private Button[] options;
    private TMP_Text[] answers;
    private float startTime;
    private LessonDetails lessonDetails;
    private ChallengeDetails challengeDetails;
    private int questionNum;
    private int score;
    public AudioSource mainTrack;
    public AudioSource clickSound;
    public AudioSource closeSound;
    public AudioSource quizDone;

    void Start()
    {
        //Initialize Quiz Screen
        lesson.SetActive(true);
        endMenu.SetActive(false);
        score =0;
        questionNum = 0;
        quizTitle = GameObject.Find("QuizTitle").GetComponent<TMP_Text>();
        quizQuestion = GameObject.Find("QuizQuestion").GetComponent<TMP_Text>();
        options = new Button[4];
        answers = new TMP_Text[4];
        for (int i=0;i<4;i++)
        {
            string s = string.Format("Option{0}",i);
            Button _option = GameObject.Find(s.ToString()).GetComponent<Button>();
            options[i] = _option;
            answers[i] = options[i].GetComponentInChildren<TMP_Text>();
            
        }
        if (PlayerPrefs.GetInt("challenge")==1)
        {
            StartCoroutine(GetChallenge());
        }
        else if (PlayerPrefs.GetInt("challenge")==2)
        {
            StartCoroutine(GetChallenged());
        }
        else
        {
            StartCoroutine(GetLesson());
        }
    }
    void Update()
    {
        //Set volume of sound effects
        mainTrack.volume = PlayerPrefs.GetFloat("volume");
        clickSound.volume = PlayerPrefs.GetFloat("volume");
        closeSound.volume = PlayerPrefs.GetFloat("volume"); 
        quizDone.volume = PlayerPrefs.GetFloat("volume");
    }
    #region Lesson
    private IEnumerator GetLesson()
    {
        //Get the lesson of the selected topic
        string url = string.Format("http://127.0.0.1:5000/lessons/?topic_id={0}&lesson_id={1}",PlayerPrefs.GetString("topicID"),PlayerPrefs.GetString("lessonID"));
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            lessonDetails = JsonUtility.FromJson<LessonDetails>(webRequest.downloadHandler.text);
            UpdateLesson();
        }
    }
    private void UpdateLesson()
    {
        //Update the scene to display the lesson got from database
        TMP_Text lessonTitle = GameObject.Find("LessonTitle").GetComponent<TMP_Text>();
        TMP_Text lessonContent = GameObject.Find("LessonContent").GetComponent<TMP_Text>();
        VideoPlayer videoPlayer = GameObject.Find("Video Player").GetComponent<VideoPlayer>();
        //videoPlayer.url = lessonDetails.url_link;
        lessonTitle.text = lessonDetails.name;
        lessonContent.text = lessonDetails.content;
        quizTitle.text = lessonDetails.name;
        quizQuestion.text = lessonDetails.questions[questionNum].description;
        for (int i=0;i<4;i++)
        {
            options[i].GetComponent<Option>().answer = lessonDetails.questions[questionNum].choices[i].is_correct;
            answers[i].text = lessonDetails.questions[questionNum].choices[i].description;
        }
    }   
    #endregion

    #region Quiz questions
    public void SelectOption()
    {
        //triggered when choosing an option during quiz
        clickSound.Play();
        int elapsedTime = (int) ((Time.time - startTime)*1000);
        startTime = Time.time;
        bool optionSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Option>().answer;
        if (!(PlayerPrefs.GetInt("challenge")>0))
            StartCoroutine(PostOption("http://127.0.0.1:5000/question_attempts/?student_id="+PlayerPrefs.GetString("userID")+"&question_id="+lessonDetails.questions[questionNum].id+"&is_correct="+optionSelected.ToString()+"&duration_ms="+elapsedTime.ToString()));
        else
            StartCoroutine(PostOption("http://127.0.0.1:5000/question_attempts/?student_id="+PlayerPrefs.GetString("userID")+"&question_id="+challengeDetails.quiz.questions[questionNum].id+"&is_correct="+optionSelected.ToString()+"&duration_ms="+elapsedTime.ToString()));
        if (optionSelected)
        {
            score++;
        }
        updateQuestion();
    }
    private IEnumerator PostOption(string url)
    {
        //submit the selected answer to database
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
        }
    }
    private void updateQuestion()
    {
        //Update the question when completing each question
        questionNum++;
        if (!(PlayerPrefs.GetInt("challenge")>0))
        {
            if (questionNum == lessonDetails.count_questions)
            {
                StartCoroutine(DoneQuiz());
                endMenu.SetActive(true);
                quizDone.Play();
                TMP_Text endMenuText = GameObject.Find("Score").GetComponent<TMP_Text>();
                endMenuText.text ="Your Score: "+ score.ToString() + "/"+questionNum.ToString();
            }
            else
            {
                quizQuestion.text = lessonDetails.questions[questionNum].description;
                for (int i=0;i<4;i++)
                {
                    answers[i].text = lessonDetails.questions[questionNum].choices[i].description;
                    options[i].GetComponent<Option>().answer = lessonDetails.questions[questionNum].choices[i].is_correct;
                }
                startTime = Time.time;
            }
        }
        else
        {
            if (questionNum == challengeDetails.quiz.questions.Length)
            {
                StartCoroutine(DoneQuiz());
                endMenu.SetActive(true);
                retryButton.SetActive(false);
                TMP_Text endMenuText = GameObject.Find("Score").GetComponent<TMP_Text>();
                endMenuText.text ="Your Score: "+ score.ToString() + "/"+questionNum.ToString();
            }
            else
            {
                quizQuestion.text = challengeDetails.quiz.questions[questionNum].description;
                for (int i=0;i<4;i++)
                {
                    answers[i].text = challengeDetails.quiz.questions[questionNum].choices[i].description;
                    options[i].GetComponent<Option>().answer = challengeDetails.quiz.questions[questionNum].choices[i].is_correct;
                }
                startTime = Time.time;
            }
        }
    }
    private IEnumerator DoneQuiz()
    {
        //Triggered when quiz is done to post quiz final result to database
        string quizID;
        if (!(PlayerPrefs.GetInt("challenge")>0))
        {
            int topic = Int32.Parse(PlayerPrefs.GetString("topicID"));
            int lesson = Int32.Parse(PlayerPrefs.GetString("lessonID"));
            quizID = (lesson+3*(topic-1)).ToString();
        }
        else
        {
            quizID = challengeDetails.quiz.id.ToString();
        }
        string url = string.Format("http://127.0.0.1:5000/quiz_attempts/?student_id={0}&quiz_id={1}&score={2}",PlayerPrefs.GetString("userID"),quizID,score);
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
            if (PlayerPrefs.GetInt("challenge")==2)
            {
                StartCoroutine(FinishChallenge());
            }
        }
    }
    private IEnumerator FinishChallenge()
    {
        //Triggered when challenge quiz is done to post final result to database
        string url = string.Format("http://127.0.0.1:5000/challenges/?from_student_id={0}&to_student_id={1}&quiz_id={2}&is_completed=true",PlayerPrefs.GetInt("challengerID"),PlayerPrefs.GetString("userID"),PlayerPrefs.GetInt("challengeQuizID"));
        using (UnityWebRequest webRequest = UnityWebRequest.Put(url,"null"))
        {
            yield return webRequest.SendWebRequest();
        }
    }
    #endregion

    #region Settings and buttons
    public void ShareTwitter()
    {
        //Share the question on twitter
        string question = quizQuestion.text;
        string pretext = "I have a problem with this question: ";
        string urlText = System.Uri.EscapeUriString(pretext + question);
        Application.OpenURL("https://twitter.com/intent/tweet?text="+urlText);
    }
    public void LoginTwitter()
    {
        //Log in to twitter
        Application.OpenURL("https://twitter.com/login");
    }   
    public void RetryButton()
    {
        //Retry quiz
        clickSound.Play();
        Start();
    }
    public void BackButton()
    {
        //Finish quiz return to main
        SceneManager.LoadScene("MainGame");
        PlayerPrefs.SetInt("challenge",0);
    }
    public void DoneLesson()
    {
        //Triggered when finished lesson to start quiz
        clickSound.Play();
        lesson.SetActive(false);
        startTime = Time.time;
    }
    public void LogOut()
    {
        //Quit application
        Application.Quit();
    }
    public void Settings()
    {
        //Open settings menu
        clickSound.Play();
        settingsMenu.SetActive(true);
        float volume = PlayerPrefs.GetFloat("volume");
        Slider slider = GameObject.Find("VolumeSlider").GetComponent<Slider>();
        slider.value = volume;
    }
    public void SettingsOut()
    {
        //Close settings menu
        closeSound.Play();
        settingsMenu.SetActive(false);
    }
    public void SetVolume(float vol)
    {
        //Save volume slider value as volume
        PlayerPrefs.SetFloat("volume",vol);
    }
    #endregion

    #region ChallengeLogic
    IEnumerator GetChallenge()
    {
        //Get challenge quiz if issuing challenge to another classmate
        string url = string.Format("http://127.0.0.1:5000/challenges/?from_student_id={0}&to_student_id={1}",PlayerPrefs.GetString("userID"),PlayerPrefs.GetString("challengeID"));
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
            challengeDetails = JsonUtility.FromJson<ChallengeDetails>(webRequest.downloadHandler.text);
            UpdateChallenge();
        }
    }
    IEnumerator GetChallenged()
    {
        //Get challenge quiz if challenge has been issued by another classmate
        string url = string.Format("http://127.0.0.1:5000/quizzes/questions?quiz_id={0}", PlayerPrefs.GetInt("challengeQuizID"));
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            QuizDetails1 challengeQuiz = JsonUtility.FromJson<QuizDetails1>(webRequest.downloadHandler.text);
            List<QuestionDetails> listOfQuestions = new List<QuestionDetails>();
            foreach (QuestionsDetails questions in challengeQuiz.questions)
            {
                listOfQuestions.Add(questions.question);
            }
            challengeDetails = new ChallengeDetails
            {
                quiz = new QuizDetails
                {
                    id = challengeQuiz.id,
                    questions = listOfQuestions.ToArray()
                }
            };
            challengeDetails.quiz.id = challengeQuiz.id;
            UpdateChallenge();
        }
    }
    private void UpdateChallenge()
    {
        //Update lesson page for challenge quiz
        TMP_Text lessonTitle = GameObject.Find("LessonTitle").GetComponent<TMP_Text>();
        TMP_Text lessonContent = GameObject.Find("LessonContent").GetComponent<TMP_Text>();
        lessonTitle.text = "This is a challenge quiz!";
        lessonContent.text = "This quiz will contain questions that you both have attempted, the winner will be determined by the highest score within the fastest time. Good luck!";
        quizTitle.text = "Challenge Quiz!";
        quizQuestion.text = challengeDetails.quiz.questions[questionNum].description;
        for (int i=0;i<4;i++)
        {

            options[i].GetComponent<Option>().answer = challengeDetails.quiz.questions[questionNum].choices[i].is_correct;
            answers[i].text = challengeDetails.quiz.questions[questionNum].choices[i].description;
        }
    }
    #endregion
}
#region JSON Classes
[Serializable]
public class QuestionDetails
{
    public AttemptsDetails[] attempts;
    public Choice[] choices;
    public int count_attempts;
    public int count_choices;
    public string created_at;
    public string description;
    public int id;
    public int lesson_id;
    public int topic_id;
}
[Serializable]
public class Choice
{
    public string created_at;
    public string description;
    public int id;
    public bool is_correct;
}
[Serializable]
public class LessonDetails
{
    public string content;
    public int count_questions;
    public string created_at;
    public string id;
    public string name;
    public QuestionDetails[] questions;
    public string topic_id;
    public string url_link;
}
[Serializable]
public class AttemptsDetails
{
    public string created_at;
    public int duration_ms;
    public string id;
    public bool is_correct;
    public string question_id;
    public string student_id;
}
[Serializable]
public class ChallengeDetails
{
    public string created_at;
    public int from_student_id;
    public bool is_completed;
    public QuizDetails quiz;
    public int to_student_id;
    public int winner_id;
}
[Serializable]
public class QuizDetails
{
    public int id;
    public QuestionDetails[] questions;
}
[Serializable]
public class QuizDetails1
{
    public int count_attempts;
    public int count_questions;
    public string date_end;
    public string date_start;
    public int id;
    public bool is_fast;
    public string name;
    public QuestionsDetails[] questions;
}
[Serializable]
public class QuestionsDetails
{
    public string created_at;
    public QuestionDetails question;
}
#endregion