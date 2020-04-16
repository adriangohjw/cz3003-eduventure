import React, { useEffect, useState } from "react";
import { useTheme } from "@material-ui/styles";
// styles
import useStyles from "./styles";

// components
import SyllabusTable from "./components/SyllabusTable";
import CircularProgress from "@material-ui/core/CircularProgress";

import { url } from "../../context/UserContext";

export default function Quizzes() {
  const [data, setData] = useState({
    topics: [],
    lessons: [],
  });
  var [isLoading, setIsLoading] = useState(true);

  var classes = useStyles();

  const retrieveData = () => {
    Promise.all([
      fetch(url + `topics/all`, {
        method: "GET",
      }),
      fetch(url + `lessons/all`, {
        method: "GET",
      }),
    ])
      .then(responses => {
        if (responses.find(res => !res.ok) == undefined) {
          return Promise.all(responses.map(res => res.json()));
        } else {
          setIsLoading(false);
          throw new Error("couldn't connect to server!");
        }
      })
      .then(([topicResponse, lessonResponse]) => {
        setData({
          topics: topicResponse.topics,
          lessons: lessonResponse.lessons,
        });
        setIsLoading(false);
      })
      .catch(error => console.log(error));
  };

  const handleDelete = (type, delete_id, topic_id) => {
    // when called from topic delete, delete_id is actually topic_id
    setIsLoading(true);
    const final_url =
      type == "topic"
        ? url + `topics/?id=${delete_id}`
        : url + `lessons/?topic_id=${topic_id}&lesson_id=${delete_id}`;
    fetch(final_url, {
      method: "DELETE",
    })
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveData();
          throw new Error("Couldn't delete!");
        }
      })
      .then(() => {
        retrieveData();
        alert("Deleted successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  const handleUpdate = (type, newData, topic_id) => {
    setIsLoading(true);
    let { id, name, content, url_link } = newData;
    const final_url =
      type == "topic"
        ? url + `topics/?id=${id}&name=${name}`
        : url +
          `lessons/?topic_id=${topic_id}&name=${name}&content=${content}&url_link=${url_link}`;
    fetch(final_url, {
      method: "PUT",
    })
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveData();
          throw new Error("Server Error!");
        }
      })
      .then(() => {
        retrieveData();
        alert("Updated successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  const handleCreate = (type, newData, topic_id) => {
    let { name, content, url_link } = newData;
    setIsLoading(true);
    const final_url =
      type == "topic"
        ? url + `topics/?name=${name}`
        : url +
          `lessons/?topic_id=${topic_id}&name=${name}&content=${content}&url_link=${url_link}`;
    fetch(final_url, {
      method: "POST",
    })
      .then(response => {
        if (response.ok) {
          response.json();
        } else {
          retrieveData();
          throw new Error("Server Error!");
        }
      })
      .then(() => {
        retrieveData();
        alert("Created successfully");
      })
      .catch(error => {
        console.error("Error:", error);
        alert("something went wrong");
      });
  };

  useEffect(() => {
    retrieveData();
  }, []);

  return (
    <>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <SyllabusTable
          data={data}
          handleDelete={handleDelete}
          handleCreate={handleCreate}
          handleUpdate={handleUpdate}
          classes={classes}
          theme={useTheme}
        />
      )}
    </>
  );
}
