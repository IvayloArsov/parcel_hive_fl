$(document).ready(function() {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('WebSocket connected!');
    });

    $(document).mousemove(function(event) {
        const x = event.pageX;
        const y = event.pageY;
        socket.emit('mouse_event', { x: x, y: y, click: false });
    });

    $(document).mousedown(function(event) {
        if (event.which === 1) {
            //added to make sure that left button is clicked
            //was having issues without this part before that
            const x = event.pageX;
            const y = event.pageY;
            socket.emit('mouse_event', { x: x, y: y, click: true });
        }
    });

    socket.on('mouse_response', function(msg) {
        $('#status').text('Mouse Coordinates: (' + msg.x + ', ' + msg.y + ')');
        if (msg.image_path) {
            $('#captured-image').attr('src', msg.image_path).show();
        }
    });

    socket.on('serial_data', function(msg) {
        console.log('Serial Data:', msg.data);
    });
});
