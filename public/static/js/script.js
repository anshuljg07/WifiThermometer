

let socket = io.connect('http://172.17.66.142:3000');
socket.emit('clientType', 'frontend');

masterSwitchBool = true;


let ctx = document.getElementById('temperatureChart').getContext('2d');
let temperatureDataC = {
    labels: new Array(300),  // Sample months for demonstration
    datasets: [{
        label: 'Temperature (°C)',
        data: [],  // Sample temperature data for demonstration
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 4,
        fill: false,
        pointRadius: 1,
    }]
};

let temperatureDataF = {
    labels: [],  // Sample months for demonstration
    datasets: [{
        label: 'Temperature (°F)',
        data: [],  // Sample temperature data for demonstration
        borderColor: 'rgba(0, 255, 0, 1)',
        borderWidth: 4,
        fill: false,
        pointRadius: 1,
    }]
};
function convertClickC(){
    tempChart.data = temperatureDataC
    tempChart.options.scales.y.max = 50
    tempChart.options.scales.y.min = 10
    tempChart.update()

}

function convertClickF(){
    tempChart.data = temperatureDataF
    tempChart.options.scales.y.max = 122
    tempChart.options.scales.y.min = 50
    tempChart.update()

}
$(function () {
    $("#chartContainer").resizable({
        aspectRatio: true,
        minHeight : 500,
        // maxHeight: 500,
        distance: 10,


    });
});


    function GetPhoneNumber(){
        var tempPhone = document.getElementById("phoneNumber").value
        var pattern = /^\d{3}-\d{3}-\d{4}$/;
        if(pattern.test(tempPhone)){
            socket.emit('phone number', tempPhone);
        }
        //socket.emit('phone number', tempPhone);
    }
    function formatPhoneNumber() {

        var phoneNumber = document.querySelector('#phoneNumber')

        phoneNumber.value = phoneNumber.value.replace(/[^0-9-]/g, '');

        phoneNumber.addEventListener('keyup', function(e){
            if (event.key != 'Backspace' &&
                (phoneNumber.value.length === 3 || phoneNumber.value.length === 7)){
                phoneNumber.value += '-';
            }
        })

    // let phoneNumber = input.value.replace(/[^0-9\+\-]/g, '');
    //
    // // Add a +1 at the beginning if it's not already there
    // if (!phoneNumber.startsWith('+1-') || phoneNumber == '') {
    // phoneNumber = '+1-' + phoneNumber;
    // }
    //
    // // Apply the formatting based on the length
    // if (phoneNumber.length == 6) {
    //     phoneNumber = phoneNumber + '-';
    // }
    //
    // if (phoneNumber.length == 9) {
    //     phoneNumber = phoneNumber + '-';
    // }
    //
    // if (phoneNumber.length == 12) {
    //     phoneNumber = phoneNumber.substring(0,11);
    // }
    // input.value = phoneNumber;
}



    function masterSwitchState(){
        if( document.getElementById("MasterSwitch").innerText== "OFF") {
            console.log("off")
            document.getElementById("MasterSwitch").style.background = "green"
            document.getElementById("MasterSwitch").textContent = "ON"
            document.getElementById("MasterSwitch").innerText = "ON"
        }else{
            console.log("on")
            document.getElementById("MasterSwitch").style.background = "red"
            document.getElementById("MasterSwitch").textContent = "OFF"
            document.getElementById("MasterSwitch").innerText = "OFF"
        }
        masterSwitchBool = !masterSwitchBool;
        socket.emit('master switch state', {masterSwitchState: masterSwitchBool})
    }

let tempChart = new Chart(ctx, {
    type: 'line',
    data: temperatureDataC,
    options: {
        animation:
            {
                duration: 0,
            },
        responsive: true,
        scales: {
            y: {
                position: 'right',
                max: 50,
                min: 10,
                beginAtZero: true
            },
            x:{
                reverse: true,
                min: 0,
                max: 300,
                stepSize: 100,
                maxTicksLimit: 3
            }
        },
    }
});

function loadLabels(){
    for(var i = 0; i <300;i++){
        if(i==0){
            temperatureDataF.labels[i] = "0"
            temperatureDataC.labels[i] = "0"
        }else if(i==102){
            temperatureDataF.labels[i] = "100"
            temperatureDataC.labels[i] = "100"
        }else if(i==204){
            temperatureDataF.labels[i] = "200"
            temperatureDataC.labels[i] = "200"
        }else if(i==294){
            temperatureDataF.labels[i] = "300"
            temperatureDataC.labels[i] = "300"      }
        else{
            temperatureDataF.labels[i] = ""
            temperatureDataC.labels[i] = ""
        }
    }
    tempChart.update();
}


//todo

function dropDown(){
    if(document.getElementById("#content").style.display == "none"){
        document.getElementById("#content").style.display = "block"

    }else{
        document.getElementById("#content").style.display = "none"

    }
}
function updateVariable(tempData) {

    document.getElementById("temperature").textContent = tempData.temp_c;
    if(tempData.temp_c === 'NO DATA AVAILABLE' || tempData.temp_c === 'SENSOR DISCONNECTED'){
        document.getElementById("status").textContent =  tempData.temp_c;
        document.getElementById("statusButton").style.background= "red"
    }else{
        document.getElementById("status").textContent = `OPERATIONAL`;
        document.getElementById("statusButton").style.background = "green"
    }

}

//todo

tempC = []
tempF = []
loadLabels();
socket.on('newData', (data) => {
    console.log('FrontEnd Received: ', data)
    updateVariable(data)
    tempC.push(data.temp_c)
    temperatureDataC.datasets[0].data = tempC.reverse();

    if(temperatureDataC.datasets[0].data.length > 300){ //updates on 10 datapoints, check lab specs
        //temperatureDataC.labels.shift();
        temperatureDataC.datasets[0].data.pop();
    }
    tempF.push(data.temp_f)
    temperatureDataF.datasets[0].data = tempF.reverse();

    if(temperatureDataF.datasets[0].data.length > 300){ //updates on 10 datapoints, check lab specs
        //temperatureDataF.labels.shift();
        temperatureDataF.datasets[0].data.pop();
    }

    tempChart.update();
    tempC.reverse()
    tempF.reverse()
})