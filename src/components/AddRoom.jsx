import React, { useState } from "react";
import { Grid, Typography, TextField, Container, Paper, Button } from "@mui/material";
import { AddCircleOutlined } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";

const AddRoom = () => {
  const [name, setName] = useState("");

  const handleSubmit = () => {
    if (name === "") {
      Swal.fire({
        text: "Enter the room name!",
        icon: "error",
      });
    } else {
      const body = {
        name: name,
      };
      console.log(body);
      axios.post("https://mehakk.pythonanywhere.com/api/add-room/", body)
        .then(() => {
          Swal.fire({
            text: "Room added successfully!",
            icon: "success",
          });
          setName("");
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
    <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
      <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
        <center>
          <Typography variant="h6" gutterBottom>
            Room Details
          </Typography>
        </center>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              required
              id="name"
              name="name"
              label="Room Name"
              fullWidth
              variant="standard"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              color="primary"
              startIcon={<AddCircleOutlined />}
              variant="outlined"
              fullWidth
              onClick={handleSubmit}
            >
              Add Room
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AddRoom;