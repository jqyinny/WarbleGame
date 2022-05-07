var player_id;
var player_name;
var socket = io.connect('//' + document.domain + ':' + location.port);
var room_code;

/*--------------------------------------------------------HTML Calls-----------------------------------------------------------*/
$(document).ready(function () {
    // populate submit events
    $("#next_turn_form").submit(function (event) {
        event.preventDefault();
        socket.emit('next_turn', room_code);
    });

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

    $("#join_room_form").submit(function (event) {
        event.preventDefault();
        room_code = $('#room_code_input').val();
        if(!room_code){
            $("#prelobby_error").text('Please enter the room code.');
        }else{
            $('#prelobby_modal_background').hide();
            $('#name_modal_background').show();
        }

    });

    $("#create_room_form").submit(function (event) {
        event.preventDefault();
        $('#prelobby_modal_background').hide();
        $('#name_modal_background').show();
    });

    // Start game.
    $("#lobby_form").submit(function (event) {
        event.preventDefault();
        var dropdown = document.getElementById("wordset_dropdown");
        var selected = dropdown.options[dropdown.selectedIndex].text;
        if($("#player_list").children().length < 2){
            $("#lobby_error").text('You must have at least 2 players to play.');
        }else{
            socket.emit('start_game', room_code, selected);
        }
    });

    $("#message_form").submit(function(event) {
        event.preventDefault();
        msg = $('#usermsg').val();
        if(msg != "" ){
            socket.emit("send_chat", msg, room_code, player_name);
        }
        $('#usermsg').val("");
    });

    $("#play_again_form").submit(function (event) {
        event.preventDefault();
        lobby();
    });

    // TODO add cookie when already logged in
    $('#prelobby_modal_background').show();
});


/*----------------------------------------------Helper Functions----------------------------------------------------*/
function lobby() {
    $('#end_modal_background').hide();
    $('#lobby_modal_background').show();

    socket.emit("get_wordset_set");
    socket.once("populate_wordset_options", populate_wordset_options);
    
    socket.once('start_turn', start_turn);
    socket.once("game_over", game_over);
}

function populate_wordset_options(data) {
    const wordset_json = data["wordset_set"];
    let wordset_options = document.getElementById('wordset_dropdown');
    console.log(wordset_json);
    for (let i = 0; i < wordset_json.length; ++i) {
        let wordset_option=document.createElement('option');
        wordset_option.value = wordset_json[i];
        wordset_option.innerHTML = wordset_json[i];   // Use innerHTML to set the text
        wordset_options.appendChild(wordset_option);                                 
    }
}

/*----------------------------------------------Onclick Calls----------------------------------------------------*/
// Onclick from html word options
function select_word(option){
    let word = document.getElementById(option).value;
    socket.emit("choose_word", word, room_code);
}

/*----------------------------------------------Server Calls----------------------------------------------------*/
// Called by server after turn starts.
function start_turn(data) {
    $('#lobby_modal_background').hide();
    $('#score_modal_background').hide();
    $('#game_modal_background').show();
    
    // reset turn
    $('#word_options_form').show();
    $("#choosen_word").text( "");
    let list = document.getElementById("chatbox");
    list.innerHTML="";

    current_player = data["current_player"];
    $("#round_num").text("Round " + data["round_num"] + " out of " + data["total_num_rounds"]);

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
    socket.once("choosen_word", choosen_word);
    socket.on("recieve_messages", recieve_messages);
    
}

function recieve_messages(data){
    // If message is the answer then only display to player.
    let chatbox = document.getElementById("chatbox");
    let li = document.createElement('li');
    
    if(data["points"] == 0){
        li.innerText = data["messenger_name"] + " says " + data["msg"];
    }else{
        li.innerText = data["messenger_name"] + " got the answer!";
    }
    chatbox.appendChild(li);
}

function choosen_word(data){
    $('#word_options_form').hide();
    if(current_player == player_name){
        $("#choosen_word").text( "Your word: " + data["choosen_word"]);

    }else{
        $("#choosen_word").text( "Guess the word!");
    }
    socket.once("turn_over", turn_over);
}

// Called by server after successful player name added.
function add_player_to_list(data){
    room_code = data["room_code"];
    $("#room_code").text("Room Code: "+ room_code);
    let list = document.getElementById("player_list");
    list.innerHTML="";
    for (const other_player_name in data["player_name"]) {
        let li = document.createElement("li");
        li.innerText = data["player_name"][other_player_name];
        list.appendChild(li);
    }
}

// Called by server after turn end conditions.
function turn_over(data){
    $('#game_modal_background').hide();
    $('#score_modal_background').show();
    let player_names = data["player_names"];
    let scores = data["scores"];
    let list = document.getElementById("player_score_list");
    list.innerHTML="";
    for (let i = 0; i < player_names.length; i++) {
        let li = document.createElement("li");
        li.innerText = player_names[i] + ": " + scores[i];
        list.appendChild(li);
    }
    socket.once("start_turn", start_turn);
    socket.off("recieve_messages", recieve_messages);
}

// Called by server after last turn ends.
function game_over(data){
    $('#score_modal_background').hide();
    $('#end_modal_background').show();

    let player_names = data["player_names"];
    let scores = data["scores"];
    let list = document.getElementById("player_end_list");
    list.innerHTML="";
    for (let i = 0; i < player_names.length; i++) {
        let li = document.createElement("li");
        li.innerText = player_names[i] + ": " + scores[i];
        list.appendChild(li);
    }
    
    $("#winner").text( data["winner"] + " Wins!");
}