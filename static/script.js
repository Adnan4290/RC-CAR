// Define a function to send the control data to the server
function getData() {
  $.ajax({
      url: '/latitude',
      type: 'GET',
      success: function(data) {
          $('#lat').html(data);
      }
  });

  $.ajax({
      url: '/longitude',
      type: 'GET',
      success: function(data) {
          $('#lon').html(data);
      }
  });
}

$(document).ready(function() {
  getData();
  setInterval(getData, 5000); // Call getData() every 10 seconds
});

function sendControls(data) {
    // Send the AJAX request to the server
    $.ajax({
        type: 'POST',
        url: '/control',
        data: data,
        success: function (response) {
            // Update the message on the webpage
            $('#message').html(response);
        }
    });
}
// Bind event listeners to the control buttons
$('#up').on('mousedown', function () {
    sendControls({ 'up': 1 });
}).on('mouseup', function () {
    sendControls({ 'up': 0 });
});

$('#down').on('mousedown', function () {
    sendControls({ 'down': 1 });
}).on('mouseup', function () {
    sendControls({ 'down': 0 });
});

$('#left').on('mousedown', function () {
    sendControls({ 'left': 1 });
}).on('mouseup', function () {
    sendControls({ 'left': 0 });
});

$('#right').on('mousedown', function () {
    sendControls({ 'right': 1 });
}).on('mouseup', function () {
    sendControls({ 'right': 0 });
});
// ------------------------------------------------------input control code --------------------------
//------------------------------------------------------video controlling code starts ------------------
  var video = document.querySelector('#video');
  var stream = new MediaSource();
  var sourceBuffer = null;

  stream.addEventListener('sourceopen', function() {
    sourceBuffer = stream.addSourceBuffer('video/mp4; codecs="avc1.42E01E"');
  });

  video.src = window.URL.createObjectURL(stream);

  fetch('/video_feed')
    .then(function(response) {
      return response.body;
    })
    .then(function(body) {
      var reader = body.getReader();
      function read() {
        reader.read().then(function(result) {
          if (result.done) {
            return;
          }
          sourceBuffer.appendBuffer(result.value.buffer);
          read();
        });
      }
      read();
    });
    //-------------------------------------------------------------
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
      console.log('Connected to server');
    });
    socket.on('disconnect', function() {
      console.log('Disconnected from server');
    });
    socket.on('frame', function(data) {
      var canvas = document.getElementById('video-canvas');
      var context = canvas.getContext('2d');
      var img = new Image();
      img.onload = function() {
        context.drawImage(img, 0, 0);
      };
      img.src = 'data:image/jpeg;base64,' + data;
    });

   