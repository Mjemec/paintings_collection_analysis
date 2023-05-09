
// intellisense for jquery in vscode
/// <reference path="../node_modules/@types/jquery/index.d.ts" />

import Chart from 'chart.js/auto'
import { getRelativePosition } from 'chart.js/helpers';

const id2time_peroid = [
  "realism",
  "early_renaissance",
  "baroque",
  "symbolism",
  "high_renaissance",
  "romanticism",
  "impressionism",
  "color_field_painting",
  "post_impressionism",
  "expressionism",
  "northern_renaissance",
  "naive_art_primitivism",
  "art_nouveau_modern",
  "cubism",
  "rococo",
  "minimalism",
  "pointillism",
  "analytical_cubism",
  "abstract_expressionism",
  "mannerism_late_renaissance",
  "contemporary_realism",
  "ukiyo_e",
  "pop_art",
  "fauvism",
  "action_painting",
  "new_realism",
  "synthetic_cubism"
];

(async function() {

  let promise = getFaceData();

  promise.done((data) => {
    let chart = new Chart(
        document.getElementById('barChart'),
        {
          type: 'bar',
          data: {
            labels: data.map(row => snakeCase2properCase(row.time_period)),
            datasets: [
              {
                label: 'Average number of faces by time period',
                data: data.map(row => row.value)
              }
            ]
          },
          options: {
            maintainAspectRatio: false,
            indexAxis: 'y',
            onClick: (e) => {
                const canvasPosition = getRelativePosition(e, chart);
    
                // Substitute the appropriate scale IDs
                const dataX = chart.scales.x.getValueForPixel(canvasPosition.x);
                const dataY = chart.scales.y.getValueForPixel(canvasPosition.y);
                // console.log(dataY);
                console.log("Clicked column: " + dataY);
                showImages(id2time_peroid[dataY]);

            }
          }
        }
      );
  });

})();

function snakeCase2properCase(str) {
  return str.replace(/^_*(.)|_+(.)/g, (s, c, d) => c ? c.toUpperCase() : ' ' + d.toUpperCase());
};
