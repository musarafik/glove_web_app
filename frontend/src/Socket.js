import io from "socket.io-client";
import ec2Url from './Utilities';

const socket = io(ec2Url);
socket.on("connect", data => {
    console.log("connected to server");
    socket.emit("send_message", "hi")
});

export default socket;