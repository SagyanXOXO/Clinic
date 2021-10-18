// Function to render toast message
// Icons have four choices Info, Warning, Success and Error
var toaster = (text, background, loaderbg, textColor, transition) =>{
    $.toast({
        text: text,
        loader: true,      
        bgColor : background,  
        loaderBg: loaderbg,
        textColor: textColor,
        showHideTransition: transition,
        allowToastClose: true,
        stack: 4,
        position: 'bottom-left',  
    });
}

var comment_renderer =()=>{
    $('.comment-thread').remove();
    // Fetch requests and render the comments
    $.ajax({
        type : 'GET',
        data : {
            action : 'get_comments'
        },
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

    if (data.has_reply != 0)
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
    if (data.isUserComment == 1)
    {
        p3 = $('<p class = "edit-comment">Edit<p>');
        p3.attr('data-action-id', data.id);
        p3.attr('data-content', data.comment);
        p4 = $('<p class = "delete-comment">Delete</p>');
        p4.attr('data-action-id', data.id);
        ci.append(i1,i2,i3,p1,p2,p3,p4)
    }
    else
    {
        ci.append(i1,i2,i3,p1,p2);
    }
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
    unbinders = ['.fa-heart', '#comment-post', '.fa-comment', '.edit-comment', '#edit-comment-post', '.delete-comment', '#comment-delete']
    for(let i = 0; i < unbinders.length; i++)
    {
        $(unbinders[i]).unbind('click');
    }
    $('.fa-heart').unbind('click');
    $('.comment-post').unbind('click');
    // Get the csrf token
    var csrftoken = getCookie('csrftoken');

    // handle JSON POST for likes and dislikes
    $('.fa-heart').on('click', function(){
        //console.log('clicked');
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
                toaster(data.message, '0D3485', 'F4F4F4', 'white', 'slide');
                get_blog_info();
                heart.siblings('.heart-remove').removeClass('heart-remove');
                heart.addClass('heart-remove');
                if (heart.attr('data-parent') == 'Comment')
                {
                    comment_renderer();
                }
            },
            error : function(data)
            {
                toaster(data.message, 'red', 'F4F4F4', 'white', 'slide');
            }
        });
    });

    // Handle Comment Post via AJAX
    $('#comment-post').on('click',function(){
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
                get_blog_info();
                $('#comment-modal').modal('hide');
                $('#comment-textarea').val('');
                comment_renderer();
                toaster(data.message, 'black', 'F4F4F4', 'white', 'slide');
            },
            error : function(data)
            {
                toaster(data.message, 'red', 'F4F4F4', 'white', 'slide');
            }
        });
    });

    // Show Comment Modal
    $('.fa-comment').on('click',function(){
        _action = $(this).attr('data-action');
        _id = $(this).attr('data-action-id');
        _parent = $(this).attr('data-parent');

        $('#comment-modal').modal('show');
    });

    // Edit Comment
    $('.edit-comment').on('click', function(){
        _action = 'edit-comment';
        _id = $(this).attr('data-action-id');
        content = $(this).attr('data-content');

        $('#edit-comment-textarea').val(content);
        $('#edit-comment-modal').modal('show');
    });

    $('#edit-comment-post').on('click',function(){
        comment = $('#edit-comment-textarea').val();
    
        $.ajax({
            datatype : 'json',
            method : 'POST',
            data : {
                action : _action,
                id : _id,
                comment : comment,
                csrfmiddlewaretoken : csrftoken,
            },
            success : function(data)
            {
                //comment_constructor();
                //console.log('working');
                // Close the modal
                // Clear the input textarea of the comment section
                get_blog_info();
                $('#edit-comment-modal').modal('hide');
                $('#edit-comment-textarea').val('');
                _action = ''
                id = ''
                comment = ''
                comment_renderer();
                toaster(data.message, 'black', 'F4F4F4', 'white', 'slide');
            },
            error : function(data)
            {
                toaster(data.message, 'red', 'F4F4F4', 'white', 'slide');
            }  
        });
    });

    // Delete Comment
    $('.delete-comment').on('click', function(){
        _action = 'delete-comment';
        _id = $(this).attr('data-action-id');
        content = $(this).attr('data-content');
        console.log(content);

        $('#delete-comment-modal').modal('show');
    });

    $('#comment-delete').on('click',function(){
        $.ajax({
            datatype : 'json',
            method : 'POST',
            data : {
                action : _action,
                id : _id,
                csrfmiddlewaretoken : csrftoken,
            },
            success : function(data)
            {
                //comment_constructor();
                //console.log('working');
                // Close the modal
                // Clear the input textarea of the comment section
                get_blog_info();
                $('#delete-comment-modal').modal('hide');
                _action = ''
                id = ''
                comment_renderer();
                toaster(data.message, 'black', 'F4F4F4', 'white', 'slide');
            },
            error : function(data)
            {
                toaster(data.message, 'red', 'F4F4F4', 'white', 'slide');
            }
        });
    });
}

var get_blog_info = () =>{
    $.ajax({
        method : 'GET',
        data : {
            action : 'get_blog_info'
        },
        success(data)
        {
            //console.log(data)
            $('.total_likes').html(data.total_likes + " likes");
            $('.total_comments').html(data.total_comments + " comments");
        }
    })
}

$(document).ready(function(){
    comment_renderer();
});