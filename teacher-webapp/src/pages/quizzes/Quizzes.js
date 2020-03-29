import React, { useEffect, useState } from "react";
import { useTheme } from "@material-ui/styles";
// styles
import useStyles from "./styles";

// components
import mockdata from "./mockdata";
import PageTitle from "../../components/PageTitle/PageTitle";
import EditForm from "./components/EditForm/EditForm";
import QuizzesTable from "./components/Table/QuizzesTable";
import CircularProgress from "@material-ui/core/CircularProgress";

//TODO:
// 1) change to select one only
// 2) add new quiz POST
// 3) Edit quiz PUT

export default function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const [id, setID] = useState([]);
  var [isLoading, setIsLoading] = useState(true);
  var [isQuizFound, setIsQuizFound] = useState(true);

  const url = new URL("http://127.0.0.1:5000/");
  var email = "laoshi@gmail.com"; //should take from profile after

  const retrieveQuizzes = () => {
    fetch(url + `staffs/?email=${email}`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setIsLoading(false);
          setIsQuizFound(false);
          throw new Error("No Quizzes Found for this Staff ID");
        }
      })
      .then(response => {
        setID(response.id);
        return response.quizzes.map(quiz => quiz.id);
      })
      .then(allQuizIDs => {
        return Promise.all(
          allQuizIDs.map(id =>
            fetch(url + `quizzes/overall?id=${id}`, {
              method: "GET",
            })
              .then(res => res.json())
              .then(response => {
                return response;
              })
              .catch(error => {
                console.log(error);
              }),
          ),
        );
      })
      .then(result => {
        return result;
      })
      .then(allQuizDetails => {
        setQuizzes(allQuizDetails);
        setIsLoading(false);
        setIsQuizFound(true);
      })
      .catch(error => console.log(error));
  };

  const deleteQuiz = id => {
    setIsLoading(true);
    fetch(url + `quizzes/?id=${id}`, {
      method: "DELETE",
    })
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveQuizzes();
          throw new Error("Couldn't delete!");
        }
      })
      .then(() => {
        retrieveQuizzes();
        alert("Deleted successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  const updateQuiz = newData => {
    setIsLoading(true);
    var keys = [];
    for (var key in newData) {
      if (
        newData.hasOwnProperty(key) &&
        key != "id" &&
        key != "staff" &&
        key != "attempts"
      ) {
        keys.push(key);
      }
    }
    console.log("keys", keys);
    let quiz_id = newData["id"];
    // newData["is_fast"] = newData["is_fast"] ? "True" : "False";
    Promise.all(
      keys.map(key => {
        let value = newData[key];
        fetch(url + `quizzes/?id=${quiz_id}&col=${key}&value=${value}`, {
          method: "PUT",
        })
          .then(response => {
            if (response.ok) {
              response.json();
            } else {
              throw new Error("Server Error!");
            }
          })
          .catch(error => {
            console.error("Error:", error);
            alert("something went wrong");
          });
      }),
    ).then(() => {
      retrieveQuizzes();
      alert("Updated successfully");
    });
  };

  const createQuiz = newData => {
    let { name, is_fast, date_start, date_end } = newData;
    setIsLoading(true);
    let fake_date_start = "2020-02-02"; //remember to delete after adrian updates api
    let fake_date_end = "2020-02-03";
    is_fast = is_fast == true ? "True" : "False";
    date_start =
      date_start.getUTCFullYear() +
      "-" +
      (date_start.getUTCMonth() + 1) +
      "-" +
      date_start.getUTCDate();
    date_end =
      date_end.getUTCFullYear() +
      "-" +
      (date_end.getUTCMonth() + 1) +
      "-" +
      date_end.getUTCDate();
    fetch(
      url +
        `quizzes/?staff_id=${id}&name=${name}&is_fast=${is_fast}&date_start=${date_start}&date_end=${date_end}`,
      {
        method: "POST",
      },
    )
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveQuizzes();
          throw new Error("Server Error!");
        }
      })
      .then(() => {
        retrieveQuizzes();
        alert("Created successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  useEffect(() => {
    retrieveQuizzes();
  }, []);

  return (
    <>
      {isLoading ? (
        <CircularProgress />
      ) : isQuizFound ? (
        <QuizzesTable
          quizzes={quizzes}
          setter={email}
          handleDelete={deleteQuiz}
          handleCreate={createQuiz}
          handleUpdate={updateQuiz}
          classes={useStyles}
          theme={useTheme}
        />
      ) : (
        <h2>No Quizzes Found!</h2>
      )}
    </>
  );
}
