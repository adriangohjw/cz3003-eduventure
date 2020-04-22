import React, { forwardRef, useState } from "react";
import { Paper } from "@material-ui/core";
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

export default function LeaderboardTable({ leaderboard, classes }) {
  const [state, setState] = useState({
    isLoading: true,
    columns: [
      { title: "ID", field: "id", editable: "never" },
      { title: "Name", field: "name", editable: "never" },
      { title: "Matric No.", field: "matriculation_num", editable: "never" },
      {
        title: "Score",
        field: "score",
        editable: "never",
        defaultSort: "desc",
        cellStyle: {
          //emphasize score column
          color: "#0000A0",
          fontWeight: "bold",
        },
      },
    ],
    options: { pageSize: leaderboard.length < 20 ? leaderboard.length : 20 }, // shows only required rows if less than 20
    data: leaderboard,
  });

  return (
    <React.Fragment>
      <Paper className={classes.quizTable}>
        <MaterialTable
          title="Leaderboard"
          columns={state.columns}
          data={state.data}
          icons={tableIcons}
          options={state.options}
        />
      </Paper>
    </React.Fragment>
  );
}
