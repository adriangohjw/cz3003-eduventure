# Teacher's Portal Webapp

Built with [React](https://facebook.github.io/react/), [Material-UI](https://material-ui.com), [React Router](https://reacttraining.com/react-router/).

**This version uses React 16.8.6, React Router v5, MaterialUI v4, built with React Hooks and React Context (No Redux)**

## Pages

- Dashboard
- Leaderboard
- Syllabus
- Question Bank
- Quizzes

## Quick Start

#### 1. Clone this repo and start up the database as per the instructions on the main README

#### 2. CD into the teacher-webapp folder and run `yarn install` from command prompt

This will install both run-time project dependencies and developer tools listed
in [package.json](package.json) file.

#### 3. Run `yarn start`

Runs the app in the development mode.

Open http://localhost:3000 to view it in the browser. Whenever you modify any of the source files inside the `/src` folder,
the module bundler ([Webpack](http://webpack.github.io/)) will recompile the
app on the fly and refresh all the connected browsers.

#### 4. Run `yarn build`

Builds the app for production to the build folder.
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.
Your app is ready to be deployed!

## Logging In
You can create a new account or utilize the data from the test db. Take note that the test db is started with ```python run_test.py``` instead of ```python run.py```.

You can use this sample account (case-sensitive):

Username: leeJohn@ntu.edu.sg  
Password: password_1

## References:
React Material Admin — (Material-UI Dashboard Template): https://github.com/flatlogic/react-material-admin  
Material UI Library: https://github.com/mui-org/material-ui  
Material Table: https://github.com/mbrn/material-table  
RECharts: https://recharts.org/en-US/api
