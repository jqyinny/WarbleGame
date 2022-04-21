var player_id;
// var player_name; TODO

$(document).ready(function () {
    // TODO add cookie when already logged in
    prelobby();

});

function prelobby() {

    $('#prelobby_modal_background').show();

    $("#join_room_form").submit(function (event) {
        event.preventDefault();
        var room_code = $('#room_code').val();
        if(!room_code){
            $("#prelobby_error").text('Please enter the room code.');
        }else{
            $('#prelobby_modal_background').hide();
            enter_name(room_code);
        }

    });
    
    $("#create_room_form").submit(function (event) {
        event.preventDefault();
        $('#prelobby_modal_background').hide();
        enter_name();
    });
}

function enter_name(room_code) {
    $('#name_modal_background').show();
    $("#name_form").submit(function (event) {
        event.preventDefault();
        var player_name = $('#player_name').val();
        if (!player_name) {
            $("#name_error").text('Please select a player name.');
        } else if (player_name.length > 10) {
            $("#name_error").text('Player name must contain less than 10 characters.');
        }else{
            socket = io.connect('//' + document.domain + ':' + location.port);
            socket.emit('add_player', player_name, room_code);
            $('#name_modal_background').hide();
            socket.on('add_player_to_list', add_player_to_list);
            lobby();
        }
    });
    
}

function lobby() {
    $('#lobby_modal_background').show();
    
    // Start game.
    $("#lobby_form").submit(function (event) {
        event.preventDefault();
        socket = io.connect('//' + document.domain + ':' + location.port);

        socket.emit('start_game', player_id);
        $('#lobby_modal_background').hide();
        socket.on('start_player_turn', start_player_turn);
        console.log("HI");
        socket.on('start_round', start_round);
    });
}

// Called by server after round starts.
function start_player_turn(data) {
    console.log("SPENCER");
    $('#game_modal_background').show();
    console.log("SPENCER");
    options = data["choices"]
    document.getElementById("Option1").value = options[0]
    document.getElementById("Option2").value = options[1]
    document.getElementById("Option3").value = options[2]

    $("input").click(function() {
        var fired_button = $(this).val();
        alert(fired_button);
    });
}

function start_round(data) {
    console.log("CHUCK")

}

function select_word(element){
    console.log("SPENCER");
    // socket = io.connect('//' + document.domain + ':' + location.port);
    // socket.emit('select_word', element.val);
    // $("#choosen_word").text(element.val);
}


// Called by server after successful player name added.
function add_player_to_list(data){
    player_id = data["room_code"]
    let list = document.getElementById("player_list");
    list.innerHTML="";
    for (const player_name in data["player_name"]) {
        let li = document.createElement("li");
        li.innerText = data["player_name"][player_name];
        list.appendChild(li);
    }
}
