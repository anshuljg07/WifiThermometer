const express = require("express");
const http = require("http"); // Import the http module
const socketIo = require("socket.io");

const app = express();
const server = http.createServer(app); // Create an HTTP server using Express
const io = socketIo(server); // Attach Socket.io to the server

let TempData = []

//server's static files dervied from public folder
app.use('/public', express.static('public'));

server.listen(3000, '172.17.67.110', ()=>{
    console.log("successfully listening on Port 3000 w/ IP: 172.17.7.178")
});

// server.listen(3000, '192.168.0.10', ()=>{
//     console.log("successfully listening on Port 3000 w/ IP: 172.17.7.178")
// });

app.get('/', (req, res) => {        //get requests to the root ("/") will route here
    res.sendFile('./views/index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser
                                                        //the .sendFile method needs the absolute path to the file, see: https://expressjs.com/en/4x/api.html#res.sendFile
});

io.on('connection', function(socket) {
    console.log("New Client has connected")

    socket.on('clientType', function(type) {
        if(type == 'raspberryPi'){
            console.log('raspberryPi has connected')
            socket.join('raspberryPi')
        }
        else if(type == 'frontend')
            console.log('frontend has connected')
            socket.join('frontend')
    });

    socket.on('temp data', (data)=>{
        console.log('Received Temperature Data: ', data);

        TempData.push({
            temp_c: data.temp_c,
            temp_f: data.temp_f
        });

        console.log('Attempting to send to FrontEnd Socket room')
        io.to('frontend').emit('newData', data)
    });
});


