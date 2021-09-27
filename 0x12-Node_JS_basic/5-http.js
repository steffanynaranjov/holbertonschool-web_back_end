const http = require("http");
const countStudents = require("./3-read_file_async");

const PATH = process.argv[2];
const PORT = 1245;

async function router(req, res) {
  if (req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("Hello Holberton School!");
  } else if (req.url === "/students") {
    const { students, studentsByCS, studentsBySWE } = await countStudents(PATH);
    try {
      res.write("This is the list of our students\n");
      res.write(`Number of students: ${students.length}\n`);
      res.write(
        `Number of students in CS: ${
          studentsByCS.length
        }. List: ${studentsByCS.join(", ")}\n`
      );
      res.write(
        `Number of students in SWE: ${
          studentsBySWE.length
        }. List: ${studentsBySWE.join(", ")}`
      );
      res.end();
    } catch (error) {
      res.end(error.message);
    }
  } else {
    res.writeHead(404);
    res.end("Invalid request");
  }
}

const app = http.createServer(router).listen(PORT);

module.exports = app;
