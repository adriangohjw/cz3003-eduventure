import React, { forwardRef, useState, setState, useEffect } from "react";
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

import SchoolIcon from "@material-ui/icons/School";

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
};

export default function SyllabusTable({
  data,
  handleDelete,
  handleUpdate,
  handleCreate,
  classes,
}) {
  const [state, setState] = useState({
    isLoading: true,
    topicColumns: [
      { title: "ID", field: "id", editable: "never", defaultSort: "asc" },
      { title: "Name", field: "name" },
    ],
    lessonColumns: [
      { title: "ID", field: "id", editable: "never", defaultSort: "asc" },
      { title: "Name", field: "name" },
      { title: "Content", field: "content" },
      { title: "Further Learning", field: "url_link" },
    ],
  });

  return (
    <React.Fragment>
      <Paper className={classes.topicsTable}>
        <MaterialTable
          title="Topics"
          columns={state.topicColumns}
          data={data.topics}
          icons={tableIcons}
          editable={{
            onRowAdd: newData =>
              new Promise(resolve => {
                handleCreate("topic", newData);
              }),
            onRowUpdate: (newData, oldData) =>
              new Promise(resolve => {
                handleUpdate("topic", newData);
              }),
            onRowDelete: oldData =>
              new Promise(resolve => {
                handleDelete("topic", oldData["id"]);
              }),
          }}
          detailPanel={[
            {
              icon: () => <SchoolIcon />,
              tooltip: "Lessons",
              render: rowData => {
                return (
                  <Paper className={classes.lessonsTable}>
                    <MaterialTable
                      title="Lessons"
                      columns={state.lessonColumns}
                      data={data.lessons.filter(
                        lesson => lesson.topic_id == rowData.id,
                      )}
                      icons={tableIcons}
                      editable={{
                        onRowAdd: newData =>
                          new Promise(resolve => {
                            handleCreate("lesson", newData, rowData.id);
                          }),
                        onRowUpdate: (newData, oldData) =>
                          new Promise(resolve => {
                            handleUpdate("lesson", newData, rowData.id);
                          }),
                        onRowDelete: oldData =>
                          new Promise(resolve => {
                            handleDelete("lesson", oldData["id"], rowData.id);
                          }),
                      }}
                    />
                  </Paper>
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
