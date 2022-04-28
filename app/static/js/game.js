var player_id;
var player_name;
var socket = io.connect('//' + document.domain + ':' + location.port);
var room_code;

$(document).ready(function () {
    // TODO add cookie when already logged in
    prelobby();

});

function prelobby() {

    $('#prelobby_modal_background').show();

    $("#join_room_form").submit(function (event) {
        event.preventDefault();
        room_code = $('#room_code').val();
        if(!room_code){
            $("#prelobby_error").text('Please enter the room code.');
        }else{
            $('#prelobby_modal_background').hide();
            enter_name();
        }

    });
    
    $("#create_room_form").submit(function (event) {
        event.preventDefault();
        $('#prelobby_modal_background').hide();
        enter_name();
    });
}

function enter_name() {
    $('#name_modal_background').show();
    $("#name_form").submit(function (event) {
        event.preventDefault();
        player_name = $('#player_name').val();
        if (!player_name) {
            $("#name_error").text('Please select a player name.');
        } else if (player_name.length > 10) {
            $("#name_error").text('Player name must contain less than 10 characters.');
        }else{
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
        socket.emit('start_game', room_code);
    });
    socket.on('start_round', start_round);
}

// Called by server after round starts.
function start_round(data) {
    $('#lobby_modal_background').hide();
    $('#game_modal_background').show();
    current_player = data["current_player"];

    if(current_player == player_name){
        $("#current_player").text("It's your turn!");
        options = data["choices"]
        document.getElementById("Option1").value = options[0]
        document.getElementById("Option2").value = options[1]
        document.getElementById("Option3").value = options[2]

    }else{
        $('#word_options_form').hide();
        $("#current_player").text( data["current_player"] + "'s turn");
    }
    socket.on("choosen_word", choosen_word);
    socket.on("recieve_messages", recieve_messages);
    
    $("#message_form").submit(function(event) {
        event.preventDefault();
        msg = $('#usermsg').val();
        if(msg != "" ){
            console.log("sending msg");
            socket.emit("send_chat", msg, room_code, player_name);
        }
        $('#usermsg').val("");
    });
}

function select_word(option){
    let word = document.getElementById(option).value;
    console.log(word);
    socket.emit("choose_word", word, room_code);
}

function recieve_messages(data){
    // If message is the answer then only display to player.
    let chatbox = document.getElementById("chatbox");
    let li = document.createElement('li');
    li.innerText = data["messenger_name"] + " says " + data["msg"];
    chatbox.appendChild(li);
}

function choosen_word(data){
    if(current_player == player_name){
        $("#choosen_word").text( "Your word: " + data["choosen_word"]);

    }else{
        $("#choosen_word").text( "Guess the word!");
    }
}

// Called by server after successful player name added.
function add_player_to_list(data){
    room_code = data["room_code"];
    let list = document.getElementById("player_list");
    list.innerHTML="";
    for (const other_player_name in data["player_name"]) {
        let li = document.createElement("li");
        li.innerText = data["player_name"][other_player_name];
        list.appendChild(li);
    }
}
