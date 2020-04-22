import React, { useState, useEffect } from "react";
import {
  Grid,
  Select,
  OutlinedInput,
  MenuItem,
  CircularProgress,
} from "@material-ui/core";
import { useTheme } from "@material-ui/styles";
import {
  ResponsiveContainer,
  CartesianGrid,
  BarChart,
  LineChart,
  Line,
  Cell,
  YAxis,
  XAxis,
  Bar,
  Tooltip,
} from "recharts";

// styles
import useStyles from "./styles";

// components
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";

import { url } from "../../context/UserContext";

const colors = [
  "#DD7173",
  "#DD758D",
  "#D47DA6",
  "#C389BB",
  "#A996CC",
  "#89A3D5",
  "#65AFD5",
  "#3FB9CD",
  "#26C0BD",
  "#34C6A8",
  "#56C98F",
  "#79CA77",
  "#9CC961",
  "#BFC651",
  "#E0C04C",
  "#000000",
];

export default function Dashboard(props) {
  var classes = useStyles();
  var theme = useTheme();

  // manage data for first chart
  var [ss1ChartData, setss1ChartData] = useState({
    isLoading: true, //whether data has been successfully retrieved
    selectedss1: 0, //index of option selected from dropdown menu
    options: [
      //options available in dropdown menu
      { value: "avg_score", label: "Average Score" },
      { value: "max_score", label: "Highest Score" },
      { value: "min_score", label: "Lowest Score" },
      { value: "stdev", label: "Standard Deviation" },
      { value: "25th_percentile", label: "25th Percentile" },
      { value: "75th_percentile", label: "75th Percentile" },
      { value: "95th_percentile", label: "95th Percentile" },
    ],
    courses: [], //course group names
    data: [], //data points of chart
  });
  //manage data for second chart
  var [ss2ChartData, setss2ChartData] = useState({
    isLoading: true,
    selectedss2: 0,
    options: [],
    data: [],
  });
  var [ss7ChartData, setss7ChartData] = useState({
    isLoading: true,
    selectedss7: 0,
    options: [],
    data: [],
  });
  const getss1ChartData = () => {
    fetch(url + `statistics/stat`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setss1ChartData({
            ...ss1ChartData,
            isLoading: false,
          });
          throw new Error(res.error);
        }
      })
      .then(response => {
        const [formattedData, courses] = formatss1Data(response); //response data is different from format needed
        setss1ChartData({
          ...ss1ChartData,
          data: formattedData,
          isLoading: false,
          courses: courses,
        });
      })
      .catch(error => console.log(error));
  };

  const formatss1Data = data => {
    const courses = [];
    const quiz_names = [];
    data.stats.map(course => {
      courses.push(course.course_index); //gets list of all course_index
    });

    data.stats[0].quizzes.map(quiz => {
      quiz_names.push(quiz.name); //gets list of all quiz_names
    });

    ss1ChartData.options.map(option => {
      data[option.value] = [];
    }); //sets empty object for each stat

    ss1ChartData.options.map(option => {
      quiz_names.map(q => {
        var _stat = {};
        _stat["name"] = q;

        courses.map(c => {
          _stat[c] = data.stats
            .find(course => {
              return course.course_index == c;
            })
            .quizzes.find(quiz => {
              return quiz.name == q;
            })[option.value];
        });

        data[option.value].push(_stat);
      });
    });
    delete data.stats; //deletes the stats attribute in the object because we have already converted it
    return [data, courses];
  };

  const getss2ChartData = () => {
    fetch(url + `statistics/lesson_completed`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setss2ChartData({
            ...ss2ChartData,
            isLoading: false,
          });
          throw new Error(res.error);
        }
      })
      .then(response => {
        const [formattedData, options] = formatss2Data(response.courses);
        setss2ChartData({
          ...ss2ChartData,
          data: formattedData,
          options: options,
          isLoading: false,
        });
      })
      .catch(error => console.log(error));
  };

  const formatss2Data = data => {
    //flattening the response array
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

  const getss7ChartData = () => {
    fetch(url + `statistics/course_score`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          setss7ChartData({
            ...ss7ChartData,
            isLoading: false,
          });
          throw new Error(res.error);
        }
      })
      .then(response => {
        const [formattedData, options] = formatss7Data(response.courses);
        setss7ChartData({
          ...ss7ChartData,
          data: formattedData,
          options: options,
          isLoading: false,
        });
      })
      .catch(error => console.log(error));
  };

  const formatss7Data = data => {
    //slightly changing the object structure so that key and values both become their own attributes
    const courses = [];
    data.map(c => {
      courses.push(c.course_index);
      const _scores = [];
      Object.entries(c.scores).forEach(([key, value]) => {
        _scores.push({ name: key, count: value });
      });
      c.scores = _scores;
    });
    return [data, courses];
  };

  const CustomizedAxisTick = props => {
    //create rotated x-axis ticks
    const { x, y, stroke, payload } = props;

    return (
      <g transform={`translate(${x},${y})`}>
        <text
          x={0}
          y={0}
          dy={16}
          textAnchor="end"
          fill="#666"
          transform="rotate(-35)"
        >
          {payload.value}
        </text>
      </g>
    );
  };

  useEffect(() => {
    getss1ChartData();
    getss2ChartData();
    getss7ChartData();
  }, []);

  return (
    <>
      <PageTitle title="Dashboard" />
      <Grid item xs={12}>
        {ss1ChartData.isLoading == true ? (
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
                  Quiz Statistics
                </Typography>
                <div className={classes.mainChartHeaderLabel}>
                  <Typography className={classes.mainChartLegentElement}>
                    Statistic:{" "}
                    {ss1ChartData.options[ss1ChartData.selectedss1].label}
                  </Typography>
                </div>
                <Select
                  value={ss1ChartData.selectedss1}
                  onChange={e => {
                    setss1ChartData({
                      ...ss1ChartData,
                      selectedss1: e.target.value,
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
                  {ss1ChartData.options.map((option, index) => {
                    return (
                      <MenuItem value={index} key={index}>
                        {option.label}
                      </MenuItem>
                    );
                  })}
                </Select>
              </div>
            }
          >
            <ResponsiveContainer width="100%" minWidth={500} height={350}>
              <LineChart
                margin={{ top: 10, right: 5, left: 5, bottom: 5 }}
                data={
                  ss1ChartData.data[
                    ss1ChartData.options[ss1ChartData.selectedss1].value
                  ]
                }
              >
                <Tooltip />
                <CartesianGrid strokeDasharray="3 3" />
                <YAxis
                  tick={{
                    fill: theme.palette.text.hint + "140",
                    fontSize: 14,
                  }}
                  padding={{ top: 40 }}
                  stroke={theme.palette.text.hint + "140"}
                  tickLine={false}
                />

                <XAxis
                  tick={{
                    fill: theme.palette.text.hint + "140",
                    fontSize: 14,
                  }}
                  stroke={theme.palette.text.hint + "140"}
                  tickLine={false}
                  dataKey="name"
                />
                {ss1ChartData.courses.map((course, index) => {
                  const _index = (
                    ((colors.length - 1) / ss1ChartData.courses.length) *
                    index
                  ).toFixed(0);
                  return (
                    <Line
                      key={index}
                      type="monotone"
                      dataKey={course}
                      stroke={colors[_index]}
                      strokeWidth={3}
                      dot={true}
                      activeDot={{ r: 8 }}
                    />
                  );
                })}
              </LineChart>
            </ResponsiveContainer>
          </Widget>
        )}
      </Grid>
      <Grid item xs={12}>
        {ss2ChartData.isLoading == true ? (
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
                  Completed Lessons by Course Group
                </Typography>
                <div className={classes.mainChartHeaderLabels}>
                  <div className={classes.mainChartHeaderLabel}>
                    <Typography className={classes.mainChartLegentElement}>
                      Course Group:{" "}
                      {ss2ChartData.options[ss2ChartData.selectedss2]}
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
                  {ss2ChartData.options.map((option, index) => {
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
                data={ss2ChartData.data[ss2ChartData.selectedss2].progress}
              >
                <YAxis
                  tick={{
                    fill: theme.palette.text.hint + "140",
                    fontSize: 14,
                  }}
                  padding={{ top: 40 }}
                  stroke={theme.palette.text.hint + "140"}
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
      <Grid item xs={12}>
        {ss7ChartData.isLoading == true ? (
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
                  Overall Course Score by Course
                </Typography>
                <div className={classes.mainChartHeaderLabels}>
                  <div className={classes.mainChartHeaderLabel}>
                    <Typography className={classes.mainChartLegentElement}>
                      Course Group:{" "}
                      {ss7ChartData.options[ss7ChartData.selectedss7]}
                    </Typography>
                  </div>
                </div>
                <Select
                  value={ss7ChartData.selectedss7}
                  onChange={e => {
                    setss7ChartData({
                      ...ss7ChartData,
                      selectedss7: e.target.value,
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
                  {ss7ChartData.options.map((option, index) => {
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
                margin={{ top: 10, right: 5, left: 5, bottom: 40 }}
                data={ss7ChartData.data[ss7ChartData.selectedss7].scores}
              >
                <defs>
                  <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis
                  dataKey="name"
                  tick={CustomizedAxisTick}
                  label={{
                    value: "Score (100%)",
                    position: "insideBottom",
                    offset: -30,
                  }}
                />
                <YAxis
                  label={{
                    value: "Number of Students",
                    angle: -90,
                    position: "insideLeft",
                  }}
                />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip
                  formatter={(value, name, props) => {
                    return [value, "Number of Students"];
                  }}
                />
                <Bar
                  type="monotone"
                  dataKey="count"
                  stroke="#8884d8"
                  fillOpacity={1}
                  fill="url(#colorUv)"
                />
              </BarChart>
            </ResponsiveContainer>
          </Widget>
        )}
      </Grid>
    </>
  );
}
