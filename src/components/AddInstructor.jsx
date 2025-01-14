import React, { useState } from "react";
import {
  Typography,
  Container,
  Paper,
  Grid,
  TextField,
  Chip,
  Button,
} from "@mui/material";
import { AddCircleOutlined } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";

const AddInstructor = () => {
  const [name, setName] = useState("");
  const [availableDays, setAvailableDays] = useState({
    monday: true,
    tuesday: true,
    wednesday: true,
    thursday: true,
    friday: true,
    saturday: true,
    sunday: false,
  });

  const handleDayToggle = (day) => {
    setAvailableDays((prevDays) => ({
      ...prevDays,
      [day]: !prevDays[day],
    }));
  };

  const handleSubmit = () => {
    if (name === "") {
      Swal.fire({
        text: "Enter the instructor's name!",
        icon: "error",
      });
      return;
    }

    const selectedDays = Object.keys(availableDays).filter(
      (day) => availableDays[day]
    );

    const body = {
      name: name,
      available_days: selectedDays,
    };

    console.log(body);

    axios.post("https://mehakk.pythonanywhere.com/api/add-instructor/", body)
      .then(() => {
        Swal.fire({
          text: "Instructor added successfully!",
          icon: "success",
        });
        setName("");
        setAvailableDays({
            monday: true,
            tuesday: true,
            wednesday: true,
            thursday: true,
            friday: true,
            saturday: true,
            sunday: false,
          });        
      })
      .catch((e) => {
        console.log(e);
        Swal.fire({
          title: "Error!",
          text: "Network Error",
          icon: "error",
        });
      });
  };

  return (
    <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
      <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
        <center>
          <Typography variant="h6" gutterBottom>
            Add Instructor
          </Typography>
        </center>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              required
              id="name"
              name="name"
              label="Instructor Name"
              fullWidth
              variant="standard"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Available Days
            </Typography>
            <Grid container spacing={1} justifyContent="center">
              {Object.keys(availableDays).map((day) => (
                <Grid item key={day}>
                  <Chip
                    label={day.charAt(0).toUpperCase() + day.slice(1)}
                    color="primary"
                    variant={availableDays[day] ? "default" : "outlined"}
                    onClick={() => handleDayToggle(day)}
                  />
                </Grid>
              ))}
            </Grid>
          </Grid>
          <Grid item xs={12}>
            <Button
              color="primary"
              startIcon={<AddCircleOutlined />}
              variant="outlined"
              fullWidth
              onClick={handleSubmit}
            >
              Add Instructor
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AddInstructor;