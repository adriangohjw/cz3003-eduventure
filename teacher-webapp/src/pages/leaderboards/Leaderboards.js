import React, { useState } from "react";
import { Grid } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import mockdata from "./mockdata";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";
import Table from "./components/Table/Table";

class Leaderboards extends React.Component {
  //https://www.youtube.com/watch?v=akxsFgM7DPA
  constructor(props) {
    super(props);
    this.state = {
      data: mockdata.table2,
      scoreAsc: true,
    };
    this.sortBy = this.sortBy.bind(this);
  }

  sortBy(key) {
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
  }

  render() {
    return (
      <div>
        <PageTitle title="Leaderboards" button="Latest Reports" />
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget title="Week 9" upperTitle noBodyPadding>
              <Table data={this.state.data} sortBy={this.sortBy} />
            </Widget>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default Leaderboards;

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
