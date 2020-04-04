import React, { useEffect, useState } from "react";
import { Grid } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import mockdata from "./mockdata";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";
import CircularProgress from "@material-ui/core/CircularProgress";
import Table from "./components/Table/Table";

export default function Leaderboards() {
  var [isLoading, setIsLoading] = useState(true);
  const [quiz_attempts, setQuizAttempts] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/quiz_attempts/leaderboard`, {
      method: "GET",
    })
      .then(response => response.json())
      .then(data => {
        setQuizAttempts(data.students);
        setIsLoading(false);
      });
  }, []);
  const sortBy = key => {
    console.log("sortBy called with ", key);

    this.setState(prevState => ({
      data: this.state.data.sort(
        this.state.scoreAsc === true
          ? (a, b) => a[key.toLowerCase()] < b[key.toLowerCase()]
          : (a, b) => b[key.toLowerCase()] < a[key.toLowerCase()],
      ),
      scoreAsc: !prevState.scoreAsc,
    }));
    //console.log(this.state.data);
  };

  return (
    <div>
      <PageTitle title="Leaderboard" button="Latest Reports" />
      {isLoading ? (
        <CircularProgress />
      ) : (
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget title="Quiz " upperTitle noBodyPadding>
              <Table data={quiz_attempts} sortBy={sortBy} />
            </Widget>
          </Grid>
        </Grid>
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
