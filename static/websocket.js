function websocket(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/webSigChannel');
    socket.on('connect', function() {
        socket.emit("new message ");
    });
    socket.on('message', function(msg){

}
