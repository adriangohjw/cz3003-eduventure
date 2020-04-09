import React, { useEffect, useState } from "react";
import { useTheme } from "@material-ui/styles";
// styles
import useStyles from "./styles";

// components
import CircularProgress from "@material-ui/core/CircularProgress";

import { url } from "../../context/UserContext";

export default function Syllabus() {
  const [id, setID] = useState([]);
  var [isLoading, setIsLoading] = useState(false);

  var classes = useStyles();

  var email = localStorage.getItem("email"); //should take from profile after

  // const retrieveQuizzes = () => {
  //   fetch(url + `staffs/?email=${email}`, {
  //     method: "GET",
  //   })
  //     .then(res => {
  //       if (res.ok) {
  //         return res.json();
  //       } else {
  //         setIsLoading(false);
  //         setIsQuizFound(false);
  //         throw new Error("No Quizzes Found for this Staff ID");
  //       }
  //     })
  //     .then(response => {
  //       setID(response.id);
  //       return response.quizzes.map(quiz => quiz.id);
  //     })
  //     .then(allQuizIDs => {
  //       return Promise.all(
  //         allQuizIDs.map(id =>
  //           fetch(url + `quizzes/overall?id=${id}`, {
  //             method: "GET",
  //           })
  //             .then(res => res.json())
  //             .then(response => {
  //               return response;
  //             })
  //             .catch(error => {
  //               console.log(error);
  //             }),
  //         ),
  //       );
  //     })
  //     .then(result => {
  //       return result;
  //     })
  //     .then(allQuizDetails => {
  //       setQuizzes(allQuizDetails);
  //       setIsLoading(false);
  //       setIsQuizFound(true);
  //     })
  //     .catch(error => console.log(error));
  // };

  // const deleteQuiz = id => {
  //   setIsLoading(true);
  //   fetch(url + `quizzes/?id=${id}`, {
  //     method: "DELETE",
  //   })
  //     .then(response => {
  //       if (response.ok) {
  //         response.json();
  //       } else {
  //         retrieveQuizzes();
  //         throw new Error("Couldn't delete!");
  //       }
  //     })
  //     .then(() => {
  //       retrieveQuizzes();
  //       alert("Deleted successfully");
  //     })
  //     .catch(error => {
  //       console.error("Error:", error);
  //       alert("something went wrong");
  //     });
  // };

  // const formatDate = date => {
  //   // console.log("dategetutcfullyear", date.getUTCFullYear());
  //   // let result =
  //   //   date.getUTCFullYear() +
  //   //   "-" +
  //   //   (date.getUTCMonth() + 1) +
  //   //   "-" +
  //   //   date.getUTCDate();
  //   // console.log("result", result);
  //   let result = new Date(date);
  //   result = result.toISOString().split("T")[0];
  //   return result;
  // };

  // const updateQuiz = newData => {
  //   setIsLoading(true);
  //   var keys = [];
  //   const uneditable_keys = [
  //     "id",
  //     "staff",
  //     "attempts",
  //     "average_score",
  //     "lowest_score",
  //     "highest_score",
  //   ];
  //   for (var key in newData) {
  //     if (newData.hasOwnProperty(key) && !uneditable_keys.includes(key)) {
  //       keys.push(key);
  //     }
  //   }
  //   let quiz_id = newData["id"];
  //   console.log("keys", keys);
  //   // newData["is_fast"] = newData["is_fast"] ? "True" : "False";
  //   Promise.all(
  //     keys.map(key => {
  //       let value = newData[key];
  //       if (key == "date_start" || key == "date_end") {
  //         value = formatDate(value);
  //       }
  //       fetch(url + `quizzes/?id=${quiz_id}&col=${key}&value=${value}`, {
  //         method: "PUT",
  //       })
  //         .then(response => {
  //           if (response.ok) {
  //             response.json();
  //           } else {
  //             throw new Error("Server Error!");
  //           }
  //         })
  //         .catch(error => {
  //           console.error("Error:", error);
  //           alert("something went wrong");
  //         });
  //     }),
  //   ).then(() => {
  //     // retrieveQuizzes();
  //     alert("Updated successfully");
  //   });
  // };

  // const createQuiz = newData => {
  //   let { name, is_fast, date_start, date_end } = newData;
  //   setIsLoading(true);
  //   is_fast = is_fast == true ? "True" : "False";
  //   date_start = formatDate(date_start);
  //   date_end = formatDate(date_end);
  //   fetch(
  //     url +
  //       `quizzes/?staff_id=${id}&name=${name}&is_fast=${is_fast}&date_start=${date_start}&date_end=${date_end}`,
  //     {
  //       method: "POST",
  //     },
  //   )
  //     .then(response => {
  //       if (response.ok) {
  //         response.json();
  //       } else {
  //         retrieveQuizzes();
  //         throw new Error("Server Error!");
  //       }
  //     })
  //     .then(() => {
  //       retrieveQuizzes();
  //       alert("Created successfully");
  //     })
  //     .catch(error => {
  //       console.error("Error:", error);
  //       alert("something went wrong");
  //     });
  // };

  // useEffect(() => {
  //   retrieveQuizzes();
  // }, []);

  return <>{isLoading ? <CircularProgress /> : <h2>Hello World</h2>}</>;
}