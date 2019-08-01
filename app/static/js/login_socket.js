// Generate a random string, that will act as a unique ID for our URL
// currently not used -- maybe as a method to stop replay attack later

function createID() {
    var text = "",
        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < 20; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

var ws = new WebSocket("ws://35.246.61.212/"),
    messages = document.createElement('ul'),
    submit = document.getElementById('mysubmit');

ws.onopen = function() {
    console.log('Opened websocket');
};

sessionInfo = {'uID' : '', 'signature': ''};
var msg = 0;

ws.onmessage = function (event) {
    var content = document.createTextNode(event.data),
        dataJSON = JSON.parse(event.data);
    
    console.log(dataJSON);

    if (dataJSON['type'] == "uID" && msg == 0) {
        console.log('We have uID');
        
        console.log(dataJSON['uID']);
        sessionInfo['uID'] = dataJSON['uID'];
        document.getElementById('session-id').innerHTML = dataJSON['uID'];
        var qr = new QRious({
          element: document.getElementById('qr'),
          size: 200,
          value: JSON.stringify({
                'type': 'loginSig',
                'wsURL': 'ws://35.246.61.212/',
                'uID': dataJSON['uID'],
                'data' : 'a pubKey of somesort',
                'expirytime' : '',
            })
        });
        msg += 1;
    } else if(dataJSON['type'] == 'loginSigSigned') {
        console.log('We have signature');
        console.log(dataJSON['loginSigSigned']);
        sessionInfo['signature'] = dataJSON['loginSigSigned'];
        console.log(sessionInfo);
    }

    console.log(event.data);

    if (sessionInfo['signature'] != '') {
        endURL = sessionInfo['uID']+'/'+sessionInfo['signature'];
        window.location.href = 'http://localhost:5000/login/confirm/'+endURL
    }

    //console.log(window.location.href = 'http://localhost:5000/login/'+event.data;
};


document.getElementById('loading').style.visibility = 'hidden';
document.getElementById('login-content').style.visibility = 'visible';