using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;

public class LoginController : MonoBehaviour
{
    private TMP_InputField userField;
    private TMP_InputField passField;
    public GameObject incorrect;

    void Start()
    {
        userField = transform.Find("UsernameField").GetComponent<TMP_InputField>();
        passField = transform.Find("PasswordField").GetComponent<TMP_InputField>();
        incorrect.SetActive(false);
    }

    public void Login()
    {
        //TO IMPLEMENT
        //Login request to database
        Debug.Log(userField.text);
        Debug.Log(passField.text);
        if ((userField.text=="username") && (passField.text=="password"))
        {
            SceneManager.LoadScene("MainGame");
            //PlayerPrefs.SetInt("userID",userID) for API calling
        }
        else
        {
            incorrect.SetActive(true);
        }
    }

    public void IncorrectDismiss()
    {
        incorrect.SetActive(false);
    }
}
