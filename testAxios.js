const axios = require('axios');

// axios.get('http://127.0.0.1:8000/api/test-endpoint/')
axios.get('https://jubilant-telegram-pvg59rv6g9r26qjr-8000.app.github.dev/api/test-endpoint/')
  .then((response) => {
    console.log("Success:", response.data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });
// const body = {
//   name: "Parallel and Distributed Computing",
//   lectureno: "1",
//   duration: "3",
//   instructor_name: "Dr. Raazia Sosan",
//   start_hr: "8",
//   end_hr: "4"
// };

// const config = {
//   headers: {
//     'Accept': 'application/json, text/plain, */*',
//     'Content-Type': 'application/json',
//     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
//     // Add any other headers that are present in the browser request
//   }
// };

// axios.post('http://127.0.0.1:8000/api/add-course/', body)
//   .then((response) => {
//     console.log("Success:", response.data);
//   })
//   .catch((error) => {
//     console.error("Error:", error);
//   });