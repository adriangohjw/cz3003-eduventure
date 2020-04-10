import React, { forwardRef, useState } from "react";
import {
  Paper,
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
      { title: "Description", field: "description" },
      { title: "Topic ID", field: "topic_id" },
      {
        title: "Lesson ID",
        field: "lesson_id",
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
          onRowClick={(event, rowData, togglePanel) => {
            console.log("rowData", rowData);
            console.log("event", event);
            togglePanel();
          }}
          detailPanel={[
            {
              icon: () => <QuestionAnswerIcon />,
              tooltip: "Questions",
              render: rowData => {
                const choices = rowData.choices.map(function(choice) {
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
                          style={{ color: choice.is_correct ? "green" : "red" }}
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
    </React.Fragment>
  );
}
