const express = require('express');
const cors = require("cors");
const app = express();
const fs = require('fs');
const sizeOf = require('image-size');

// configure CORS
app.use(cors({origin: "*"}));

let byGroup = require('../by_group.json');
let timePeriods = byGroup[0];
let byGroupValues = byGroup[1];
const indexFaces = 7;

const img_collection_dir = "../imgCollection";

app.get('/chart/faces', (req, res) => {

  res.setHeader('Content-Type', 'application/json');

  let data = []
  console.log(byGroupValues)
  timePeriods.forEach((timePeriod) => {
    if (byGroupValues[timePeriod] != null)
      data.push({ time_period: timePeriod, value: byGroupValues[timePeriod][indexFaces] });
  });

  res.end(JSON.stringify(data));

});


app.get("/img_collection/:time_period/:id", (req, res) => {

  let time_period = req.params.time_period;
  console.log(time_period);
  let id = req.params.id;
  console.log(id);

  res.setHeader('Content-Type', 'image/jpg');
  path = img_collection_dir + "/" + time_period;
  // console.log(path);

  fs.readdir(path, (err, files) => {

    files.sort();
    fileName = files[id % files.length];
    // dimensions = sizeOf(path + "/" + fileName);
    // console.log(dimensions);
    // console.log(fileName);
    res.sendFile(fileName, { root: path });

  });

});


// Start the server
app.listen(3000, () => console.log('Server listening on port 3000'));
