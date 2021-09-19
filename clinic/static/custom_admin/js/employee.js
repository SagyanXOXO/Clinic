// Render the user and job-title foreign key
var users = [];

$.ajax({
    url : "/custom_admin/employee_admin/",
    dataType : 'json',
    success : function(data)
    {
        render_page(data);
    }
});

render_page = (data) => {
    select = document.getElementById('user');
    select2 = document.getElementById('job');
    for (u in data.User)
    {
        var opt = document.createElement('option');
        opt.value = data.User[u].username;
        opt.innerHTML = data.User[u].username;
        select.appendChild(opt);
    }
    for (j in data.Job)
    {
        var opt = document.createElement('option');
        opt.value = data.Job[u].title;
        opt.innerHTML = data.Job[u].title;
        select2.appendChild(opt);
    }
}