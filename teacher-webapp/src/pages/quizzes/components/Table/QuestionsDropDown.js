import React from "react";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import CircularProgress from "@material-ui/core/CircularProgress";

import { url } from "../../../../context/UserContext";

export default function QuestionsDropDown(handleOnChange) {
  const [open, setOpen] = React.useState(false);
  const [questions, setQuestions] = React.useState([]);
  const loading = open && questions.length === 0;

  React.useEffect(() => {
    let active = true;

    if (!loading) {
      return undefined;
    }
    fetch(url + `questions/all`, {
      method: "GET",
    })
      .then(res => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("No Questions Found");
        }
      })
      .then(response => {
        setQuestions(response.questions);
        active = false;
      })
      .catch(error => console.log(error));
  }, [loading]);

  React.useEffect(() => {
    if (!open) {
      setQuestions([]);
    }
  }, [open]);

  return (
    <Autocomplete
      id="questions-drop-down"
      style={{ width: 300 }}
      open={open}
      onOpen={() => {
        setOpen(true);
      }}
      onClose={(event, reason) => {
        setOpen(false);
      }}
      getOptionSelected={(option, value) =>
        option.description === value.description
      }
      onChange={handleOnChange}
      getOptionLabel={option => option.description}
      options={questions}
      loading={loading}
      renderInput={params => (
        <TextField
          {...params}
          label="Select Question"
          variant="outlined"
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <React.Fragment>
                {loading ? (
                  <CircularProgress color="inherit" size={20} />
                ) : null}
                {params.InputProps.endAdornment}
              </React.Fragment>
            ),
          }}
        />
      )}
    />
  );
}
