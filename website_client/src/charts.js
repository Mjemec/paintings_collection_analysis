
// intellisense for jquery in vscode
/// <reference path="../node_modules/@types/jquery/index.d.ts" />

import Chart from 'chart.js/auto'
import { getRelativePosition } from 'chart.js/helpers';

const id2time_peroid = [
  "early_renaissance",
  "high_renaissance",
  "mannerism_late_renaissance",
  "northern_renaissance",
  "baroque",
  "ukiyo_e",
  "rococo",
  "realism",
  "impressionism",
  "romanticism",
  "symbolism",
  "pointillism",
  "art_nouveau_modern",
  "naive_art_primitivism",
  "post_impressionism",
  "fauvism",
  "cubism",
  "analytical_cubism",
  "expressionism",
  "color_field_painting",
  "abstract_expressionism",
  "action_painting",
  "pop_art",
  "contemporary_realism",
  "new_realism",
  "minimalism"
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
