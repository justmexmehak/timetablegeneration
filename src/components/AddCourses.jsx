import React, { useState } from "react";
import { Grid, Typography, TextField, Container, Paper, Button } from "@mui/material";
import { AddCircleOutlined } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";

const AddCourses = () => {
  const [name, setName] = useState("");
  const [creditHours, setCreditHours] = useState(0);

  const handleSubmit = () => {
    if (name === "" || creditHours === 0) {
      Swal.fire({
        text: "Enter all values!",
        icon: "error",
      });
    } else {
      const body = {
        name: name,
        credit_hours: creditHours,
      };
      console.log(body);
      axios.post("https://mehakk.pythonanywhere.com/api/add-course/", body)
        .then(() => {
          Swal.fire({
            text: "Course registered successfully!",
            icon: "success",
          });
          setName("");
          setCreditHours(0);
        })
        .catch((e) => {
          console.log(e);
          Swal.fire({
            title: "Error!",
            text: "Network Error",
            icon: "error",
          });
        });
    }
  };

  return (
    <>
      <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
        <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
          <center>
            <Typography variant="h6" gutterBottom>
              Course Details
            </Typography>
          </center>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={12}>
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
            </Grid>
            <Grid item xs={12} sm={12}>
              <TextField
                required
                id="creditHours"
                name="creditHours"
                label="Credit Hours"
                type="number"
                fullWidth
                variant="standard"
                value={creditHours}
                onChange={(e) => setCreditHours(e.target.value)}
              />
            </Grid>
            <Grid item xs={12} sm={12}>
              <Button
                color="primary"
                startIcon={<AddCircleOutlined />}
                variant="outlined"
                fullWidth
                onClick={handleSubmit}
              >
                Add Course
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </>
  );
};

export default AddCourses;