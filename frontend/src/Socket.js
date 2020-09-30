import io from "socket.io-client";

const socket = io('http://localhost:5000');
socket.on("connect", data => {
    console.log("connected to server");
    socket.emit("send_message", "hi")
});

export default socket;