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
  const [selectedTopicID, setSelectedTopicID] = useState(0);
  const [selectedLessonID, setSelectedLessonID] = useState(0);

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
    fetch(url + `questions/?id=${id}`, {
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

  const editQuestion = newData => {
    setIsLoading(true);
    console.log(newData);
    fetch(
      url + `questions/?id=${newData.id}&description=${newData.description}`,
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
    let { description } = newData;
    setIsLoading(true);

    fetch(
      url +
        `questions/?topic_id=${selectedTopicID}&lesson_id=${selectedLessonID}&description=${description}`,
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
          setSelectedTopicID={setSelectedTopicID}
          setSelectedLessonID={setSelectedLessonID}
          classes={classes}
          theme={useTheme}
        />
      )}
    </>
  );
}
