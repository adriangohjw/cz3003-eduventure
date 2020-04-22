import React, { useEffect, useState } from "react";
import { Button } from "@material-ui/core";

// styles
import useStyles from "./styles";
import { url } from "../../context/UserContext";

// components
import CircularProgress from "@material-ui/core/CircularProgress";
import LeaderboardTable from "./components/Table/LeaderboardTable";

export default function Leaderboards() {
  var [isLoading, setIsLoading] = useState(true);
  const [leaderboard, setLeaderboard] = useState([]);
  var classes = useStyles();
  const retrieveLeaderboard = () => {
    fetch(url + `statistics/leaderboard`, {
      method: "GET",
    })
      .then(response => response.json())
      .then(data => {
        setLeaderboard(data.scores);
        setIsLoading(false);
      })
      .catch(error => console.log(error));
  };
  useEffect(() => {
    //fetch leaderboard data on component render
    retrieveLeaderboard();
  }, []);

  return (
    <div>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <LeaderboardTable leaderboard={leaderboard} classes={classes} />
      )}
    </div>
  );
}
