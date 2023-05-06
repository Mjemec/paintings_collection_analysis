const express = require('express');
const cors = require("cors");
const app = express();
const fs = require('fs');

// configure CORS
app.use(cors({origin: "*"}));

let byGroup = require('../by_group.json');
let timePeriods = byGroup[0];
let byGroupValues = byGroup[1];
const indexFaces = 7;

const time_period_examples_dir = "../time_period_examples";

app.get('/chart/sample', (req, res) => {
  
  const data = [
    { year: 2010, count: 10 },
    { year: 2011, count: 20 },
    { year: 2012, count: 15 },
    { year: 2013, count: 25 },
    { year: 2014, count: 22 },
    { year: 2015, count: 30 },
    { year: 2016, count: 28 },
  ];

  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(data));

});

app.get('/chart/faces', (req, res) => {

  res.setHeader('Content-Type', 'application/json');

  let data = []
  timePeriods.forEach((timePeriod) => {
    data.push({ time_period: timePeriod, value: byGroupValues[timePeriod][indexFaces] });
  });

  res.end(JSON.stringify(data));

});


app.get("/time_period_examples/:category/:time_period", (req, res) => {

  let category = req.params.category;
  let time_period = req.params.time_period;
  console.log(category);
  console.log(time_period);

  res.setHeader('Content-Type', 'image/jpg');
  path = time_period_examples_dir + "/" + category + "/" + time_period;
  console.log(path);

  let fileName = "";
  fs.readdirSync(path).forEach(file => {
    fileName = file;
  });

  console.log(fileName);
  res.sendFile(fileName, { root: path });

});


// Start the server
app.listen(3000, () => console.log('Server listening on port 3000'));
