import React, { forwardRef, useState, setState } from "react";
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
import QuestionsTable from "./QuestionsTable";

import { url } from "../../../../context/UserContext";

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

export default function QuizzesTable({
  quizzes,
  handleDelete,
  handleUpdate,
  handleCreate,
  classes,
}) {
  const [state, setState] = useState({
    isLoading: true,
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
    data: quizzes,
  });

  const retrieveQuestions = quiz_id => {
    fetch(url + `quizzes/questions?quiz_id=${quiz_id}`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setState(state.isLoading, false);
          throw new Error("No Questions Found for this Quiz");
        }
      })
      .then(response => {
        // setState(state.isLoading, false);
        console.log("response.questions is", response.questions);
        // setState(state.questions, response.questions);
      })
      .catch(error => console.log(error));
  };

  return (
    <React.Fragment>
      <Paper className={classes.quizTable}>
        <MaterialTable
          title="Quizzes"
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
              icon: () => <AssignmentIcon />,

              tooltip: "Questions",
              render: rowData => {
                return (
                  <QuestionsTable
                    handleDelete={handleDelete}
                    handleCreate={handleCreate}
                    handleUpdate={handleUpdate}
                    classes={classes}
                    quizData={rowData}
                  />
                );
              },
            },
          ]}
        />
      </Paper>
    </React.Fragment>
  );
}

// setTimeout(() => {
//   resolve();
//   setState(prevState => {
//     const data = [...prevState.data];
//     data.push(newData);
//     return { ...prevState, data };
//   });
// }, 600);

// setTimeout(() => {
//   resolve();
//   setState(prevState => {
//     const data = [...prevState.data];
//     data.splice(data.indexOf(oldData), 1);
//     return { ...prevState, data };
//   });
// }, 600);

// setTimeout(() => {
//   resolve();
//   if (oldData) {
//     setState(prevState => {
//       const data = [...prevState.data];
//       data[data.indexOf(oldData)] = newData;
//       return { ...prevState, data };
//     });
//   }
// }, 600);
