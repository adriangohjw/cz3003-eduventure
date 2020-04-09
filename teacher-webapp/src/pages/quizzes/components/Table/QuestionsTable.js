import React, { forwardRef, useEffect, useState } from "react";
import { Grid, Paper, CircularProgress } from "@material-ui/core";
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
} from "@material-ui/icons/";
import AssignmentIcon from "@material-ui/icons/Assignment";
import { Typography } from "../../../../components/Wrappers/Wrappers";

import MaterialTable from "material-table";

import { url } from "../../../../context/UserContext";

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
  Assignment: forwardRef((props, ref) => (
    <AssignmentIcon {...props} ref={ref} />
  )),
};

export default function QuestionsTable({
  rowData,
  // questions,
  handleDelete,
  handleUpdate,
  handleCreate,
  classes,
}) {
  const [questions, setQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
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
    retrieveQuestions(rowData.id);
  }, []);

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
                    Questions from {rowData.name}
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
                  handleCreate(newData);
                }),
              onRowUpdate: (newData, oldData) =>
                new Promise(resolve => {
                  handleUpdate(newData);
                }),
              onRowDelete: oldData =>
                new Promise(resolve => {
                  handleDelete(oldData["id"]);
                }),
            }}
          />
        </Paper>
      )}
    </React.Fragment>
  );
}
