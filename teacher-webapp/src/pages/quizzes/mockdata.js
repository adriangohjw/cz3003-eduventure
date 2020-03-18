export default {
  columns: [
    { title: "ID", field: "id" },
    { title: "Name", field: "name" },
    { title: "Setter", field: "staff_id" },
    { title: "Fast Quiz", field: "is_fast" },
    { title: "Start Date", field: "date_start" },
    { title: "End Date", field: "date_end" },
  ],

  data: [
    {
      id: "001",
      staff_id: "Peter",
      name: "Quiz 1",
      is_fast: "true",
      date_start: "03/01/2020",
      date_end: "03/31/2020",
    },
    {
      id: "002",
      staff_id: "Peter",
      name: "Quiz 2",
      is_fast: "true",
      date_start: "04/01/2020",
      date_end: "04/31/2020",
    },
    {
      id: "003",
      staff_id: "Tom",
      name: "Quiz 3",
      is_fast: "true",
      date_start: "05/01/2020",
      date_end: "05/31/2020",
    },
  ],
};

// back up mockdata
// export default {
//   columns: [
//     { title: "Name", field: "name" },
//     { title: "Surname", field: "surname" },
//     { title: "Birth Year", field: "birthYear", type: "numeric" },
//     {
//       title: "Birth Place",
//       field: "birthCity",
//       lookup: { 34: "İstanbul", 63: "Şanlıurfa" },
//     },
//   ],
//   data: [
//     { name: "Mehmet", surname: "Baran", birthYear: 1987, birthCity: 63 },
//     {
//       name: "Zerya Betül",
//       surname: "Baran",
//       birthYear: 2017,
//       birthCity: 34,
//     },
//   ],
// };
