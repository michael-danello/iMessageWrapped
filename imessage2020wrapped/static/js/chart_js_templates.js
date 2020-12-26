var getData = $.get('/data/all_days')
getData.done(function(results) {
  var strResults = JSON.stringify(results);
  var labels = results['day'];
  var data = results;
  var element_id = "day-chart";
  yearBarChart(labels, data, element_id, "month", "Texts by Day");
});

var getData = $.get('/data/all_hours')
getData.done(function(results) {
  var strResults = JSON.stringify(results);
  var labels = results['time'];
  var data = results;
  var element_id = "hour-chart";
  hourBarChart(labels, data, element_id, "Texts by Hour");
});

var getData = $.get('/data/week_days')
getData.done(function(results) {
  var strResults = JSON.stringify(results);
  var labels = results['day'];
  var data = results;
  var element_id = "weekday-chart";
  weekdayBarChart(labels, data, element_id, "Texts by Day of the Week");
});

// Bar chart
function yearBarChart(labels, data, element_id, time_unit, title) {
  var strResults = JSON.stringify(data);
  var labels = labels;
  var data = data
  new Chart(document.getElementById(element_id), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: "Messages Sent",
            backgroundColor: "#3e95cd",
            data: data['from_me']
          },
          {
            label: "Messages Recieved",
            backgroundColor: "#008000",
            data: data['to_me']
          }
        ]
      },
      options: {
        legend: { display: false },
        title: {
          display: true,
          text: title
        },
        tooltip: {
          mode: 'index',
          intersect: false
        },
        responsive: true,
        scales: {
          xAxes: [{
              stacked: true,
              type: 'time',
                time: {
                    unit: 'month'
                }

          }],
          yAxes: [{
              stacked: true
          }]

    }
      }
  });
};


function hourBarChart(labels, data, element_id, title) {
  var strResults = JSON.stringify(data);
  var labels = labels;
  var data = data
  new Chart(document.getElementById(element_id), {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: "Messages Sent",
            backgroundColor: "rgba(0,0,251,0.2)",
            data: data['from_me']
          },
          {
            label: "Messages Recieved",
            backgroundColor: "rgba(30,126,52,0.2)",
            data: data['total_chats']
          },
          {
            label: "Total Messages",
            backgroundColor: "rgb(127 255 212 / 0.38)",
            data: data['to_me']
          }
        ]
      },
      options: {
        legend: { display: true },
        title: {
          display: true,
          text: title
        },
        responsive: true,
      }
  });
};

function weekdayBarChart(labels, data, element_id, title) {
  var strResults = JSON.stringify(data);
  var labels = labels;
  var data = data
  new Chart(document.getElementById(element_id), {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: "Messages Sent",
            backgroundColor: "rgba(0,0,251,0.5)",
            data: data['from_me']
          },
          {
            label: "Messages Recieved",
            backgroundColor: "rgba(30,126,52,0.5)",
            data: data['to_me']
          }
        ]
      },
      options: {
        legend: { display: false },
        title: {
          display: true,
          text: title
        },
        tooltip: {
          mode: 'index',
          intersect: false
        },
        responsive: true,
      }
  });
};
