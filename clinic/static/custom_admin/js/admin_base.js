// This is the base.js which will run everytime 
// Therefore the function to get csrftoken cookie will be placed here so that all other js files can have access
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var notification_toggler = ()=>{
    // On click render toggle the notification dropdown
    $('.notification-icon').on('click', function(){
        let display = ($('.notification-dropdown').css('display'));
        if (display == 'none')
        {
            $('.notification-dropdown').css('display','flex');
        }
        else
        {
            $('.notification-dropdown').css('display', 'none');
        }
    });

    // Remove the dropdown when clicked everywhere except the dropdown
    $(document).click(function(e) {
        if ( $(e.target).closest('.notification-dropdown').length === 0  && $(e.target).closest('.notification-icon').length === 0 ) {
            $('.notification-dropdown').css('display', 'none');
        }
    });
}

var websocket_handler = () => {
    const url = 'ws://' + window.location.host + '/ws/notifications/'

    const socket = new WebSocket(url);

    socket.addEventListener('message', function(e){
        console.log(e);
    });
}    

var notification_render = () => {
    let url = window.location.origin + '/' + 'cadmin/notification/';
    console.log(url);
    $.ajax({
        datatype : 'json',
        method : 'GET',
        url : url,
        data : {
            action : 'get_notification'
        },
        success : function(d)
        {
            data = d.notification;
            for (let i = 0; i < data.length; i++)
            {
                console.log(data[i].fields);
            }
        }
    });
}

$(document).ready(function(){
    notification_toggler();
    websocket_handler();
    notification_render();
});