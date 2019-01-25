    var localVideo = document.getElementById('localVideo');
    var remoteVideo = document.getElementById('remoteVideo');

    var peerConnectionConfig = {
        'iceServers': [
            {'urls': 'stun:stun.services.mozilla.com'},
            {'urls': 'stun:stun.l.google.com:19302'},
            {
                'urls': 'turn:turn.salar.click:3478?transport=udp',
                'credential': 'PASSWORD',
                'username': 'salar'
            },
        ]
    };

    var peerConnection = new RTCPeerConnection(peerConnectionConfig);
    peerConnection.onaddstream = gotRemoteStream;
    peerConnection.onicecandidate = gotIceCandidate;

    var constraints = {
        video: true
    };

    if(navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia(constraints).then(getUserMediaSuccess).catch(errorHandler);
    } else {
        alert('Your browser does not support getUserMedia API');
    }

function getUserMediaSuccess(stream) {
    console.log("getUserMediaSuccess");
    localStream = stream;
    localVideo.src = window.URL.createObjectURL(stream);
    peerConnection.addStream(localStream);
    }

function gotIceCandidate(event) {
    if(event.candidate != null) {
        send_massage(JSON.stringify({'ice': event.candidate}) , "{{name}}", 'ice2');

    }
}

    function errorHandler(error) {
        console.log(error);
    }

    var source = new EventSource("/stream?channel="+"{{name}}");
    source.addEventListener('request', gotRequest);

    function gotRequest(event) {
        var data = JSON.parse(event.data);
        data =  JSON.parse(data.message);
        peerConnection.setRemoteDescription(new RTCSessionDescription(data.sdp)).then(function() {
            peerConnection.createAnswer().then(createdDescription).catch(errorHandler);
        }).catch(errorHandler);

    }

    source.addEventListener('ice1', gotIce);
    function gotIce(event) {
        var data = JSON.parse(event.data);
        data =  JSON.parse(data.message);
        peerConnection.addIceCandidate(new RTCIceCandidate(data.ice)).catch(errorHandler);
    }


   function createdDescription(description) {
        peerConnection.setLocalDescription(description).then(function() {
            send_massage(JSON.stringify({'sdp': peerConnection.localDescription}) , "{{name}}", 'response');

        }).catch(errorHandler);
    }

    function gotRemoteStream(event) {
        remoteVideo.src = window.URL.createObjectURL(event.stream);
    }