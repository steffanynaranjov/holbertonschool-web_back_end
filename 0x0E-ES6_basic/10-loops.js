export default function appendToEachArrayValue(array, appendString) {
  const appendValue = [];
  for (const value of array) {
    appendValue.push(`${appendString}${value}`);
  }

  return appendValue;
}
