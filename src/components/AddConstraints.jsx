import React, { useState, useEffect } from "react";
import {
  Typography,
  Container,
  Paper,
  Grid,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
} from "@mui/material";
import { AddCircleOutlined, RemoveCircleOutline } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";

const AddConstraints = () => {
  const [rooms, setRooms] = useState([]);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedRooms, setSelectedRooms] = useState([""]);

  useEffect(() => {
    // Fetch rooms and courses from the backend
    axios.get("https://mehakk.pythonanywhere.com/api/get-rooms/")
      .then((res) => setRooms(res.data))
      .catch((err) => console.error(err));

    axios.get("https://mehakk.pythonanywhere.com/api/get-courses/")
      .then((res) => setCourses(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleAddRoom = () => {
    setSelectedRooms([...selectedRooms, ""]);
  };

  const handleRemoveRoom = (index) => {
    const newSelectedRooms = selectedRooms.filter((_, i) => i !== index);
    setSelectedRooms(newSelectedRooms);
  };

  const handleRoomChange = (index, value) => {
    const newSelectedRooms = selectedRooms.map((room, i) => (
      i === index ? value : room
    ));
    setSelectedRooms(newSelectedRooms);
  };

  const handleSubmit = () => {
    if (selectedCourse === "" || selectedRooms.some(room => room === "")) {
      Swal.fire({
        text: "Select both course and all room options!",
        icon: "error",
      });
      return;
    }

    const body = {
      course: selectedCourse,
      rooms: selectedRooms,
    };

    console.log(body);

    axios.post("https://mehakk.pythonanywhere.com/api/add-constraint/", body)
      .then(() => {
        Swal.fire({
          text: "Constraint added successfully!",
          icon: "success",
        });
        setSelectedCourse("");
        setSelectedRooms([""]);
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
            Add Constraints
          </Typography>
        </center>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <FormControl fullWidth variant="standard">
              <InputLabel id="course-label">Course</InputLabel>
              <Select
                labelId="course-label"
                id="course"
                value={selectedCourse}
                onChange={(e) => setSelectedCourse(e.target.value)}
              >
                {courses.map((course) => (
                  <MenuItem key={course.id} value={course.id}>
                    {course.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          {selectedRooms.map((room, index) => (
            <Grid item xs={12} key={index}>
              <FormControl fullWidth variant="standard">
                <InputLabel id={`room-label-${index}`}>Room</InputLabel>
                <Select
                  labelId={`room-label-${index}`}
                  id={`room-${index}`}
                  value={room}
                  onChange={(e) => handleRoomChange(index, e.target.value)}
                >
                  {rooms.map((room) => (
                    <MenuItem key={room.id} value={room.id}>
                      {room.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              {index > 0 && (
                <IconButton onClick={() => handleRemoveRoom(index)}>
                  <RemoveCircleOutline />
                </IconButton>
              )}
            </Grid>
          ))}
          <Grid item xs={12}>
            <Button
              color="primary"
              startIcon={<AddCircleOutlined />}
              variant="outlined"
              fullWidth
              onClick={handleAddRoom}
            >
              Add Room Option
            </Button>
          </Grid>
          <Grid item xs={12}>
            <Button
              color="primary"
              variant="contained"
              fullWidth
              onClick={handleSubmit}
            >
              Add Room Constraint
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AddConstraints;