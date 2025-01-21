import axios from "axios";
import React, { useState } from "react";
import { 
  Button, 
  CircularProgress, 
  Typography, 
  Paper,
  Container,
  Box,
  Divider,
  Alert
} from "@mui/material";
import { Download, Refresh } from '@mui/icons-material';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const slots = Array.from({ length: 9 }, (_, i) => i + 1);

const slotToTime = (slot) => {
  const startHour = 8 + slot - 1;
  return `${startHour}:30 - ${startHour + 1}:30`;
};

const ViewTimeTable = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [clicked, setClicked] = useState(false);

  const getTimeTable = () => {
    console.log("Fetching timetable...");
    setClicked(true);
    setLoading(true);
    setError(null);

    axios
      .get("https://mehakk.pythonanywhere.com/api/generate-timetable/")
      .then((res) => {
        console.log("Response received:", res.data);
        const temp = {};
        for (const [key, value] of Object.entries(res.data)) {
          let internal_tmp = value.map((elem) => ({
            ...elem,
            time: slotToTime(elem.startSlot),
          }));
          temp[key] = internal_tmp;
        }
        setData(temp);
        setLoading(false);
      })
      .catch((e) => {
        console.error("Error fetching timetable:", e);
        setError("Failed to fetch timetable. Please try again.");
        setLoading(false);
      });
  };

  const downloadTimetable = () => {
    try {
      setLoading(true);
      const pdf = new jsPDF('l', 'mm', 'a4');
      
      Object.entries(data).forEach(([section, classes], sectionIndex) => {
        if (sectionIndex > 0) {
          pdf.addPage();
        }

        // Add section header
        pdf.setFontSize(16);
        pdf.text(`Section ${section} Timetable`, 15, 15);
        pdf.setFontSize(12);

        // Prepare table data
        const tableData = [];
        const tableColumns = [
          { header: 'Time', dataKey: 'time' },
          ...daysOfWeek.map(day => ({ header: day, dataKey: day }))
        ];

        // Create time slots array
        slots.forEach(slot => {
          const row = {
            time: slotToTime(slot)
          };

          daysOfWeek.forEach(day => {
            const event = classes.find(
              c => c.day === day && c.startSlot <= slot && slot < c.startSlot + c.duration
            );

            if (event && event.startSlot === slot) {
              row[day] = `${event.name}\n${event.room}\n${event.instructor}`;
            } else if (event && slot > event.startSlot && slot < event.startSlot + event.duration) {
              row[day] = '↑ Continued';
            } else {
              row[day] = '';
            }
          });

          tableData.push(row);
        });

        // Generate table
        pdf.autoTable({
          startY: 25,
          head: [tableColumns.map(col => col.header)],
          body: tableData.map(row => tableColumns.map(col => row[col.dataKey])),
          theme: 'grid',
          styles: {
            overflow: 'linebreak',
            cellPadding: 2,
            fontSize: 8,
            valign: 'middle'
          },
          columnStyles: {
            0: { cellWidth: 25 }, // Time column width
          },
          headStyles: {
            fillColor: [0, 121, 88],
            textColor: 255,
            fontSize: 10
          }
        });
      });

      pdf.save('timetable.pdf');
      setError(null);
    } catch (error) {
      console.error('PDF generation error:', error);
      setError(`Failed to generate PDF: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          mb: 4 
        }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Class Schedule
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={getTimeTable}
              startIcon={<Refresh />}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Timetable'}
            </Button>
            {!loading && clicked && Object.keys(data).length > 0 && (
              <Button
                variant="contained"
                color="secondary"
                onClick={downloadTimetable}
                startIcon={<Download />}
                disabled={loading}
              >
                {loading ? 'Generating PDF...' : 'Download PDF'}
              </Button>
            )}
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        )}

        {!loading && clicked && Object.keys(data).length === 0 && (
          <Alert severity="info">
            No timetable data available. Click Generate Timetable to create a new schedule.
          </Alert>
        )}

        {!loading && Object.keys(data).length > 0 && (
          Object.keys(data).map((section) => (
            <Paper 
              key={section} 
              elevation={3} 
              sx={{ mb: 4, overflow: 'hidden' }}
              className="timetable-section"
            >
              <Box sx={{ bgcolor: 'primary.main', p: 2 }}>
                <Typography variant="h6" sx={{ color: 'white' }}>
                  Section {section}
                </Typography>
              </Box>
              <Box sx={{ p: 2 }}>
                <div style={{ display: "flex", flexDirection: "column" }}>
                  <div style={{ display: "flex" }}>
                    <div style={{ 
                      flex: "1", 
                      border: "1px solid #e0e0e0", 
                      padding: "16px",
                      backgroundColor: '#f5f5f5'
                    }}>
                      <Typography variant="subtitle2" fontWeight="bold">Time</Typography>
                    </div>
                    {daysOfWeek.map((day) => (
                      <div key={day} style={{ 
                        flex: "1", 
                        border: "1px solid #e0e0e0", 
                        padding: "16px",
                        backgroundColor: '#f5f5f5'
                      }}>
                        <Typography variant="subtitle2" fontWeight="bold">{day}</Typography>
                      </div>
                    ))}
                  </div>

                  {slots.map((slot) => (
                    <div key={slot} style={{ display: "flex", position: "relative" }}>
                      <div style={{ 
                        flex: "1", 
                        border: "1px solid #e0e0e0",
                        padding: "16px",
                        minHeight: "80px",
                        backgroundColor: '#fafafa'
                      }}>
                        <Typography variant="body2">{slotToTime(slot)}</Typography>
                      </div>
                      {daysOfWeek.map((day) => {
                        const event = data[section]?.find(
                          (e) => e.day === day && e.startSlot <= slot && slot < e.startSlot + e.duration
                        );
                        return (
                          <div key={day} style={{ 
                            flex: "1", 
                            border: "1px solid #e0e0e0",
                            padding: "8px",
                            minHeight: "80px",
                            position: "relative"
                          }}>
                            {event && event.startSlot === slot && (
                              <Paper
                                elevation={2}
                                sx={{
                                  p: 1,
                                  bgcolor: 'primary.main',
                                  position: 'absolute',
                                  top: 0,
                                  left: 0,
                                  right: 0,
                                  height: `${event.duration * 80}px`,
                                  zIndex: 1,
                                  m: 1
                                }}
                              >
                                <Typography variant="body2" sx={{ color: 'white', fontWeight: 'bold' }}>
                                  {event.name}
                                </Typography>
                                <Divider sx={{ my: 0.5, borderColor: 'rgba(255,255,255,0.2)' }} />
                                <Typography variant="caption" sx={{ color: 'white', display: 'block' }}>
                                  {event.room}
                                </Typography>
                                <Typography variant="caption" sx={{ color: 'white', display: 'block' }}>
                                  {event.instructor}
                                </Typography>
                              </Paper>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </Box>
            </Paper>
          ))
        )}
      </Box>
    </Container>
  );
};

export default ViewTimeTable;