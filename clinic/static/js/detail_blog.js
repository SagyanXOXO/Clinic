var comment_renderer =()=>{
    $('.comment-thread').remove();
    // Fetch requests and render the comments
    $.ajax({
        type : 'GET',
        data : 'comments',
        success : function(data)
        {
            data = (JSON.parse(data.comments));
            for (d in data.comments)
            {
                comment_constructor(data.comments[d]);
            }
            referesh_listeners();
        }
    });
    
}

// Dynamic nested comment constructor
var comment_constructor = (data)=>{
    var cd = $('.comment-div');

    var main_classname = "comment-thread";
    if (data.parent_id == 0)
    {
        main_classname = main_classname.concat(" ");
        main_classname = main_classname.concat("root-comment");

    }
    else{
        main_classname = main_classname.concat(" ");
        main_classname = main_classname.concat("is-child");
    }

    if (data.reply_count != 0)
    {
        main_classname = main_classname.concat(' ');
        main_classname = main_classname.concat('has-child');
    }

    // Comment Thread div
    var cth = $('<div></div>').addClass(main_classname);
    cth.attr('id',data.id);

    // Comment Wrapper div
    var cw = $('<div></div>').addClass('comment-wrapper');

    var cpic = $('<img>').addClass('commenter-pic');
    cpic.attr('src', 'http://wpthemesgrid.com/themes/medikit/img/author1.jpg');
    cw.append(cpic);

    // Comment Content
    var cc = $('<div></div>').addClass('comment-content');
    cc.append($('<p></p>').addClass('commenter').text(data.name));
    var ct = $('<div></div>').addClass('comment-time');
    ct.append($('<i></i>').addClass('far fa-calendar-alt'));
    ct.append($('<p></p>').text(data.time));
    cc.append(ct);

    mc = $('<p></p>').addClass('main-comment').text(data.comment);
    cc.append(mc);

    ci = $('<div></div>').addClass('comment-interaction');
    if (data.has_liked == 1)
    {
        i1 = $('<i></i>').addClass('fas fa-heart fa-lg');
        i2 = $('<i></i>').addClass('far fa-heart fa-lg heart-remove');
    }
    else{
        i1 = $('<i></i>').addClass('fas fa-heart fa-lg heart-remove');
        i2 = $('<i></i>').addClass('far fa-heart fa-lg');
    }
    i1.attr('data-action','Like');
    i1.attr('data-parent','Comment');
    i1.attr('data-action-id',data.id);
    i2.attr('data-action','Like');
    i2.attr('data-parent','Comment');
    i2.attr('data-action-id',data.id);
    i3 = $('<i></i>').addClass('far fa-comment fa-lg');
    i3.attr('data-action','Comment');
    i3.attr('data-parent','Comment');
    i3.attr('data-action-id',data.id);
    p1 = $('<p></p>').text(data.time);
    p2 = $('<p></p>').text(data.likes + ' likes');
    ci.append(i1,i2,i3,p1,p2);
    cc.append(ci);

    cw.append(cc);
    cth.append(cw);
    if (data.parent_id)
    {
        _id = '#' + data.parent_id.toString();
        $(_id).append(cth);
    }
    else{
        cd.append(cth);
    }
}

var referesh_listeners = ()=>{
    // Get the csrf token
    var csrftoken = getCookie('csrftoken');

    // handle JSON POST for likes and dislikes
    $('.fa-heart').on('click', function(){
        console.log('clicked');
        let heart =$(this);
        $.ajax({
            datatype : 'json',
            method : 'POST',
            data : {
                action : $(this).attr('data-action'),
                id : $(this).attr('data-action-id'),
                parent : $(this).attr('data-parent'),
                csrfmiddlewaretoken : csrftoken,
            },
            success : function(data)
            {
                heart.siblings('.heart-remove').removeClass('heart-remove');
                heart.addClass('heart-remove');
                if (heart.attr('data-parent') == 'Comment')
                {
                    comment_renderer();
                }
            }
        });
    });

    // Handle Comment Post via AJAX
    $('#comment-post').one('click',function(){
        console.log('clicked');
        
        comment = $('#comment-textarea').val();
    
        $.ajax({
            datatype : 'json',
            method : 'POST',
            data : {
                action : _action,
                id : _id,
                parent : _parent,
                comment : comment,
                csrfmiddlewaretoken : csrftoken,
            },
            success : function(data)
            {
                //comment_constructor();
                //console.log('working');
                // Close the modal
                // Clear the input textarea of the comment section
                $('#comment-modal').modal('hide');
                $('#comment-textarea').val('');
                alert(data.message);
                comment_renderer();

            }
            
        });
    });

    // Show Comment Modal
    $('.fa-comment').one('click',function(){
        _action = $(this).attr('data-action');
        _id = $(this).attr('data-action-id');
        _parent = $(this).attr('data-parent');

        $('#comment-modal').modal('show');
    });
}

$(document).ready(function(){

    comment_renderer();

});