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

$(document).ready(function(){
    $('.mask').fadeOut(); 
    $('.loader').fadeOut();
    document.getElementById('preloader').classList.add('preloader-fade');

    navbar = document.getElementById('bottom-part');
    sticky = (navbar.offsetTop);

    window.onscroll = function(){
        addsticky();
    }

    var addsticky = ()=>{
        if (window.pageYOffset >= sticky)
        {
            navbar.classList.add('sticky');
        }
        else
        {
            navbar.classList.remove('sticky');
        }
    }
})