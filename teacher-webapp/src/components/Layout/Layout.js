import React, { useState, useEffect } from "react";
import { Route, Switch, Redirect, withRouter } from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

// components
import Header from "../Header";
import Sidebar from "../Sidebar";

// pages
import Dashboard from "../../pages/dashboard";
import Charts from "../../pages/charts";
import Quizzes from "../../pages/quizzes";
import Leaderboards from "../../pages/leaderboards";
import Syllabus from "../../pages/syllabus";
// import QuestionBank from "../../pages/questionbank";
// context
import { useLayoutState } from "../../context/LayoutContext";

function Layout(props) {
  var classes = useStyles();
  // global
  var layoutState = useLayoutState();
  return (
    <div className={classes.root}>
      <>
        <Header history={props.history} />
        <Sidebar />
        <div
          className={classnames(classes.content, {
            [classes.contentShift]: layoutState.isSidebarOpened,
          })}
        >
          <div className={classes.fakeToolbar} />
          <Switch>
            <Route path="/app/dashboard" component={Dashboard} />
            <Route path="/app/leaderboards" component={Leaderboards} />
            <Route path="/app/quizzes" component={Quizzes} />
            {/* <Route path="/app/questionbank" component={QuestionBank} /> */}
            <Route path="/app/syllabus" component={Syllabus} />
          </Switch>
        </div>
      </>
    </div>
  );
}

export default withRouter(Layout);
