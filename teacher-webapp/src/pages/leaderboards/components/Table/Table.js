import React from "react";
import {
  Table,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@material-ui/core";

// components
import { Button } from "../../../../components/Wrappers";
import { TableSortLabel } from "@material-ui/core";
import { getThemeProps } from "@material-ui/styles";

const states = {
  sent: "success",
  pending: "warning",
  declined: "secondary",
};

export default function TableComponent(props) {
  /* var keys = Object.keys(props.data[0]).map(i => i.toUpperCase());
  keys.shift(); // delete "id" key for old dummy data */
  var keys = ["Student ID", "Name", "Email", "Score"];
  //var keys = ["STUDENT_ID", "NAME","EMAIL", "SCORE"];
  console.log("keys: ", keys);
  return (
    <Table className="mb-0">
      <TableHead>
        <TableRow>
          {keys.map(key => (
            <TableCell key={key}>
              {key}
              <TableSortLabel
                onClick={() => props.sortBy(key)}
              ></TableSortLabel>
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {/* {props.data.map(({ id, studentID, name, email, course, score }) => (
          <TableRow key={id}>
            <TableCell>{studentID}</TableCell>
            <TableCell className="pl-3 fw-normal">{name}</TableCell>
            <TableCell>{email}</TableCell>
            <TableCell>{course}</TableCell>
            <TableCell>{score}</TableCell>
          </TableRow>
        ))} */}
        {props.data.map(({ email, id, name, score }) => (
          <TableRow key={id}>
            <TableCell>{id}</TableCell>
            <TableCell>{name}</TableCell>
            <TableCell>{email}</TableCell>
            <TableCell className="pl-3 fw-normal">{score}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
