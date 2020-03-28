import React, { useState, forwardRef } from "react";
import Paper from "@material-ui/core/Paper";
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
import AddCircleIcon from "@material-ui/icons/AddCircle";

import MaterialTable from "material-table";

import { useTheme } from "@material-ui/styles";

// styles
import useStyles from "../../styles";

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
};

export default function QuizzesTable({
  quizzes,
  handleDelete,
  handleUpdate,
  handleCreate,
}) {
  var classes = useStyles();
  var theme = useTheme();
  const [state, setState] = React.useState({
    columns: [
      { title: "ID", field: "id", editable: "never" },
      { title: "Name", field: "name" },
      { title: "Setter", field: "staff.name", editable: "never" },
      {
        title: "Quiz Type",
        field: "is_fast",
        lookup: { true: "Fast", false: "Normal" },
      },
      { title: "Attempts", field: "attempts.length", editable: "never" },
      { title: "Starts On", field: "date_start", type: "datetime" },
      { title: "Ends On", field: "date_end", type: "datetime" },
    ],
    data: quizzes,
  });

  return (
    <React.Fragment>
      <Paper className={classes.paper}>
        <MaterialTable
          title="Quizzes"
          columns={state.columns}
          data={state.data}
          icons={tableIcons}
          editable={{
            onRowAdd: newData =>
              new Promise(resolve => {
                setTimeout(() => {
                  resolve();
                  setState(prevState => {
                    const data = [...prevState.data];
                    data.push(newData);
                    return { ...prevState, data };
                  });
                }, 600);
              }).then(handleCreate(newData)),
            onRowUpdate: (newData, oldData) =>
              new Promise(resolve => {
                setTimeout(() => {
                  resolve();
                  if (oldData) {
                    setState(prevState => {
                      const data = [...prevState.data];
                      data[data.indexOf(oldData)] = newData;
                      return { ...prevState, data };
                    });
                  }
                }, 600);
              }).then(handleUpdate(newData)),
            onRowDelete: oldData =>
              new Promise(resolve => {
                setTimeout(() => {
                  resolve();
                  setState(prevState => {
                    const data = [...prevState.data];
                    data.splice(data.indexOf(oldData), 1);
                    return { ...prevState, data };
                  });
                }, 600);
              }).then(handleDelete(oldData["id"])),
          }}
        />
      </Paper>
    </React.Fragment>
  );
}
