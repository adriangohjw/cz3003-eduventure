import React, { useEffect, useState } from "react";
import { useTheme } from "@material-ui/styles";
// styles
import useStyles from "./styles";

// components
import QuizzesTable from "./components/Table/QuizzesTable";
import CircularProgress from "@material-ui/core/CircularProgress";

import { url } from "../../context/UserContext";

export default function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const [id, setID] = useState([]);
  var [isLoading, setIsLoading] = useState(true);
  var [isQuizFound, setIsQuizFound] = useState(true);

  var classes = useStyles();

  var email = localStorage.getItem("email");

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

  const formatDate = date => {
    // console.log("dategetutcfullyear", date.getUTCFullYear());
    // let result =
    //   date.getUTCFullYear() +
    //   "-" +
    //   (date.getUTCMonth() + 1) +
    //   "-" +
    //   date.getUTCDate();
    // console.log("result", result);
    let result = new Date(date);
    result = result.toISOString().split("T")[0];
    return result;
  };

  const updateQuiz = newData => {
    setIsLoading(true);
    console.log("newData", newData);

    fetch(
      url +
        `quizzes/?id=${newData.id}&name=${newData.name}&is_fast=${
          newData.is_fast
        }&date_start=${formatDate(newData.date_start)}&date_end=${formatDate(
          newData.date_end,
        )}`,
      {
        method: "PUT",
      },
    )
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          throw new Error("Server Error!");
        }
      })
      .then(() => {
        retrieveQuizzes();
        alert("Updated successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  const createQuiz = newData => {
    let { name, is_fast, date_start, date_end } = newData;
    setIsLoading(true);
    is_fast = is_fast == "true" || is_fast == true ? "true" : "false";
    date_start = formatDate(date_start);
    date_end = formatDate(date_end);
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
          handleDelete={deleteQuiz}
          handleCreate={createQuiz}
          handleUpdate={updateQuiz}
          classes={classes}
          theme={useTheme}
        />
      ) : (
        <h2>No Quizzes Found!</h2>
      )}
    </>
  );
}
