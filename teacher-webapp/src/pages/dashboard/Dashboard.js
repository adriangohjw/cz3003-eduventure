import React, { useState, useEffect } from "react";
import {
  Grid,
  LinearProgress,
  Select,
  OutlinedInput,
  MenuItem,
  CircularProgress,
} from "@material-ui/core";
import { useTheme } from "@material-ui/styles";
import {
  ResponsiveContainer,
  ComposedChart,
  BarChart,
  AreaChart,
  LineChart,
  Line,
  Area,
  PieChart,
  Pie,
  Cell,
  YAxis,
  XAxis,
  Bar,
  Tooltip,
} from "recharts";

// styles
import useStyles from "./styles";

// components
import mock from "./mock";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";
import Dot from "../../components/Sidebar/components/Dot";
import Table from "./components/Table/Table";
import BigStat from "./components/BigStat/BigStat";

import { url } from "../../context/UserContext";

const PieChartData = [
  { name: "Group A", value: 400, color: "primary" },
  { name: "Group B", value: 300, color: "secondary" },
  { name: "Group C", value: 300, color: "warning" },
  { name: "Group D", value: 200, color: "success" },
];

const colors = [
  "#D27370",
  "#D07483",
  "#C77895",
  "#B87EA4",
  "#A486B0",
  "#8C8EB6",
  "#7295B7",
  "#589BB2",
  "#449FA7",
  "#3CA299",
  "#44A487",
  "#55A474",
  "#6AA262",
  "#7F9F52",
  "#959B47",
  "#A99642",
  "#BC8F44",
];

export default function Dashboard(props) {
  var classes = useStyles();
  var theme = useTheme();

  // local
  var [mainChartState, setMainChartState] = useState("");
  var [ss1ChartData, setss1ChartData] = useState([]);
  var [ss2ChartData, setss2ChartData] = useState({
    selectedss2: 0,
    ss2Options: [],
    data: [],
  });
  var [isLoading, setIsLoading] = useState({
    ss1: true,
    ss2: true,
  });

  const getss1ChartData = () => {
    fetch(url + `statistics/stat`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setIsLoading({
            ...isLoading,
            ss1: false,
          });
          throw new Error(res.error);
        }
      })
      .then(response => {
        setss1ChartData(response.stats);
        setIsLoading({
          ...isLoading,
          ss1: false,
        });
      })
      .catch(error => console.log(error));
  };

  const getss2ChartData = () => {
    fetch(url + `statistics/lesson_completed`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setIsLoading({
            ...isLoading,
            ss2: false,
          });
          throw new Error(res.error);
        }
      })
      .then(response => {
        const [formattedData, options] = formatss2Data(response.courses);
        setss2ChartData({
          ...ss2ChartData,
          data: formattedData,
          ss2Options: options,
        });
        setIsLoading({
          ...isLoading,
          ss2: false,
        });
      })
      .catch(error => console.log(error));
  };

  const formatss2Data = data => {
    var options = [];
    data.map(course => {
      options.push(course.course_index);
      var flattened_lessons = [];
      course.progress.map(topic => {
        flattened_lessons.push(...topic.lessons);
      });
      course.progress = flattened_lessons;
    });
    return [data, options];
  };

  useEffect(() => {
    getss1ChartData();
    getss2ChartData();
  }, []);

  return (
    <>
      <PageTitle title="Dashboard" button="Latest Reports" />
      <Grid container spacing={4}>
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Visits Today"
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <div className={classes.visitsNumberContainer}>
              <Typography size="xl" weight="medium">
                12, 678
              </Typography>
              <LineChart
                width={55}
                height={30}
                data={[
                  { value: 10 },
                  { value: 15 },
                  { value: 10 },
                  { value: 17 },
                  { value: 18 },
                ]}
                margin={{ left: theme.spacing(2) }}
              >
                <Line
                  type="natural"
                  dataKey="value"
                  stroke={theme.palette.success.main}
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </div>
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  Registrations
                </Typography>
                <Typography size="md">860</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  Sign Out
                </Typography>
                <Typography size="md">32</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  Rate
                </Typography>
                <Typography size="md">3.25%</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        <Grid item lg={3} md={8} sm={6} xs={12}>
          <Widget
            title="App Performance"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <div className={classes.performanceLegendWrapper}>
              <div className={classes.legendElement}>
                <Dot color="warning" />
                <Typography
                  color="text"
                  colorBrightness="secondary"
                  className={classes.legendElementText}
                >
                  Integration
                </Typography>
              </div>
              <div className={classes.legendElement}>
                <Dot color="primary" />
                <Typography
                  color="text"
                  colorBrightness="secondary"
                  className={classes.legendElementText}
                >
                  SDK
                </Typography>
              </div>
            </div>
            <div className={classes.progressSection}>
              <Typography
                size="md"
                color="text"
                colorBrightness="secondary"
                className={classes.progressSectionTitle}
              >
                Integration
              </Typography>
              <LinearProgress
                variant="determinate"
                value={30}
                classes={{ barColorPrimary: classes.progressBar }}
                className={classes.progress}
              />
            </div>
            <div>
              <Typography
                size="md"
                color="text"
                colorBrightness="secondary"
                className={classes.progressSectionTitle}
              >
                SDK
              </Typography>
              <LinearProgress
                variant="determinate"
                value={55}
                classes={{ barColorPrimary: classes.progressBar }}
                className={classes.progress}
              />
            </div>
          </Widget>
        </Grid>
        <Grid item lg={3} md={8} sm={6} xs={12}>
          <Widget
            title="Server Overview"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <div className={classes.serverOverviewElement}>
              <Typography
                color="text"
                colorBrightness="secondary"
                className={classes.serverOverviewElementText}
              >
                60% / 37°С / 3.3 Ghz
              </Typography>
              <div className={classes.serverOverviewElementChartWrapper}>
                <ResponsiveContainer height={50} width="99%">
                  <AreaChart data={getRandomData(10)}>
                    <Area
                      type="natural"
                      dataKey="value"
                      stroke={theme.palette.secondary.main}
                      fill={theme.palette.secondary.light}
                      strokeWidth={2}
                      fillOpacity="0.25"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div className={classes.serverOverviewElement}>
              <Typography
                color="text"
                colorBrightness="secondary"
                className={classes.serverOverviewElementText}
              >
                54% / 31°С / 3.3 Ghz
              </Typography>
              <div className={classes.serverOverviewElementChartWrapper}>
                <ResponsiveContainer height={50} width="99%">
                  <AreaChart data={getRandomData(10)}>
                    <Area
                      type="natural"
                      dataKey="value"
                      stroke={theme.palette.primary.main}
                      fill={theme.palette.primary.light}
                      strokeWidth={2}
                      fillOpacity="0.25"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div className={classes.serverOverviewElement}>
              <Typography
                color="text"
                colorBrightness="secondary"
                className={classes.serverOverviewElementText}
              >
                57% / 21°С / 3.3 Ghz
              </Typography>
              <div className={classes.serverOverviewElementChartWrapper}>
                <ResponsiveContainer height={50} width="99%">
                  <AreaChart data={getRandomData(10)}>
                    <Area
                      type="natural"
                      dataKey="value"
                      stroke={theme.palette.warning.main}
                      fill={theme.palette.warning.light}
                      strokeWidth={2}
                      fillOpacity="0.25"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </Widget>
        </Grid>
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget title="Revenue Breakdown" upperTitle className={classes.card}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <ResponsiveContainer width="100%" height={144}>
                  <PieChart margin={{ left: theme.spacing(2) }}>
                    <Pie
                      data={PieChartData}
                      innerRadius={45}
                      outerRadius={60}
                      dataKey="value"
                    >
                      {PieChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={theme.palette[entry.color].main}
                        />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </Grid>
              <Grid item xs={6}>
                <div className={classes.pieChartLegendWrapper}>
                  {PieChartData.map(({ name, value, color }, index) => (
                    <div key={color} className={classes.legendItemContainer}>
                      <Dot color={color} />
                      <Typography style={{ whiteSpace: "nowrap" }}>
                        &nbsp;{name}&nbsp;
                      </Typography>
                      <Typography color="text" colorBrightness="secondary">
                        &nbsp;{value}
                      </Typography>
                    </div>
                  ))}
                </div>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        {/* <Grid item xs={12}>
          {isLoading.ss1 == true ? (
            <CircularProgress />
          ) : (
            <Widget
              bodyClass={classes.mainChartBody}
              header={
                <div className={classes.mainChartHeader}>
                  <Typography
                    variant="h5"
                    color="text"
                    colorBrightness="secondary"
                  >
                    Daily Line Chart
                  </Typography>
                  <div className={classes.mainChartHeaderLabels}>
                    <div className={classes.mainChartHeaderLabel}>
                      <Dot color="warning" />
                      <Typography className={classes.mainChartLegentElement}>
                        Tablet
                      </Typography>
                    </div>
                    <div className={classes.mainChartHeaderLabel}>
                      <Dot color="primary" />
                      <Typography className={classes.mainChartLegentElement}>
                        Mobile
                      </Typography>
                    </div>
                    <div className={classes.mainChartHeaderLabel}>
                      <Dot color="primary" />
                      <Typography className={classes.mainChartLegentElement}>
                        Desktop
                      </Typography>
                    </div>
                  </div>
                  <Select
                    value={mainChartState}
                    onChange={e => setMainChartState(e.target.value)}
                    input={
                      <OutlinedInput
                        labelWidth={0}
                        classes={{
                          notchedOutline: classes.mainChartSelectRoot,
                          input: classes.mainChartSelect,
                        }}
                      />
                    }
                    autoWidth
                  >
                    <MenuItem value="avg_score">Average Score</MenuItem>
                    <MenuItem value="max_score">Highest Score</MenuItem>
                    <MenuItem value="min_score">Lowest Score</MenuItem>
                  </Select>
                </div>
              }
            >
              <ResponsiveContainer width="100%" minWidth={500} height={350}>
                <ComposedChart
                  margin={{ top: 0, right: -15, left: -15, bottom: 0 }}
                  data={ss1ChartData[0].progress}
                >
                  <YAxis
                    // ticks={[0, 2500, 5000, 7500]}
                    tick={{
                      fill: theme.palette.text.hint + "80",
                      fontSize: 14,
                    }}
                    stroke={theme.palette.text.hint + "80"}
                    tickLine={false}
                  />
                  <XAxis
                    // tickFormatter={i => i + 1}
                    tick={{
                      fill: theme.palette.text.hint + "80",
                      fontSize: 14,
                    }}
                    stroke={theme.palette.text.hint + "80"}
                    tickLine={false}
                    dataKey="quizzes.name"
                  />
                  <Area
                  type="natural"
                  dataKey="desktop"
                  fill={theme.palette.background.light}
                  strokeWidth={0}
                  activeDot={false}
                />
                  <Line
                    type="natural"
                    dataKey="avg_score"
                    stroke={theme.palette.primary.main}
                    strokeWidth={2}
                    dot={false}
                    activeDot={false}
                  />
                  <Line
                  type="linear"
                  dataKey="tablet"
                  stroke={theme.palette.warning.main}
                  strokeWidth={2}
                  dot={{
                    stroke: theme.palette.warning.dark,
                    strokeWidth: 2,
                    fill: theme.palette.warning.main,
                  }}
                />
                </ComposedChart>
              </ResponsiveContainer>
            </Widget>
          )}
        </Grid> */}
        <Grid item xs={12}>
          {isLoading.ss2 == true ? (
            <CircularProgress />
          ) : (
            <Widget
              bodyClass={classes.mainChartBody}
              header={
                <div className={classes.mainChartHeader}>
                  <Typography
                    variant="h5"
                    color="text"
                    colorBrightness="secondary"
                  >
                    Lesson Progress Chart
                  </Typography>
                  <div className={classes.mainChartHeaderLabels}>
                    <div className={classes.mainChartHeaderLabel}>
                      <Typography className={classes.mainChartLegentElement}>
                        {ss2ChartData.ss2Options[ss2ChartData.selectedss2]}
                      </Typography>
                    </div>
                  </div>
                  <Select
                    value={ss2ChartData.selectedss2}
                    onChange={e => {
                      setss2ChartData({
                        ...ss2ChartData,
                        selectedss2: e.target.value,
                      });
                    }}
                    displayEmpty
                    input={
                      <OutlinedInput
                        labelWidth={0}
                        classes={{
                          notchedOutline: classes.mainChartSelectRoot,
                          input: classes.mainChartSelect,
                        }}
                      />
                    }
                    autoWidth
                  >
                    {ss2ChartData.ss2Options.map((option, index) => {
                      return (
                        <MenuItem value={index} key={index}>
                          {option}
                        </MenuItem>
                      );
                    })}
                  </Select>
                </div>
              }
            >
              <ResponsiveContainer width="100%" minWidth={500} height={350}>
                <BarChart
                  margin={{ top: 0, right: -15, left: -15, bottom: 0 }}
                  data={ss2ChartData.data[ss2ChartData.selectedss2].progress} // set it as 0 first until we can dynamically set it
                >
                  <YAxis
                    // ticks={[0, 2500, 5000, 7500]}
                    tick={{
                      fill: theme.palette.text.hint + "80",
                      fontSize: 14,
                    }}
                    stroke={theme.palette.text.hint + "80"}
                    tickLine={false}
                  />
                  <XAxis dataKey="lesson_name" allowDataOverflow={false} />
                  <Tooltip
                    formatter={(value, name, props) => {
                      return [value, "Completed"];
                    }}
                  />
                  <Bar
                    dataKey="count_completed"
                    isAnimationActive={true}
                    background={true}
                  >
                    {ss2ChartData.data[ss2ChartData.selectedss2].progress.map(
                      (entry, index) => (
                        <Cell key={`cell-${index}`} fill={colors[index]} />
                      ),
                    )}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Widget>
          )}
        </Grid>
        {mock.bigStat.map(stat => (
          <Grid item md={4} sm={6} xs={12} key={stat.product}>
            <BigStat {...stat} />
          </Grid>
        ))}
        <Grid item xs={12}>
          <Widget
            title="Support Requests"
            upperTitle
            noBodyPadding
            bodyClass={classes.tableWidget}
          >
            <Table data={mock.table} />
          </Widget>
        </Grid>
      </Grid>
    </>
  );
}

// #######################################################################
function getRandomData(length, min, max, multiplier = 10, maxDiff = 10) {
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
