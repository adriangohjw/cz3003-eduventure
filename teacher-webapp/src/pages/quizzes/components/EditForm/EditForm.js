import React from "react";
import { withStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Slide from "@material-ui/core/Slide";
import Container from "@material-ui/core/Container";

import useStyles from "../../styles";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function EditForm({ profile }) {
  const [open, setOpen] = React.useState(false);
  const [state, setState] = React.useState({});
  // const [selectedDate, setSelectedDate] = React.useState(new Date('2014-08-18T21:11:54'));
  var classes = useStyles();

  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleSelectChange = event => {
    const name = event.target.name;
    setState(
      {
        ...state,
        [name]: event.target.value,
      },
      console.log(name, event.target.value),
    );
  };
  return (
    <div>
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
      >
        <AppBar className={classes.appBar}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              New Quiz
            </Typography>
            <Button autoFocus color="inherit" onClick={handleClose}>
              Submit
            </Button>
          </Toolbar>
        </AppBar>
        <Container maxWidth="md">
          <form
            className={classes.textfields_root}
            noValidate
            autoComplete="off"
          >
            <div>
              <TextField
                disabled
                variant="filled"
                id="setter-id"
                label="ID"
                defaultValue={profile.id}
              />
              <TextField
                disabled
                variant="filled"
                id="setter-name"
                label="Setter Name"
                defaultValue={profile.name}
              />
            </div>
            <div>
              <TextField required id="quiz-name" label="Quiz Name" />
            </div>
            <div>
              <FormControl required className={classes.formControl}>
                <InputLabel id="demo-simple-select-required-label">
                  Quiz Type
                </InputLabel>
                <Select
                  labelId="isFast-simple-select-required-label"
                  id="isFast-simple-select-required"
                  name="isFast"
                  defaultValue={false}
                  value={state.isFast}
                  onChange={handleSelectChange}
                  className={classes.selectEmpty}
                >
                  <MenuItem value={true}>Fast</MenuItem>
                  <MenuItem value={false}>Normal</MenuItem>
                </Select>
                <FormHelperText>Required</FormHelperText>
              </FormControl>
            </div>
            <div>
              <TextField
                id="datetime_end"
                name="date_start"
                label="Start Date"
                type="datetime-local"
                defaultValue="2020-03-24T10:30"
                className={classes.textField}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </div>
            <div>
              <TextField
                id="datetime_start"
                name="date_end"
                label="End Date"
                type="datetime-local"
                defaultValue="2020-03-25T10:30"
                className={classes.textField}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </div>
          </form>
        </Container>
      </Dialog>
    </div>
  );
}
