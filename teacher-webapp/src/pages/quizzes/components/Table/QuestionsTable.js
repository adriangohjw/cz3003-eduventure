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
  const handleOnChange = (event, value) => {
    console.log(value);
  };
  const [columns, setColumns] = useState([
    {
      title: "ID",
      field: "question.id",
      editable: "never",
      deafultSort: "desc",
    },
    {
      title: "Description",
      field: "question.description",
      editable: "onAdd",
      editComponent: () => QuestionsDropDown(handleOnChange),
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

  const handleNewQuestion = questionData => {
    console.log(questionData);
  };

  const handleDeleteQuestion = question_id => {};

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
              onRowAdd: newData => {
                // new Promise(resolve => {
                //   handleNewQuestion(newData);
                // })
              },
              onRowDelete: oldData =>
                new Promise(resolve => {
                  handleDeleteQuestion(oldData["id"]);
                }),
            }}
            detailPanel={[
              {
                icon: () => <QuestionAnswerIcon />,
                tooltip: "Questions",
                render: rowData => {
                  console.log(rowData);
                  const choices = rowData.question.choices.map(function(
                    choice,
                  ) {
                    return (
                      <>
                        <ListItem key={choice.id}>
                          <ListItemIcon>
                            {choice.is_correct ? (
                              <CheckCircleIcon />
                            ) : (
                              <CancelIcon />
                            )}
                          </ListItemIcon>
                          <ListItemText
                            primary={choice.description}
                            key={choice.id}
                          />
                        </ListItem>
                        <Divider />
                      </>
                    );
                  });
                  return (
                    <React.Fragment>
                      <Divider />
                      <List component="nav" aria-label="main mailbox folders">
                        {choices}
                      </List>
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
