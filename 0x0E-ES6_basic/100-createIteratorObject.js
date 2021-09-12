export default function createIteratorObject(report) {
  const values = [];

  const departmentsList = Object.values(report.allEmployees);
  for (const value of departmentsList) {
    values.push(...value);
  }

  return values;
}
