const express = require("express");
const path = require("path");
const { fileURLToPath } = require("url");

const app = express();

app.use(express.static("public"));

app.use("/lib", express.static(path.join(__dirname, "lib")));

app.use((req, res, next) => {
  console.log(`Request URL: ${req.url}`);
  next();
});

console.log(path.join(__dirname, "public"));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "index.html"));
});

app.listen(3000, () => {
  console.log("Server started on port 3000");
});
