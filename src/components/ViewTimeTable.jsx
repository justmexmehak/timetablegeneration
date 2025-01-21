import axios from "axios";
import React, { useState } from "react";
import { Button, CircularProgress, Typography, Paper } from "@mui/material";

const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const slots = Array.from({ length: 9 }, (_, i) => i + 1); // 9 slots

const slotToTime = (slot) => {
  const startHour = 8 + slot - 1; // Assuming the first slot starts at 9 AM
  return `${startHour}:30 - ${startHour + 1}:30`; // Example time range
};

const ViewTimeTable = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [clicked, setClicked] = useState(false);

  const getTimeTable = () => {
    setClicked(true);
    axios
      .get("https://mehakk.pythonanywhere.com/api/generate-timetable/")
      .then((res) => {
        const temp = {};
        for (const [key, value] of Object.entries(res.data)) {
          let internal_tmp = value.map((elem) => ({
            ...elem,
            // day: daysOfWeek[Math.floor((elem.startSlot - 1) / slots.length)],
            time: slotToTime(elem.startSlot),
          }));
          temp[key] = internal_tmp;
        }
        setData(temp);
        setLoading(false);
      })
      .catch((e) => console.log(e));
  };

  return (
    <div>
      <Button variant="contained" color="primary" onClick={getTimeTable}>
        Generate Timetable
      </Button>
      {loading && clicked ? (
        <CircularProgress />
      ) : (
        Object.keys(data).map((section) => (
          <div key={section}>
            <Typography variant="h6" gutterBottom>
              {section}
            </Typography>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <div style={{ display: "flex" }}>
                <div style={{ flex: "1", border: "2px solid #363636", padding: "10px" }}>
                  <Typography variant="subtitle1">Time</Typography>
                </div>
                {daysOfWeek.map((day) => (
                  <div key={day} style={{ flex: "1", border: "2px solid #363636", padding: "10px" }}>
                    <Typography variant="subtitle1">{day}</Typography>
                  </div>
                ))}
              </div>
              {slots.map((slot) => (
                <div key={slot} style={{ display: "flex" }}>
                  <div style={{ flex: "1", border: "2px solid #363636", padding: "10px" }}>
                    <Typography variant="body2">{slotToTime(slot)}</Typography>
                  </div>
                  {daysOfWeek.map((day) => {
                    const event = data[section].find(
                      (e) => e.day === day && e.startSlot <= slot && slot < e.startSlot + e.duration
                    );
                    return (
                      <div key={day} style={{ flex: "1", border: "2px solid #363636", padding: "10px" }}>
                        <Paper
                          style={{
                            padding: "10px",
                            backgroundColor: event ? "#007958" : "#fff",
                          }}
                        >
                          {event ? (
                            <>
                              <Typography variant="body2" style={{ fontWeight: "bold", color: "#fbfaf5" }}>{event.name}</Typography>
                              <Typography variant="caption" style={{ fontSize: "10px", display: "block", color: "#fbfaf5" }}>{event.room}</Typography>
                              <Typography variant="caption" style={{ fontSize: "10px", display: "block", color: "#fbfaf5" }}>{event.instructor}</Typography>
                            </>
                          ) : (
                            // <Typography variant="body2">Free</Typography>
                            <></>
                          )}
                        </Paper>
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default ViewTimeTable;