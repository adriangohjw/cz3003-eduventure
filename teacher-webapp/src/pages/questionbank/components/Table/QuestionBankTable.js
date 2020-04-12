import React, { forwardRef, useState } from "react";
import {
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  TextField,
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

import AssignmentIcon from "@material-ui/icons/Assignment";

import MaterialTable from "material-table";

// import { useTheme } from "@material-ui/styles";

const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => (
    <ChevronRight {...props} ref={ref} />
  )),
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

export default function QuestionBankTable({
  questions,
  handleDelete,
  handleUpdate,
  handleCreate,
  classes,
}) {
  const [state, setState] = useState({
    isLoading: true,
    columns: [
      { title: "ID", field: "id", editable: "never", deafultSort: "desc" },
      { title: "Topic", field: "topic_name" },
      {
        title: "Lesson",
        field: "lesson_name",
      },
      { title: "Description", field: "description" },
      {
        title: "Correct Option",
        field: "choices",
        sorting: false,
        cellStyle: {
          color: "#10a100",
        },
        render: rowData => {
          const correct = rowData.choices.filter(choice => choice.is_correct)[0]
            .description;
          return correct;
        },
        editComponent: rowData => {
          if (rowData.value != undefined) {
            // for update Question
            const correctOption = rowData.value.filter(
              choice => choice.is_correct == true,
            )[0];
            return (
              <TextField
                id={correctOption.id.toString()}
                defaultValue={correctOption.description}
              />
            );
          } else {
            // for add new Question
            return <TextField id="0" />;
          }
        },
      },
      {
        title: "Other Option",
        field: "choices",
        sorting: false,
        cellStyle: {
          color: "#b01020",
        },
        render: rowData => {
          const incorrect = rowData.choices.filter(
            choice => choice.is_correct == false,
          );
          return incorrect.length > 0 ? incorrect[0].description : null;
        },
        editComponent: rowData => {
          if (rowData.value != undefined) {
            // for edit Question
            const incorrect = rowData.value.filter(
              choice => !choice.is_correct,
            );
            return incorrect.length > 0 ? (
              <TextField
                id={incorrect[0].id.toString()}
                defaultValue={incorrect[0].description}
              />
            ) : (
              <TextField id="1" />
            );
          } else {
            //for add new Question
            return <TextField id="1" />;
          }
        },
      },
      {
        title: "Other Option",
        field: "choices",
        sorting: false,
        cellStyle: {
          color: "#b01020",
        },
        render: rowData => {
          const incorrect = rowData.choices.filter(
            choice => choice.is_correct == false,
          );
          return incorrect.length > 1 ? incorrect[1].description : null;
        },
        editComponent: rowData => {
          if (rowData.value != undefined) {
            // for edit Question
            const incorrect = rowData.value.filter(
              choice => !choice.is_correct,
            );
            return incorrect.length > 1 ? (
              <TextField
                id={incorrect[1].id.toString()}
                defaultValue={incorrect[1].description}
              />
            ) : (
              <TextField id="2" />
            );
          } else {
            //for add new Question
            return <TextField id="2" />;
          }
        },
      },
      {
        title: "Other Option",
        field: "choices",
        sorting: false,
        cellStyle: {
          color: "#b01020",
        },
        render: rowData => {
          const incorrect = rowData.choices.filter(
            choice => choice.is_correct == false,
          );
          return incorrect.length > 2 ? incorrect[2].description : null;
        },
        editComponent: rowData => {
          if (rowData.value != undefined) {
            // for edit Question
            const incorrect = rowData.value.filter(
              choice => !choice.is_correct,
            );
            return incorrect.length > 2 ? (
              <TextField
                id={incorrect[2].id.toString()}
                defaultValue={incorrect[2].description}
              />
            ) : (
              <TextField id="3" />
            );
          } else {
            //for add new Question
            return <TextField id="3" />;
          }
        },
      },
    ],
    data: questions,
  });

  return (
    <React.Fragment>
      <Paper className={classes.quizTable}>
        <MaterialTable
          title="All Questions"
          columns={state.columns}
          data={state.data}
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
    </React.Fragment>
  );
}
