import React, { forwardRef, useEffect, useState } from "react";
import {
  Grid,
  Paper,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@material-ui/core";
import {
  AddBox,
  ArrowDownward,
  Check,
  ChevronLeft,
  ChevronRight,
  Clear,
  DeleteOutline,
  Edit,
  FilterList,
  FirstPage,
  LastPage,
  Remove,
  SaveAlt,
  Search,
  ViewColumn,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
} from "@material-ui/icons/";
import QuestionAnswerIcon from "@material-ui/icons/QuestionAnswer";
import { Typography } from "../../../../components/Wrappers/Wrappers";

import MaterialTable from "material-table";

import { url } from "../../../../context/UserContext";
import QuestionsDropDown from "./QuestionsDropDown";
// import { useTheme } from "@material-ui/styles";

const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => (
    <ChevronLeft {...props} ref={ref} />
  )),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />),
};

export default function QuestionsTable({ quizData, classes }) {
  const [questions, setQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedQuestionID, setSelectedQuestionID] = useState(0);

  const [columns, setColumns] = useState([
    {
      title: "ID",
      field: "question.id",
      editable: "never",
      defaultSort: "asc",
    },
    {
      title: "Description",
      field: "question.description",
      editComponent: () => QuestionsDropDown(setSelectedQuestionID),
    },
    {
      title: "Topic",
      field: "question.topic_id",
      editable: "never",
    },
    {
      title: "Lesson",
      field: "question.lesson_id",
      editable: "never",
    },
  ]);

  const retrieveQuestions = quiz_id => {
    fetch(url + `quizzes/questions?quiz_id=${quiz_id}`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setIsLoading(false);
          throw new Error("No Questions Found for this Quiz");
        }
      })
      .then(response => {
        setQuestions(response.questions);
        setIsLoading(false);
      })
      .catch(error => console.log(error));
  };

  useEffect(() => {
    retrieveQuestions(quizData.id);
  }, []);

  const handleDeleteQuestion = oldData => {
    setIsLoading(true);
    fetch(
      url +
        `quizzes/questions?quiz_id=${quizData.id}&question_id=${oldData.question.id}`,
      {
        method: "DELETE",
      },
    )
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setIsLoading(false);
          throw new Error("No Questions Found for this Quiz");
        }
      })
      .then(response => {
        retrieveQuestions(quizData.id);
      })
      .catch(error => console.log(error));
  };

  const handleNewQuestion = newData => {
    setIsLoading(true);
    console.log("selectedQuestionID is", selectedQuestionID);
    fetch(
      url +
        `quizzes/questions?quiz_id=${quizData.id}&question_id=${selectedQuestionID}`,
      {
        method: "POST",
      },
    )
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setIsLoading(false);
          throw new Error("No Questions Found for this Quiz");
        }
      })
      .then(response => {
        retrieveQuestions(quizData.id);
      })
      .catch(error => console.log(error));
  };

  return (
    <React.Fragment>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <Paper className={classes.questionsTable}>
          <MaterialTable
            title={
              <Grid
                container={true}
                direction="row"
                justify="space-around"
                alignItems="center"
              >
                <Grid item={true}>
                  <Typography variant="h6">
                    Questions from {quizData.name}
                  </Typography>
                </Grid>
              </Grid>
            }
            columns={columns}
            data={questions}
            icons={tableIcons}
            editable={{
              onRowAdd: newData =>
                new Promise(resolve => {
                  handleNewQuestion(newData);
                }),
              // onRowUpdate: (newData, oldData) => {},
              onRowDelete: oldData =>
                new Promise(resolve => {
                  handleDeleteQuestion(oldData);
                }),
            }}
            detailPanel={[
              //show options
              {
                icon: () => <QuestionAnswerIcon />,
                tooltip: "Choices",
                render: rowData => {
                  const choices = rowData.question.choices.map(function(
                    choice,
                  ) {
                    return (
                      <>
                        <ListItem key={choice.id}>
                          <ListItemIcon>
                            {choice.is_correct ? (
                              <CheckCircleIcon key={choice.id} />
                            ) : (
                              <CancelIcon key={choice.id} />
                            )}
                          </ListItemIcon>
                          <ListItemText
                            primary={choice.description}
                            key={choice.id}
                            style={{
                              color: choice.is_correct ? "green" : "red",
                            }}
                          />
                        </ListItem>
                        <Divider />
                      </>
                    );
                  });
                  return (
                    <React.Fragment>
                      <Divider />
                      <List component="nav">{choices}</List>
                    </React.Fragment>
                  );
                },
              },
            ]}
          />
        </Paper>
      )}
    </React.Fragment>
  );
}
