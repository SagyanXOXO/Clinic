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