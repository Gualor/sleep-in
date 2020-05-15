var table = document.getElementById('eff_dict');
var sleep_data = [];
var day_label = [];


for (var i = 0; i < table.rows.length; i++) {
  var day = table.rows[i].cells[0].innerHTML
  var num = table.rows[i].cells[1].innerHTML
  day_label.push(day)
  sleep_data.push(num)
};

var ctx = document.getElementById('patientChart').getContext('2d');
var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: 'line',

  // The data for our dataset
  data: {
    labels: day_label,
    datasets: [{
      label: 'Daily Sleep Index',
      backgroundColor: '#0694b1',
      borderColor: '#0694b1',
      data: sleep_data
    }]
  },

  // Configuration options go here
  options: {
    scales: {
      yAxes: [{
        display: true,
        ticks: {
          min: 0,
          max: 100,
          stepSize: 20
        }
      }]
    }
  }
});

console.log(sleep_data);