import React, { useEffect, useState } from "react";
import { useTheme } from "@material-ui/styles";
// styles
import useStyles from "./styles";

// components
import QuestionBankTable from "./components/Table/QuestionBankTable";
import CircularProgress from "@material-ui/core/CircularProgress";

import { url } from "../../context/UserContext";

export default function QuestionBank() {
  const [questions, setQuestions] = useState([]);
  var [isLoading, setIsLoading] = useState(true);

  var classes = useStyles();

  const retrieveQuestions = () => {
    fetch(url + `questions/all`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("No Questions Found");
        }
      })
      .then(response => {
        setQuestions(response.questions);
        setIsLoading(false);
      })
      .catch(error => console.log(error));
  };

  const deleteQuestion = id => {
    setIsLoading(true);
    fetch(url + `quizzes/?id=${id}`, {
      method: "DELETE",
    })
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveQuestions();
          throw new Error("Couldn't delete!");
        }
      })
      .then(() => {
        retrieveQuestions();
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

  const editQuestion = newData => {
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
        retrieveQuestions();
        alert("Updated successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  const createQuestion = newData => {
    let { topic_id, lesson_id, description } = newData;
    setIsLoading(true);

    fetch(
      url +
        `questions/?topic_id=${topic_id}&lesson_id=${lesson_id}&description=${description}`,
      {
        method: "POST",
      },
    )
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveQuestions();
          throw new Error("Server Error!");
        }
      })
      .then(() => {
        retrieveQuestions();
        alert("Created successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  useEffect(() => {
    retrieveQuestions();
  }, []);

  return (
    <>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <QuestionBankTable
          questions={questions}
          handleDelete={deleteQuestion}
          handleCreate={createQuestion}
          handleUpdate={editQuestion}
          classes={classes}
          theme={useTheme}
        />
      )}
    </>
  );
}
