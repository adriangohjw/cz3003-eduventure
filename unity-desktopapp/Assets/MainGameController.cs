using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;


public class MainGameController : MonoBehaviour
{
    public GameObject cropMenu;
    public GameObject pointsMenu;
    public GameObject quizMenu;
    private string cropSelected;
    private int questionNum;
    // Start is called before the first frame update
    void Start()
    {
        cropMenu.SetActive(false);
        pointsMenu.SetActive(false);
        quizMenu.SetActive(false);
        int i;
        Button[] crops = new Button[6];
        TMP_Text[] cropsText = new TMP_Text[6];
        TMP_Text pointsText = GameObject.Find("PointsText").GetComponent<TMP_Text>();
        //either hardcode crops and location or replace with a dynamic way
        string[] cropNames = new string[6];
        cropNames = CropManager.GetCropsNames(1);
        for (i=0;i<6;i++)
        { 
            string s = string.Format("Crop{0}",i+1);
            Button _crops = GameObject.Find(s.ToString()).GetComponent<Button>();
            crops[i] = _crops;
            cropsText[i] = crops[i].GetComponentInChildren<TMP_Text>();
            cropsText[i].text = cropNames[i];
        }
        pointsText.text = PointsManager.GetPoints(1000).ToString();
    }

    public void CropClick()
    {
        //query database for statistic with Crop name
        cropSelected = EventSystem.current.currentSelectedGameObject.GetComponentInChildren<TMP_Text>().text;
        cropMenu.SetActive(true);
        string[] cropContent = new string[2];
        cropContent = CropManager.GetCropsMenu(cropSelected);
        TMP_Text plantTitle = GameObject.Find("PlantTitle").GetComponent<TMP_Text>();
        plantTitle.text = cropContent[0];
        TMP_Text plantStats = GameObject.Find("PlantContent").GetComponent<TMP_Text>();
        plantStats.text = cropContent[1];

    }
    public void CropMenuClose()
    {
        cropMenu.SetActive(false);
    }

    public void LogOut()
    {
        //TO IMPLEMENT
        //save the game to database or something
        Application.Quit();
    }
    public void PointsClick()
    {
        pointsMenu.SetActive(true);
        TMP_Text pointsTitle = GameObject.Find("PointsTitle").GetComponent<TMP_Text>();
        TMP_Text pointsContent = GameObject.Find("PointsContent").GetComponent<TMP_Text>();
        pointsContent.text = PointsManager.GetLeaderboard(100);
    }
    public void PointsClickOut()
    {
        pointsMenu.SetActive(false);
    }
    public void QuizStart()
    {
        questionNum = 1;
        quizMenu.SetActive(true);
        UpdateQuestion();
    }
    public void UpdateQuestion()
    {
        TMP_Text quizTitle = GameObject.Find("QuizTitle").GetComponent<TMP_Text>();
        TMP_Text quizQuestion = GameObject.Find("QuizQuestion").GetComponent<TMP_Text>();
        Button[] options = new Button[4];
        TMP_Text[] answers = new TMP_Text[4];
        for (int i =0;i<4;i++)
        {
            string s = string.Format("Option{0}",i);
            options[i] = GameObject.Find(s.ToString()).GetComponent<Button>();
            answers[i] = options[i].GetComponentInChildren<TMP_Text>();
        }

        QuizQuestion question = QuizManager.GetQuiz(questionNum);
        quizQuestion.text = question.Question;
        answers[0].text = question.Option1;
        answers[1].text = question.Option2;
        answers[2].text = question.Option3;
        answers[3].text = question.Option4;
    }
    public void QuizNextQuestion()
    {
        if (questionNum==10)
        {
            quizMenu.SetActive(false);
            cropMenu.SetActive(true);
            TMP_Text plantStats = GameObject.Find("PlantContent").GetComponent<TMP_Text>();
            //update content of the plant stats after finishing quiz
            plantStats.text = cropSelected.ToString() + " Statistics from Database";
        }
        else
        {
            questionNum= questionNum+1;
            UpdateQuestion();
        }
    }
}
