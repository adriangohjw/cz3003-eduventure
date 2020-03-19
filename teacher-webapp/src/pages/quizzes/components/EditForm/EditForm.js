import React from "react";
import { withStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import AddCircleIcon from "@material-ui/icons/AddCircle";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Slide from "@material-ui/core/Slide";
import Container from "@material-ui/core/Container";

import useStyles from "../../styles";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function EditForm(props) {
  const [open, setOpen] = React.useState(false);
  const [state, setState] = React.useState({});
  var classes = useStyles();

  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleSelectChange = event => {
    const name = event.target.name;
    setState({
      ...state,
      [name]: event.target.value,
    });
  };
  return (
    <div>
      <Button variant="contained" color="primary" onClick={handleClickOpen}>
        {<AddCircleIcon />}
        &nbsp; Add New Quiz
      </Button>
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
                defaultValue={props.profile.id}
              />
              <TextField
                disabled
                variant="filled"
                id="setter-name"
                label="Setter Name"
                defaultValue={props.profile.name}
              />
            </div>
            <div>
              <TextField required id="quiz-name" label="Quiz Name" />
            </div>
            <div>
              <FormControl className={classes.formControl}>
                <InputLabel htmlFor="age-native-simple">Fast Quiz?</InputLabel>
                <Select
                  value={state.is_fast}
                  onChange={handleSelectChange}
                  inputProps={{
                    name: "Fast Quiz",
                    id: "age-native-required",
                  }}
                >
                  <option aria-label="None" value="" />
                  <option value={true}>Fast</option>
                  <option value={false}>Normal</option>
                </Select>
              </FormControl>
            </div>
          </form>
        </Container>
      </Dialog>
    </div>
  );
}
