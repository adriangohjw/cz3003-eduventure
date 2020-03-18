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

const states = {
  sent: "success",
  pending: "warning",
  declined: "secondary",
};

export default function TableComponent({ data }) {
  var keys = Object.keys(data[0]).map(i => i.toUpperCase());
  keys.shift(); // delete "id" key

  return (
    <Table className="mb-0">
      <TableHead>
        <TableRow>
          {keys.map(key => (
            <TableCell key={key}>
              {key}
              <TableSortLabel direction={"asc"}></TableSortLabel>
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {data.map(({ studentID, name, email, course, score }) => (
          <TableRow key={studentID}>
            <TableCell className="pl-3 fw-normal">{name}</TableCell>
            <TableCell>{email}</TableCell>
            <TableCell>{course}</TableCell>
            <TableCell>{score}</TableCell>
          </TableRow>
        ))}
        {/* {data.map(({ id, name, email, product, price, date, city, status }) => (
          <TableRow key={id}>
            <TableCell className="pl-3 fw-normal">{name}</TableCell>
            <TableCell>{email}</TableCell>
            <TableCell>{product}</TableCell>
            <TableCell>{price}</TableCell>
            <TableCell>{date}</TableCell>
            <TableCell>{city}</TableCell>
            <TableCell>
              <Button
                color={states[status.toLowerCase()]}
                size="small"
                className="px-2"
                variant="contained"
              >
                {status}
              </Button>
            </TableCell>
          </TableRow>
        ))} */}
      </TableBody>
    </Table>
  );
}
