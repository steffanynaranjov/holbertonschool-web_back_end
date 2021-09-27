const fs = require("fs");

function getStudents(lines) {
  return lines
    .map((data) => data.split(","))
    .filter((student) => /\w{3,}/.test(student[0]))
    .map((student) => ({
      firstName: student[0],
      lastName: student[1],
      age: student[2],
      field: student[3],
    }));
}

function getStudentsByField(students) {
  const csStudents = students
    .filter((student) => student.field === "CS")
    .map((student) => student.firstName);

  const sweStudents = students
    .filter((student) => student.field === "SWE")
    .map((student) => student.firstName);

  return [csStudents, sweStudents];
}

module.exports = async function countStudents(path) {
  if (!fs.existsSync(path)) {
    throw new Error("Cannot load the database");
  }
  const data = fs.readFileSync(path, { encoding: "utf8", flag: "r" });
  const lines = data.split("\n").slice(1);

  const students = await getStudents(lines);
  const [studentsByCS, studentsBySWE] = await getStudentsByField(students);

  console.log(`Number of students: ${students.length}`);
  console.log(
    `Number of students in CS: ${
      studentsByCS.length
    }. List: ${studentsByCS.join(", ")}`
  );
  console.log(
    `Number of students in SWE: ${
      studentsBySWE.length
    }. List: ${studentsBySWE.join(", ")}`
  );

  return { students, studentsByCS, studentsBySWE };
};
