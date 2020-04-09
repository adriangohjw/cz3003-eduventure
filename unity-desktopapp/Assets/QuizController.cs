using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using System;
using UnityEngine.Networking;

public class QuizController : MonoBehaviour
{
    public GameObject lesson;
    private TMP_Text quizTitle;
    private TMP_Text quizQuestion;
    private Button[] options;
    private TMP_Text[] answers;
    private float startTime;

    void Start()
    {
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
        //StartCoroutine(GetLesson("TODO"));
    }
    private IEnumerator GetQuestion(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            QuestionDetails question = JsonUtility.FromJson<QuestionDetails>(webRequest.downloadHandler.text);
            updateQuestion(question);
        }
    }
    private IEnumerator GetLesson(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            LessonDetails lesson = JsonUtility.FromJson<LessonDetails>(webRequest.downloadHandler.text);
        }
    }
    private void updateQuestion(QuestionDetails question)
    {   
        quizQuestion.text = question.description;
        for (int i=0;i<4;i++)
        {
            answers[i].text = question.choices[i].description;
            options[i].GetComponent<Option>().answer = question.choices[i].is_correct;
        }
        startTime = Time.time;
    }
    public void DoneLesson()
    {
        lesson.SetActive(false);
        Debug.Log(UserController.qnsNum);
        StartCoroutine(GetQuestion("http://127.0.0.1:5000/questions/?id="+UserController.qnsNum));
    }
    public void SelectOption()
    {
        int elapsedTime = (int) ((Time.time - startTime)*1000);
        startTime = Time.time;
        Debug.Log(elapsedTime);
        bool optionSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<Option>().answer;
        StartCoroutine(PostOption("http://127.0.0.1:5000/question_attempts/?student_id="+UserController.userID+"&question_id="+UserController.qnsNum+"&is_correct="+optionSelected.ToString()+"&duration_ms="+elapsedTime.ToString()));
    }
    private IEnumerator PostOption(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
            UserController.qnsNum++;
            StartCoroutine(GetQuestion("http://127.0.0.1:5000/questions/?id="+UserController.qnsNum));
        }
    }

}
[Serializable]
public class QuestionDetails
{
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
    public string something;
}