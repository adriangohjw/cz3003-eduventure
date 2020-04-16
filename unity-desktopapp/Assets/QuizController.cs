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
    private TMP_Text quizTitle;
    private TMP_Text quizQuestion;
    private Button[] options;
    private TMP_Text[] answers;
    private float startTime;
    private LessonDetails lessonDetails;
    private int questionNum;
    private int score=0;

    void Start()
    {
        
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
        StartCoroutine(GetLesson());
    }
    private IEnumerator GetLesson()
    {
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
        TMP_Text lessonTitle = GameObject.Find("LessonTitle").GetComponent<TMP_Text>();
        TMP_Text lessonContent = GameObject.Find("LessonContent").GetComponent<TMP_Text>();
        VideoPlayer videoPlayer = GameObject.Find("Video Player").GetComponent<VideoPlayer>();
        //Unable to play Youtube Videos TODO
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
    private void updateQuestion()
    {   
        questionNum++;
        if (questionNum == lessonDetails.count_questions)
        {
            StartCoroutine(DoneQuiz());
            SceneManager.LoadScene("MainGame");
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
    public void DoneLesson()
    {
        lesson.SetActive(false);
        startTime = Time.time;
    }
    public void SelectOption()
    {
        int elapsedTime = (int) ((Time.time - startTime)*1000);
        startTime = Time.time;
        bool optionSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Option>().answer;
        StartCoroutine(PostOption("http://127.0.0.1:5000/question_attempts/?student_id="+PlayerPrefs.GetString("userID")+"&question_id="+lessonDetails.questions[questionNum].id+"&is_correct="+optionSelected.ToString()+"&duration_ms="+elapsedTime.ToString()));
        if (optionSelected)
        {
            score++;
        }
        updateQuestion();
    }
    private IEnumerator PostOption(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
        }
    }
    private IEnumerator DoneQuiz()
    {
        int topic = Int32.Parse(PlayerPrefs.GetString("topicID"));
        int lesson = Int32.Parse(PlayerPrefs.GetString("lessonID"));
        string quizID = (lesson+3*(topic-1)).ToString();
        string url = string.Format("http://127.0.0.1:5000/quiz_attempts/?student_id={0}&quiz_id={1}&score={2}",PlayerPrefs.GetString("userID"),quizID,score);
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
        }
    }

}
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