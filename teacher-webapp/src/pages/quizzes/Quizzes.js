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
import { Typography } from "../../components/Wrappers/Wrappers";

export default function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const [id, setID] = useState([]);
  var [isLoading, setIsLoading] = useState(true);
  var [isQuizFound, setIsQuizFound] = useState(true);

  const url = "http://127.0.0.1:5000/";
  var email = "laoshi@gmail.com"; //should take from profile after

  useEffect(() => {
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
            fetch(url + `quizzes/?id=${id}`, {
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
  }, []);
  return (
    <>
      <PageTitle
        title="Quizzes"
        button={<EditForm profile={mockdata.profile} />}
      />
      {isLoading ? (
        <CircularProgress />
      ) : isQuizFound ? (
        <QuizzesTable
          quizzes={quizzes}
          setter={email}
          setter_id={id}
          classes={useStyles}
          theme={useTheme}
          url={url}
        />
      ) : (
        <h2>No Quizzes Found!</h2>
      )}
    </>
  );
}
