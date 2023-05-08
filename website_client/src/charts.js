
// intellisense for jquery in vscode
/// <reference path="../node_modules/@types/jquery/index.d.ts" />

import Chart from 'chart.js/auto'
import { getRelativePosition } from 'chart.js/helpers';

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
                console.log("Clicked column: " + dataX);
                // console.log(dataY);
                showImages(dataX);

            }
          }
        }
      );
  });

})();

function snakeCase2properCase(str) {
  return str.replace(/^_*(.)|_+(.)/g, (s, c, d) => c ? c.toUpperCase() : ' ' + d.toUpperCase());
};
