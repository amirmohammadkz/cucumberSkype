function send_massage(massage, id, type) {
    var xhr = new XMLHttpRequest();
    var inp = "/channel/send/"+id+"/"+type;
    xhr.open('POST', inp, true);
    xhr.send(massage);
}