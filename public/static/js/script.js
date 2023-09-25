let socket = io.connect('http://172.17.39.169:3000');
socket.emit('clientType', 'frontend');

let ctx = document.getElementById('temperatureChart').getContext('2d');
let temperatureData = {
    labels: [],  // Sample months for demonstration
    datasets: [{
        label: 'Temperature (°C)',
        data: [],  // Sample temperature data for demonstration
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

socket.on('newData', (data) => {
    console.log('FrontEnd Received: ', data)
    temperatureData.labels.push(data.timestamp)
    temperatureData.datasets[0].data.push(data.temp_c);

    if(temperatureData.labels.length > 180){ //updates on 10 datapoints, check lab specs
        temperatureData.labels.shift();
        temperatureData.datasets[0].data.shift();
    }

    tempChart.update();
})