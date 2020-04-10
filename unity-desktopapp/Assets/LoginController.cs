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
    public GameObject signup;
    public GameObject signupFailed;

    void Start()
    {
        userField = transform.Find("UsernameField").GetComponent<TMP_InputField>();
        passField = transform.Find("PasswordField").GetComponent<TMP_InputField>();
        incorrect.SetActive(false);
        signup.SetActive(false);
        signupFailed.SetActive(false);
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
    public void SignUpStart()
    {
        signup.SetActive(true);
    }
    public void SignUpClose()
    {
        signup.SetActive(false);
    }
    public void SignUpComplete()
    {
        TMP_InputField username = GameObject.Find("SignupUserField").GetComponent<TMP_InputField>();
        TMP_InputField password1 = GameObject.Find("SignupPassField1").GetComponent<TMP_InputField>();
        TMP_InputField password2 = GameObject.Find("SignupPassField2").GetComponent<TMP_InputField>();
        TMP_InputField matricNum = GameObject.Find("SignupMatricField").GetComponent<TMP_InputField>();
        if ((string.IsNullOrEmpty(username.text)) || (string.IsNullOrEmpty(password1.text)) || (string.IsNullOrEmpty(password2.text)) || (string.IsNullOrEmpty(matricNum.text)))
        {
            signupFailed.SetActive(true);
            TMP_Text errorMsg = signupFailed.GetComponentInChildren<TMP_Text>();
            errorMsg.text = "Please fill in every field before signing up.";
        }
        else if (password1.text != password2.text)
        {
            signupFailed.SetActive(true);
            TMP_Text errorMsg = signupFailed.GetComponentInChildren<TMP_Text>();
            errorMsg.text = "Passwords do not match. Please try again.";
        }
        else
        {
            StartCoroutine(SignUp(username.text,password1.text,matricNum.text));
        }
    }
    public void SignUpFailedClose()
    {
        signupFailed.SetActive(false);
    }
    IEnumerator SignUp(string user,string pass,string matric)
    {
        string url = string.Format("http://127.0.0.1:5000/students/?email={0}&password={1}&matriculation_number={2}",user,pass,matric);
        using (UnityWebRequest webRequest = UnityWebRequest.Post(url,"null"))
        {
            yield return webRequest.SendWebRequest();
            UserDetails userDets = JsonUtility.FromJson<UserDetails>(webRequest.downloadHandler.text);
            SignupCompleted(userDets);
        }
    }
    private void SignupCompleted(UserDetails userDets)
    {
        if (userDets.error != null)
        {
            signupFailed.SetActive(true);
            TMP_Text errorMsg = signupFailed.GetComponentInChildren<TMP_Text>();
            errorMsg.text = userDets.error;
        }
        else
        {
            signupFailed.SetActive(true);
            signup.SetActive(false);
            TMP_Text errorMsg = signupFailed.GetComponentInChildren<TMP_Text>();
            errorMsg.text = "Completed Sign Up, You can now log in.";
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
    public string matriculation_number;
}

