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
    private TMP_Text quizTitle;
    private TMP_Text quizQuestion;
    private Button[] options;
    private TMP_Text[] answers;
    private float startTime;
    private LessonDetails lessonDetails;
    private ChallengeDetails challengeDetails;
    private int questionNum;
    private int score;

    void Start()
    {
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

    #region quizQuestions
    public void SelectOption()
    {
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
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
        }
    }
    private IEnumerator DoneQuiz()
    {
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
        string url = string.Format("http://127.0.0.1:5000/challenges/?from_student_id={0}&to_student_id={1}&quiz_id={2}&is_completed=true",PlayerPrefs.GetInt("challengerID"),PlayerPrefs.GetString("userID"),PlayerPrefs.GetInt("challengeQuizID"));
        using (UnityWebRequest webRequest = UnityWebRequest.Put(url,"null"))
        {
            yield return webRequest.SendWebRequest();
        }
    }
    private void updateQuestion()
    {   
        questionNum++;
        if (!(PlayerPrefs.GetInt("challenge")>0))
        {
            if (questionNum == lessonDetails.count_questions)
            {
                StartCoroutine(DoneQuiz());
                endMenu.SetActive(true);
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
    #endregion

    #region Buttons
    public void ShareTwitter()
    {
        string question = quizQuestion.text;
        string pretext = "I have a problem with this question: ";
        string urlText = System.Uri.EscapeUriString(pretext + question);
        Application.OpenURL("https://twitter.com/intent/tweet?text="+urlText);
    }
    public void RetryButton()
    {
        Start();
    }
    public void BackButton()
    {
        SceneManager.LoadScene("MainGame");
        PlayerPrefs.SetInt("challenge",0);
    }
    public void DoneLesson()
    {
        lesson.SetActive(false);
        startTime = Time.time;
    }
    #endregion

    #region ChallengeLogic
    IEnumerator GetChallenge()
    {
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