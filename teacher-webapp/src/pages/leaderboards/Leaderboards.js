import React, { useEffect, useState } from "react";
import { Button } from "@material-ui/core";

// styles
import useStyles from "./styles";
import { url } from "../../context/UserContext";

// components
import PageTitle from "../../components/PageTitle";
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

// #######################################################################
/* function getRandomData(length, min, max, multiplier = 10, maxDiff = 10) {
  var array = new Array(length).fill();
  let lastValue;

  return array.map((item, index) => {
    let randomValue = Math.floor(Math.random() * multiplier + 1);

    while (
      randomValue <= min ||
      randomValue >= max ||
      (lastValue && randomValue - lastValue > maxDiff)
    ) {
      randomValue = Math.floor(Math.random() * multiplier + 1);
    }

    lastValue = randomValue;

    return { value: randomValue };
  });
}

function getMainChartData() {
  var resultArray = [];
  var tablet = getRandomData(31, 3500, 6500, 7500, 1000);
  var desktop = getRandomData(31, 1500, 7500, 7500, 1500);
  var mobile = getRandomData(31, 1500, 7500, 7500, 1500);

  for (let i = 0; i < tablet.length; i++) {
    resultArray.push({
      tablet: tablet[i].value,
      desktop: desktop[i].value,
      mobile: mobile[i].value,
    });
  }

  return resultArray;
}
 */
