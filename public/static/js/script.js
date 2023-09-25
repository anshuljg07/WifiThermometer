let socket = io.connect('http://172.17.7.178:3000');
socket.emit('clientType', 'frontend');

let ctx = document.getElementById('temperatureChart').getContext('2d');
let temperatureData = {
    labels: ['3:10', '3:11', '3:12', '3:13', '3:14'],  // Sample months for demonstration
    datasets: [{
        label: 'Temperature (°C)',
        data: [70, 75, 68, 80, 82],  // Sample temperature data for demonstration
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        fill: false
    }]
};

let tempChart = new Chart(ctx, {
    type: 'line',
    data: temperatureData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

//TODO: Test if index.js -> script.js newData update works.
socket.on('newData', (data) => {
    temperatureData.labels.push(new Data().toLocaleTimeString())
    temperatureData.datasets[0].data.push(data.temp_c);

    if(temperatureData.labels.length > 10){ //updates on 10 datapoints, check lab specs
        temperatureData.labels.shift();
        temperatureData.datasets[0].data.shift();
    }

    tempChart.update();
})