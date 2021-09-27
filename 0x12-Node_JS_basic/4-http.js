const http = require("http");

const app = http
  .createServer((req, res) => {
    console.log(req.url);
    res.write("Hello Holberton School!");
    res.end();
  })
  .listen(1245);

module.exports = app;
