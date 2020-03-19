import React, { useState } from "react";
import { useTheme } from "@material-ui/styles";

// styles
import useStyles from "./styles";

// components
import mockdata from "./mockdata";
import PageTitle from "../../components/PageTitle/PageTitle";
import EditForm from "./components/EditForm/EditForm";
import QuizzesTable from "./components/Table/QuizzesTable";
import { Typography } from "../../components/Wrappers/Wrappers";

export default function Quizzes(props) {
  var classes = useStyles();
  var theme = useTheme();

  return (
    <>
      <PageTitle title="Quizzes" button={<EditForm />} />
      <QuizzesTable data={mockdata} classes={classes} theme={theme} />
    </>
  );
}
