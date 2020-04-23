using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;

public class LoginController : MonoBehaviour
{
    private TMP_InputField userField;
    private TMP_InputField passField;
    public GameObject incorrect;
    public GameObject signup;
    public GameObject signupFailed;
    private AudioSource main_audio;
    public AudioSource clickSound;
    public AudioSource closeSound;

    void Start()
    {
        //Initializes variables and sets pop up boxes to be inactive.
        userField = transform.Find("UsernameField").GetComponent<TMP_InputField>();
        passField = transform.Find("PasswordField").GetComponent<TMP_InputField>();
        incorrect.SetActive(false);
        signup.SetActive(false);
        signupFailed.SetActive(false);
        main_audio = GameObject.Find("Background").GetComponent<AudioSource>();
    }
    void Update()
    {
        //Constantly checks the volume setting to ensure sound effects play at correct volume
        main_audio.volume = PlayerPrefs.GetFloat("volume");
        clickSound.volume = PlayerPrefs.GetFloat("volume");
        closeSound.volume = PlayerPrefs.GetFloat("volume");
    }
    #region Login Functions
    public void Login()
    {
        //Triggered by clicking login button
        clickSound.Play();
        StartCoroutine(GetRequest("http://127.0.0.1:5000/users/auth?email="+userField.text+"&password="+passField.text));
    }
    IEnumerator GetRequest(string uri)
    {
        //Sends request to authentication API
        using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
        {
            yield return webRequest.SendWebRequest();
            UserDetails userDets = JsonUtility.FromJson<UserDetails>(webRequest.downloadHandler.text);
            VerifyLogin(userDets);
        }
    }
    private void VerifyLogin(UserDetails userDets)
    {
        //Processes results of authentication API
        if (userDets.error != null)
        {
            incorrect.SetActive(true);
            TMP_Text incorrectText = GameObject.Find("IncorrectText").GetComponent<TMP_Text>();
            incorrectText.text = userDets.error;
        }
        else
        {
            PlayerPrefs.SetString("userID",userDets.id);
            PlayerPrefs.SetString("userEmail",userDets.email);
            StartCoroutine(GetCourse());
        }
    }
    IEnumerator GetCourse()
    {
        //If successful login, get more details about the student and change to main game scene
        string url = "http://127.0.0.1:5000/students/courses?user_email=" + PlayerPrefs.GetString("userEmail");
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();
            CourseDetails courseDet = JsonUtility.FromJson<CourseDetails>(webRequest.downloadHandler.text);
            PlayerPrefs.SetString("userCourse",courseDet.courses[0].course_index);
            SceneManager.LoadScene("MainGame");
        }
    }
    public void IncorrectDismiss()
    {
        //Close incorrect box
        closeSound.Play();
        incorrect.SetActive(false);
    }
    #endregion
    #region Sign-up checks and processes
    public void SignUpStart()
    {
        //Triggered by sign up button
        clickSound.Play();
        signup.SetActive(true);
    }
    public void SignUpComplete()
    {
        //Triggered by Sign up complete button
        //Checks if any field is empty or passwords do not match
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
    IEnumerator SignUp(string user,string pass,string matric)
    {
        //Calls sign up API with set email,password and matriculation number
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
        //After successful signup, display success message
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
    public void SignUpClose()
    {
        //Close sign up box
        closeSound.Play();
        signup.SetActive(false);
    }
    public void SignUpFailedClose()
    {
        //Close sign up fail/success message box
        closeSound.Play();
        signupFailed.SetActive(false);
    }
    #endregion
}
#region JSON Classes
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
[Serializable]
public class CourseDetails
{
    public string count_courses;
    public CoursesDetails[] courses;
    public string email;
    public int id;
    public string name;
}
[Serializable]
public class CoursesDetails
{
    public string course_index;
    public string created_at;
}
#endregion