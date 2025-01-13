import React, { useState } from "react";
import {
  Grid2,
  Typography,
  TextField,
  Container,
  Paper,
  Button,
} from "@mui/material";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { AddCircleOutlined } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";

const AddCourses = () => {
    const [name, setName] = useState("");
    const [lecturesno, setLecturesNo] = useState(0);
    const [duration, setDuration] = useState(0);
    const [iname, setIName] = useState("");
    const [startHour, setStartHour] = useState(new Date());
    const [endHour, setEndHour] = useState(new Date());
    const handleStart = (newValue) => {
      setStartHour(newValue);
    };
    const handleEnd = (newValue) => {
      setEndHour(newValue);
    };
  
    const handleSubmit = () => {
      if (name === "" || lecturesno === 0 || duration === 0 || iname === "") {
        Swal.fire({
          text: "Enter all values!",
          icon: "error",
        });
      } else {
        var body = {
          name: name,
          lectureno: lecturesno,
          duration: duration,
          instructor_name: iname,
          start_hr: startHour.getHours(),
          end_hr: endHour.getHours(),
        };
        // Swal.fire({
        //     text: "Course registered successfully!",
        //     icon: "success",
        // });
        console.log(body);
        axios.post("https://mehakk.pythonanywhere.com/api/add-course/", body)
        // axios.get('http://localhost:8000/api/test-endpoint/')
        // axios.get('https://mehakk.pythonanywhere.com/api/test-endpoint/')
          .then(() => {
            Swal.fire({
              text: "Course registered successfully!",
              icon: "success",
            });
            setName("");
            setDuration(0);
            setLecturesNo(0);
            setIName("");
            setStartHour(new Date());
            setEndHour(new Date());
          })
          .catch((e) => console.log(e));
      }
    };
  
    return (
      <>
        <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
          <Paper
            variant="outlined"
            sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
          >
            <center>
              <Typography variant="h6" gutterBottom>
                Course Details
              </Typography>
            </center>
            <Grid2 container spacing={3}>
              <Grid2 item xs={12} sm={12}>
                <TextField
                  required
                  id="name"
                  name="name"
                  label="Name of Course"
                  fullWidth
                  variant="standard"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </Grid2>
              <Grid2 item xs={12} sm={6}>
                <TextField
                  required
                  id="lecturesno"
                  name="lecturesno"
                  label="Number of Lectures"
                  type="number"
                  fullWidth
                  variant="standard"
                  helperText="per week"
                  value={lecturesno}
                  onChange={(e) => setLecturesNo(e.target.value)}
                />
              </Grid2>
              <Grid2 item xs={12} sm={6}>
                <TextField
                  required
                  id="duration"
                  name="duration"
                  label="Duration of Lecture"
                  type="number"
                  fullWidth
                  variant="standard"
                  helperText="in hours"
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                />
              </Grid2>
              <Grid2 item xs={12} sm={12}>
                <TextField
                  required
                  id="iname"
                  name="iname"
                  label="Name of Instructor"
                  type="text"
                  fullWidth
                  variant="standard"
                  value={iname}
                  onChange={(e) => setIName(e.target.value)}
                />
              </Grid2>
              <Grid2 item xs={12} sm={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <TimePicker
                    label="Instructor Start Hour"
                    value={startHour}
                    onChange={handleStart}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        helperText="Instructor Working Hours"
                      />
                    )}
                  />
                </LocalizationProvider>
              </Grid2>
              <Grid2 item xs={12} sm={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <TimePicker
                    label="Instructor End Hour"
                    value={endHour}
                    onChange={handleEnd}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        helperText="Instructor Working Hours"
                      />
                    )}
                  />
                </LocalizationProvider>
              </Grid2>
              <Grid2 item xs={12} sm={12}>
                <Button
                  color="primary"
                  startIcon={<AddCircleOutlined />}
                  variant="outlined"
                  fullWidth
                  onClick={handleSubmit}
                >
                  Add Course
                </Button>
              </Grid2>
            </Grid2>
          </Paper>
        </Container>
      </>
    );
  };
  
  export default AddCourses;