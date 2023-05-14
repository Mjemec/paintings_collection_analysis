const express = require('express');
const cors = require("cors");
const app = express();
const fs = require('fs');
const sizeOf = require('image-size');

// configure CORS
app.use(cors({origin: "*"}));

let byGroup = require('../by_group.json');
let timePeriods = [...new Set(byGroup[0])];
let byGroupValues = byGroup[1];

const img_collection_dir = "../imgCollection";

app.get('/chart/:filter', (req, res) => {

  let filter = req.params.filter;
  let filter2index = {
    "lines": 6,
    "faces": 7,
    "poses": 8,
    "contours": 9
  }
  let index = filter2index[filter];

  res.setHeader('Content-Type', 'application/json');

  let data = []
  timePeriods.forEach((timePeriod) => {
    if (byGroupValues[timePeriod] != null)
      data.push({ time_period: timePeriod, value: byGroupValues[timePeriod][index] });
  });

  res.end(JSON.stringify(data));

});


app.get("/img_collection/:variant/:time_period/:id", (req, res) => {

  let variant = req.params.variant;
  console.log("variant: " + variant);
  let time_period = req.params.time_period;
  console.log("time period: " + time_period);
  let id = req.params.id;
  console.log("id: " + id);

  let variant2path = {
    "default": "",
    "pose": "_pose",
    "lines": "_lines",
    "dim": "_dim"
  };
  let variantExtensions = Object.values(variant2path).filter(s => s != "");

  variant = variant2path[variant];
  console.log("variant2path: " + variant);

  res.setHeader('Content-Type', 'image/jpg');
  path = img_collection_dir + "/" + time_period;
  // console.log(path);

  fs.readdir(path, (err, files) => {

    if (files == null)
      res.end();
    else {

      // don't include _pose, _face etc.
      // files = files.filter(file => variantExtensions.filter(ext => file.includes(ext)).length == 0);
      files = files.filter(file => null != file.match(/image_[0-9]+\.[^_]+/g));

      files.sort();
      let filePath = files[id % files.length];
      let fileName = filePath.match(/.*\./g)[0];
      if (fileName.charAt(fileName.length - 1) == ".")
        fileName = fileName.substring(0, fileName.length - 1);
      let fileExtension = "." + filePath.replace(/.*\./g, "");

      // add variant
      filePath = fileName + variant + fileExtension;

      // console.log("filePath: " + filePath);
      // console.log("fileName: " + fileName);
      // console.log("fileExtension: " + fileExtension);
      // console.log();

      if (variant == "_dim") {
        let dimensions = sizeOf(path + "/" + fileName + fileExtension);
        // console.log(dimensions);
        res.send(dimensions);
      }
      else {
        res.sendFile(filePath, { root: path });
      }

    }

  });
  console.log();

});

// Start the server
app.listen(3000, () => console.log('Server listening on port 3000'));
