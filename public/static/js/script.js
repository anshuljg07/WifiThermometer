let socket = io.connect('http:// 172.17.4.165:3000');
socket.emit('clientType', 'frontend');

let ctx = document.getElementById('temperatureChart').getContext('2d');
let temperatureData = {
    labels: [0,100,200,300],  // Sample months for demonstration
    datasets: [{
        label: 'Temperature (°C)',
        data: [],  // Sample temperature data for demonstration
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        fill: false
    }]
};
function convertClick(){
    document.getElementById("convert").textContent = "convert to C"
}
$(function () {
    $("#chartContainer").resizable({
        aspectRatio: true,
        // maxHeight: 500,
        distance: 10,
        // animate: true,
        // animateDuration: "fast",
        // animateEasing: "swing",
        // autoHide: true,

    });
});


let tempChart = new Chart(ctx, {
    type: 'line',
    data: temperatureData,
    options: {
        animationEnabled: true,
        responsive: true,
        scales: {
            y: {
                max: 50,
                min: 10,
                beginAtZero: true
            },
            x:{
                max: 300,
                min: 0,
                stepSize: 100,
                maxTicksLimit: 3
            }
        }
    }
});

socket.on('newData', (data) => {
    console.log('FrontEnd Received: ', data)
    temperatureData.labels.push(data.timestamp)
    temperatureData.datasets[0].data.push(data.temp_c);

    if(temperatureData.labels.length > 300){ //updates on 10 datapoints, check lab specs
        temperatureData.labels.shift();
        temperatureData.datasets[0].data.shift();
    }

    tempChart.update();
})