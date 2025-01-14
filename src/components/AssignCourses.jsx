import React, { useState, useEffect } from "react";
import { Grid, Typography, TextField, Container, Paper, Button, IconButton, MenuItem, Select, FormControl, InputLabel } from "@mui/material";
import { AddCircleOutlined, RemoveCircleOutline } from "@mui/icons-material";
import Swal from "sweetalert2";
import axios from "axios";

const AssignCourses = () => {
  const [sectionName, setSectionName] = useState("");
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [assignments, setAssignments] = useState([{ course: "", instructor: "" }]);

  useEffect(() => {
    // Fetch courses and instructors from the backend
    axios.get("https://mehakk.pythonanywhere.com/api/get-courses/")
      .then((res) => setCourses(res.data))
      .catch((err) => console.error(err));

    axios.get("https://mehakk.pythonanywhere.com/api/get-instructors/")
      .then((res) => setInstructors(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleAddAssignment = () => {
    setAssignments([...assignments, { course: "", instructor: "" }]);
  };

  const handleRemoveAssignment = (index) => {
    const newAssignments = assignments.filter((_, i) => i !== index);
    setAssignments(newAssignments);
  };

  const handleAssignmentChange = (index, field, value) => {
    const newAssignments = assignments.map((assignment, i) => (
      i === index ? { ...assignment, [field]: value } : assignment
    ));
    setAssignments(newAssignments);
  };

  const handleSubmit = () => {
    if (sectionName === "" || assignments.some(a => a.course === "" || a.instructor === "")) {
      Swal.fire({
        text: "Enter all values!",
        icon: "error",
      });
      return;
    }

    const body = {
      section_name: sectionName,
      assignments: assignments,
    };

    console.log(body);

    axios.post("https://mehakk.pythonanywhere.com/api/assign-courses/", body)
      .then(() => {
        Swal.fire({
          text: "Courses assigned successfully!",
          icon: "success",
        });
        setSectionName("");
        setAssignments([{ course: "", instructor: "" }]);
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
            Assign Courses to Section
          </Typography>
        </center>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              required
              id="sectionName"
              name="sectionName"
              label="Section Name"
              fullWidth
              variant="standard"
              value={sectionName}
              onChange={(e) => setSectionName(e.target.value)}
            />
          </Grid>
          {assignments.map((assignment, index) => (
            <React.Fragment key={index}>
              <Grid item xs={5}>
                <FormControl fullWidth variant="standard">
                  <InputLabel id={`course-label-${index}`}>Course</InputLabel>
                  <Select
                    labelId={`course-label-${index}`}
                    id={`course-${index}`}
                    value={assignment.course}
                    onChange={(e) => handleAssignmentChange(index, "course", e.target.value)}
                  >
                    {courses.map((course) => (
                      <MenuItem key={course.id} value={course.id}>
                        {course.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={5}>
                <FormControl fullWidth variant="standard">
                  <InputLabel id={`instructor-label-${index}`}>Instructor</InputLabel>
                  <Select
                    labelId={`instructor-label-${index}`}
                    id={`instructor-${index}`}
                    value={assignment.instructor}
                    onChange={(e) => handleAssignmentChange(index, "instructor", e.target.value)}
                  >
                    {instructors.map((instructor) => (
                      <MenuItem key={instructor.id} value={instructor.id}>
                        {instructor.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={2} container alignItems="center">
                <IconButton onClick={() => handleRemoveAssignment(index)}>
                  <RemoveCircleOutline />
                </IconButton>
              </Grid>
            </React.Fragment>
          ))}
          <Grid item xs={12}>
            <Button
              color="primary"
              startIcon={<AddCircleOutlined />}
              variant="outlined"
              fullWidth
              onClick={handleAddAssignment}
            >
              Add Course
            </Button>
          </Grid>
          <Grid item xs={12}>
            <Button
              color="primary"
              variant="contained"
              fullWidth
              onClick={handleSubmit}
            >
              Assign Courses
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AssignCourses;