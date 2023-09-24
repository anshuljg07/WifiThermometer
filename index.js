// const express = require("express");
// const app = express();
// //var server = require("http").Server(app);
// var server = Server(app);
// var io = require("socket.io")(server);
// const port = 3000;

const express = require("express");
const http = require("http"); // Import the http module
const socketIo = require("socket.io");

const app = express();
const server = http.createServer(app); // Create an HTTP server using Express
const io = socketIo(server); // Attach Socket.io to the server

let TempData = []

server.listen(3000, '172.17.7.178', ()=>{
    console.log("successfully listening on Port 3000 w/ IP: 172.17.7.178")
});

// server.listen(3000, ()=>{
//     console.log("successfully listening on Port 3000")
//})

app.get('/', (req, res) => {        //get requests to the root ("/") will route here
    res.sendFile('index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser
                                                        //the .sendFile method needs the absolute path to the file, see: https://expressjs.com/en/4x/api.html#res.sendFile
});

io.on('connection', function(socket) {
    socket.on('temp data', (data)=>{
        console.log('Received Temperature Data: ', data);

        TempData.push({
            temp_c: data.temp_c,
            temp_f: data.temp_f
        })
    });
});

