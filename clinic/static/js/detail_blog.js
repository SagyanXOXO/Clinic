var cd = $('.comment-div');

var comment_constructor = (data)=>{
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
    i1 = $('<i></i>').addClass('fas fa-heart fa-lg');
    i2 = $('<i></i>').addClass('far fa-heart fa-lg');
    i3 = $('<i></i>').addClass('far fa-comment fa-lg');
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

    if (data.replies)
    {
        for (var d in data.replies)
        {
            comment_constructor(data.replies[d]);
        }
    }
}

$.ajax({
    type : 'GET',
    url : '/blog/2',
    data : 'comments',
    success : function(data)
    {
        data = (JSON.parse(data.comments));
        for (d in data.comments)
        {
            comment_constructor(data.comments[d]);
        }
    }
});

$(document).ready(function(){

});