import React, { useEffect, useState, forwardRef } from "react";
import { TextField } from "@material-ui/core";

// components
import CircularProgress from "@material-ui/core/CircularProgress";

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
import TopicLessonDropDown from "./components/TopicLessonDropDown";
import AssignmentIcon from "@material-ui/icons/Assignment";

import MaterialTable from "material-table";

import { url } from "../../context/UserContext";

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

export default function QuestionBank() {
  const [questions, setQuestions] = useState([]);
  var [isLoading, setIsLoading] = useState(true);
  const [selectedTopicID, setSelectedTopicID] = useState(0);
  const [selectedLessonID, setSelectedLessonID] = useState(0);
  //sets description for options
  const [correctOption, setCorrectOption] = useState({});
  const [incorrectOption1, setIncorrectOption1] = useState({});
  const [incorrectOption2, setIncorrectOption2] = useState({});
  const [incorrectOption3, setIncorrectOption3] = useState({});

  const textField = (setFunction, name, id, defaultValue) => {
    //text field used to render the options
    return (
      <TextField
        id={id}
        name={name}
        defaultValue={defaultValue}
        onChange={event => {
          setFunction({
            id: event.target.id,
            description: event.target.value,
          });
        }}
      />
    );
  };

  const [state, setState] = useState({
    options: { pageSize: 20 },
    columns: [
      { title: "ID", field: "id", editable: "never", defaultSort: "asc" },
      {
        title: "Topic",
        field: "topic_name",
        editable: "never",
      },
      {
        title: "Lesson",
        field: "lesson_name",
        editable: "onAdd",
        editComponent: () =>
          //custom edit component
          TopicLessonDropDown(
            "lesson",
            setSelectedLessonID,
            setSelectedTopicID,
          ),
      },
      { title: "Description", field: "description" },
      {
        title: "Correct Option",
        field: "choices",
        sorting: false,
        cellStyle: {
          //highlighted in green to depict correct option
          color: "#10a100",
        },
        render: rowData => {
          if (rowData.choices.length > 0) {
            return rowData.choices.find(choice => choice.id == 1).description;
          } else return null;
        },
        editComponent: rowData => {
          const _description =
            rowData.value != undefined
              ? rowData.value.find(v => v.id == 1).description
              : null;
          return textField(
            setCorrectOption,
            "correctOption",
            "1",
            _description,
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
          //render incorrect option and custom edit component
          if (rowData.choices.length > 1) {
            return rowData.choices.find(choice => choice.id == 2).description;
          } else return null;
        },
        editComponent: rowData => {
          const _description =
            rowData.value != undefined
              ? rowData.value.find(v => v.id == 2).description
              : null;
          return textField(
            setIncorrectOption1,
            "incorrectOption1",
            "2",
            _description,
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
          if (rowData.choices.length > 2) {
            return rowData.choices.find(choice => choice.id == 3).description;
          } else return null;
        },
        editComponent: rowData => {
          const _description =
            rowData.value != undefined
              ? rowData.value.find(v => v.id == 3).description
              : null;
          return textField(
            setIncorrectOption2,
            "incorrectOption2",
            "3",
            _description,
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
          if (rowData.choices.length > 3) {
            return rowData.choices.find(choice => choice.id == 4).description;
          } else return null;
        },
        editComponent: rowData => {
          const _description =
            rowData.value != undefined
              ? rowData.value.find(v => v.id == 4).description
              : null;
          return textField(
            setIncorrectOption3,
            "incorrectOption3",
            "4",
            _description,
          );
        },
      },
    ],
  });

  const retrieveQuestions = () => {
    fetch(url + `questions/all`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("No Questions Found");
        }
      })
      .then(response => {
        setQuestions(response.questions);
        setIsLoading(false);
      })
      .catch(error => console.log(error));
  };

  const deleteQuestion = oldData => {
    setIsLoading(true);
    let { id, choices } = oldData;
    Promise.all(
      //have to delete all question options first before deleting question itself if not API will throw error
      choices.map(choice => {
        fetch(
          url +
            `question_choices/?question_id=${id}&questionChoice_id=${choice.id}`,
          { method: "DELETE" },
        );
      }),
    ).then(() => {
      fetch(url + `questions/?id=${id}`, {
        method: "DELETE",
      })
        .then(res => {
          if (res.ok) {
            return res.json();
          } else {
            setIsLoading(false);
            throw new Error(res.json().error);
          }
        })
        .then(res => {
          retrieveQuestions();
          alert(res.message);
        })
        .catch(error => {
          console.error("Error:", error);
          alert(error);
        });
    });
  };

  const isEmpty = obj => {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
  };

  const editQuestion = (oldData, newData) => {
    setIsLoading(true);
    var _correct;
    var _incorrect1;
    var _incorrect2;
    var _incorrect3;

    if (isEmpty(correctOption)) {
      _correct = oldData["choices"].find(choice => choice["id"] == "1");
    } else _correct = correctOption;
    if (isEmpty(incorrectOption1)) {
      _incorrect1 = oldData.choices.find(choice => choice.id == 2);
    } else _incorrect1 = incorrectOption1;
    if (isEmpty(incorrectOption2)) {
      _incorrect2 = oldData.choices.find(choice => choice.id == 3);
    } else _incorrect2 = incorrectOption2;
    if (isEmpty(incorrectOption3)) {
      _incorrect3 = oldData.choices.find(choice => choice.id == 4);
    } else _incorrect3 = incorrectOption3;
    Promise.all([
      //calls API to update question description and all 4 options singularly since there is no batch update function in API for now
      fetch(
        url + `questions/?id=${newData.id}&description=${newData.description}`,
        { method: "PUT" },
      ),
      fetch(
        url +
          `question_choices/?question_id=${newData.id}&questionChoice_id=${
            _correct.id
          }&description=${_correct.description}&is_correct=${true}`,
        { method: "PUT" },
      ),
      fetch(
        url +
          `question_choices/?question_id=${newData.id}&questionChoice_id=${
            _incorrect1.id
          }&description=${_incorrect1.description}&is_correct=${false}`,
        { method: "PUT" },
      ),
      fetch(
        url +
          `question_choices/?question_id=${newData.id}&questionChoice_id=${
            _incorrect2.id
          }&description=${_incorrect2.description}&is_correct=${false}`,
        { method: "PUT" },
      ),
      fetch(
        url +
          `question_choices/?question_id=${newData.id}&questionChoice_id=${
            _incorrect3.id
          }&description=${_incorrect3.description}&is_correct=${false}`,
        { method: "PUT" },
      ),
    ])
      .then(() => {
        retrieveQuestions();
        alert("Updated successfully");
        return;
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  const createQuestion = newData => {
    let { description } = newData;
    //set options to have a reminder if teacher does not fill it in
    const _correctOption =
      correctOption.description != ""
        ? correctOption.description
        : "Please fill in an option!";
    const _incorrectOption1 =
      incorrectOption1.description != ""
        ? incorrectOption1.description
        : "Please fill in an option!";
    const _incorrectOption2 =
      incorrectOption2.description != ""
        ? incorrectOption2.description
        : "Please fill in an option!";
    const _incorrectOption3 =
      incorrectOption3.description != ""
        ? incorrectOption3.description
        : "Please fill in an option!";
    setIsLoading(true);
    fetch(
      url +
        `questions/?topic_id=${selectedTopicID}&lesson_id=${selectedLessonID}&description=${description}`,
      {
        method: "POST",
      },
    )
      .then(questionResponse => {
        if (questionResponse.ok) {
          return questionResponse.json();
        } else {
          retrieveQuestions();
          throw new Error("Server Error!");
        }
      })
      .then(response => {
        //have to nest the subsequent post requests as the question must be created before options can be created for it
        const id = response.id;
        fetch(
          url +
            `question_choices/?question_id=${id}&description=${_correctOption}&is_correct=${true}`,
          { method: "POST" },
        )
          .then(res => {
            if (!res.ok) {
              retrieveQuestions();
              throw new Error("Server Error!");
            }
            return;
          })
          .then(() => {
            fetch(
              url +
                `question_choices/?question_id=${id}&description=${_incorrectOption1}&is_correct=${false}`,
              { method: "POST" },
            )
              .then(res => {
                if (!res.ok) {
                  retrieveQuestions();
                  throw new Error("Server Error!");
                }
                return;
              })
              .then(() => {
                fetch(
                  url +
                    `question_choices/?question_id=${id}&description=${_incorrectOption2}&is_correct=${false}`,
                  { method: "POST" },
                )
                  .then(res => {
                    if (!res.ok) {
                      retrieveQuestions();
                      throw new Error("Server Error!");
                    }
                    return;
                  })
                  .then(() => {
                    fetch(
                      url +
                        `question_choices/?question_id=${id}&description=${_incorrectOption3}&is_correct=${false}`,
                      { method: "POST" },
                    )
                      .then(res => {
                        if (!res.ok) {
                          retrieveQuestions();
                          throw new Error("Server Error!");
                        } else {
                          retrieveQuestions();
                        }
                      })
                      .catch(error => {
                        console.error("Error:", error);
                        alert("something went wrong");
                      });
                  })
                  .catch(error => {
                    console.error("Error:", error);
                    alert("something went wrong");
                  });
              })
              .catch(error => {
                console.error("Error:", error);
                alert("something went wrong");
              });
          })
          .catch(error => {
            console.error("Error:", error);
            alert("something went wrong");
          });
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  useEffect(() => {
    retrieveQuestions();
  }, []);

  return (
    <>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <MaterialTable
          title="All Questions"
          columns={state.columns}
          data={questions}
          icons={tableIcons}
          options={state.options}
          editable={{
            onRowAdd: newData =>
              new Promise(resolve => {
                createQuestion(newData);
              }),
            onRowUpdate: (newData, oldData) =>
              new Promise(resolve => {
                editQuestion(oldData, newData);
              }),
            onRowDelete: oldData =>
              new Promise(resolve => {
                deleteQuestion(oldData);
              }),
          }}
        />
      )}
    </>
  );
}
