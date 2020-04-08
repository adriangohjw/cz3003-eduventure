using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
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
        StartCoroutine(GetRequest("http://127.0.0.1:5000/users/auth?email="+userField.text+"&password="+passField.text));
    }

    public void IncorrectDismiss()
    {
        incorrect.SetActive(false);
    }

    IEnumerator GetRequest(string uri)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
        {
            yield return webRequest.SendWebRequest();
            UserDetails userDets = JsonUtility.FromJson<UserDetails>(webRequest.downloadHandler.text);
            VerifyLogin(userDets);
        }
    }
    private void VerifyLogin(UserDetails userDets)
    {
        if (userDets.error != null)
        {
            incorrect.SetActive(true);
            TMP_Text incorrectText = GameObject.Find("IncorrectText").GetComponent<TMP_Text>();
            incorrectText.text = userDets.error;
            
        }
        else
        {
            UserController.userID = userDets.id;
            SceneManager.LoadScene("MainGame");
        }
    }
}
[Serializable]
public class UserDetails
{
    public string created_at;
    public string email;
    public string encrypted_password;
    public string id;
    public string name;
    public string error;
}

