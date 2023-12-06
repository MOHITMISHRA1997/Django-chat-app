const logged_in_user = document.getElementById('logged_in_user').innerText
console.log('This is logged_in user',logged_in_user)


const online_websocket = new WebSocket('ws://' + window.location.host + '/ws/sc/'+'status/')

online_websocket.onopen = function (event) {
    console.log('websocket status has been connected..',event)
    online_websocket.send(JSON.stringify({'username': logged_in_user, 'type': 'open'}));
  }

window.addEventListener('beforeunload',function(event) {
    online_websocket.send(JSON.stringify({
        'username': logged_in_user,
        'type':'offline'
    }))
    
})


online_websocket.onmessage = function (event) {
    var data = JSON.parse(event.data)
    console.log('status message has been recived from client..',event)
  }


online_websocket.onerror = function (event) {
    console.log('status websocket got some errors...',event)
  }



online_websocket.onclose = function (event) {
    console.log('status got disconnected..',event)
  }