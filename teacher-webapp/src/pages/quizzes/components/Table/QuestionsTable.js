import React, { forwardRef } from "react";
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
  name,
  questions,
  handleDelete,
  handleUpdate,
  handleCreate,
  classes,
  isLoading,
}) {
  const [state, setState] = React.useState({
    columns: [
      { title: "ID", field: "id", editable: "never", deafultSort: "desc" },
      { title: "Name", field: "name" },
      { title: "Setter", field: "staff.name", editable: "never" },
      {
        title: "Quiz Type",
        field: "is_fast",
        lookup: { true: "Fast", false: "Normal" },
      },
      { title: "Attempts", field: "attempts.length", editable: "never" },
      { title: "Average", field: "average_score", editable: "never" },
      { title: "Highest", field: "highest_score", editable: "never" },
      { title: "Lowest", field: "lowest_score", editable: "never" },
      { title: "Starts On", field: "date_start", type: "date" },
      { title: "Ends On", field: "date_end", type: "date" },
    ],
    data: questions,
  });

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
                  <Typography variant="h6">Questions from {name}</Typography>
                </Grid>
              </Grid>
            }
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
      )}
    </React.Fragment>
  );
}
