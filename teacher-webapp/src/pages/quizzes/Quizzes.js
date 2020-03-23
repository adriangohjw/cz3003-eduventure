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
  var [isLoading, setIsLoading] = useState(true);

  const url = "http://127.0.0.1:5000/";
  var email = "laoshi@gmail.com"; //should take from profile after
  useEffect(() => {
    fetch(url + `staffs/?email=${email}`, {
      method: "GET",
    })
      .then(res => res.json())
      .then(response => {
        setQuizzes(response.quizzes);
        setIsLoading(false);
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
      ) : (
        <QuizzesTable
          quizzes={quizzes}
          classes={useStyles}
          theme={useTheme}
          setter={email}
        />
      )}
    </>
  );
}
