import React, { forwardRef, useState } from "react";
import { Paper, TextField } from "@material-ui/core";
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
import TopicLessonDropDown from "../TopicLessonDropDown";
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
  setSelectedLessonID,
  setSelectedTopicID,
  setCorrectOption,
  setIncorrectOption1,
  setIncorrectOption2,
  setIncorrectOption3,
  classes,
}) {
  const textField = (setOptionFunction, name, id, defaultValue) => {
    return (
      <TextField
        id={id}
        name={name}
        defaultValue={defaultValue}
        onChange={event => {
          setOptionFunction({
            id: id,
            description: event.target.value,
          });
        }}
      />
    );
  };

  const [state, setState] = useState({
    columns: [
      { title: "ID", field: "id", editable: "never", deafultSort: "desc" },
      {
        title: "Topic",
        field: "topic_name",
        editable: "onAdd",
        editComponent: () => TopicLessonDropDown("topic", setSelectedTopicID),
      },
      {
        title: "Lesson",
        field: "lesson_name",
        editable: "onAdd",
        editComponent: () => TopicLessonDropDown("lesson", setSelectedLessonID),
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
          const correct = rowData.choices.filter(
            choice => choice.is_correct == true,
          );
          return correct.length > 0 ? correct[0].description : null;
        },
        editComponent: rowData => {
          if (rowData.value != undefined) {
            // for update Question
            const correctOption = rowData.value.filter(
              choice => choice.is_correct == true,
            )[0];
            return correctOption != undefined
              ? textField(
                  setCorrectOption,
                  "correctOption",
                  correctOption.id.toString(),
                  correctOption.description,
                )
              : textField(setCorrectOption, "correctOption", "1", null);
          } else {
            // for add new Question
            return textField(setCorrectOption, "correctOption", "1", null);
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
            return incorrect.length > 0
              ? textField(
                  setIncorrectOption1,
                  "incorrectOption1",
                  incorrect[0].id.toString(),
                  incorrect[0].description,
                )
              : textField(setIncorrectOption1, "incorrectOption1", "2", null);
          }
          //for add new Question
          else
            return textField(
              setIncorrectOption1,
              "incorrectOption1",
              "2",
              null,
            );
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
            return incorrect.length > 1
              ? textField(
                  setIncorrectOption2,
                  "incorrectOption2",
                  incorrect[1].id.toString(),
                  incorrect[1].description,
                )
              : textField(setIncorrectOption2, "incorrectOption2", "3", null);
          }
          //for add new Question
          else
            return textField(
              setIncorrectOption2,
              "incorrectOption2",
              "3",
              null,
            );
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
            return incorrect.length > 2
              ? textField(
                  setIncorrectOption3,
                  "incorrectOption3",
                  incorrect[2].id.toString(),
                  incorrect[2].description,
                )
              : textField(setIncorrectOption3, "incorrectOption3", "4", null);
          }
          //for add new Question
          else
            return textField(
              setIncorrectOption3,
              "incorrectOption3",
              "4",
              null,
            );
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
                handleUpdate(oldData, newData);
              }),
            onRowDelete: oldData =>
              new Promise(resolve => {
                handleDelete(oldData);
              }),
          }}
        />
      </Paper>
    </React.Fragment>
  );
}
