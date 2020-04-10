using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using TMPro;
using UnityEngine.SceneManagement;

public static class QuizManager 
{
    private static int userID;
    private static int quizID;
    private static string data;
    private static bool done = false;

    public static QuizQuestion GetQuiz(int questionNum)
    {
        //TO IMPLEMENT
        //pass playerID and cropID to database to get relevant quiz json
        //StartCoroutine(GetRequest(URL))
        //StartCoroutine(GetRequest("http://127.0.0.1:5000/users/?email=adriangohjw13@gmail.com"));
        while (done == false)
        {
            Debug.Log("NotDone");
        }
        Debug.Log(data);
        string stringJsonData = "{\"Question\":\"This is question 1\",\"Option1\":\"This is option 1\",\"Option2\":\"This would be option 2\",\"Option3\":\"And This is Option 3\",\"Option4\":\"Lasty, Option 4\"}";
        QuizQuestion question = new QuizQuestion();
        question = JsonUtility.FromJson<QuizQuestion>(stringJsonData);
        question.Question = string.Format("This is question {0}",questionNum);
        return question;
    }
    public static void SendAnswer(int answer)
    {
        //TO IMPLEMENT
        //send answer selected to database
        Debug.Log(answer);
    }
    static IEnumerator GetRequest(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            Debug.Log(webRequest.downloadHandler.text);
            data =  webRequest.downloadHandler.text;
            done = true;
        }
    }

}

[Serializable]
public class QuizQuestion
{
    public string Question;
    public string Option1;
    public string Option2;
    public string Option3;
    public string Option4;
    
}