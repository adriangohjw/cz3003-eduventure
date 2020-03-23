export default {
  profile: { id: "001", name: "Peter" },

  columns: [
    { title: "ID", field: "id" },
    { title: "Name", field: "name" },
    { title: "Setter", field: "staff_id" },
    { title: "Fast Quiz", field: "is_fast" },
    { title: "Attempts", field: "attempts" },
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
