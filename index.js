const express = require("express");
const app = express();
var server = require("http").Server(app);
var io = require("socket.io")(server);
const port = 3000;

let TempData = []

server.listen(3000, ()=>{
    console.log("successfully listening on Port 3000")
})

io.on('connection', function(socket) {
    socket.on('temp data', (data)=>{
        console.log('Received Temperature Data: ', data);

        TempData.push({
            temp_c: data.temp_c,
            temp_f: data.temp_f
        })
    });
});

