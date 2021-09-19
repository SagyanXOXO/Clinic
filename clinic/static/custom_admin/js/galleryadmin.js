// A $( document ).ready() block.
var pre = [];
var sure = 0;
var thisbtn;
var classindex;

var sure_delete = ()=>{
    sure = 1;
    $('.iui-close')[classindex].click();
}

var dont_delete = ()=>{
    sure = 2;
    //$('.iui-close')[classindex].click();

}


// Necessary function definitions
var referesh = ()=>{
    // Destroy previous listeners
    $('.uploaded-image').off();
    $('.iui-close').off();

    // Open the image in new tab when clicked
   $('.uploaded-image').on('click', function(e){
    full = ($('img', this).attr('src'));
    window.open(full);
   })

   // Are you sure you want to delete this image
   $('.iui-close').on('click', function(event){
       thisbtn = this.className;
       classindex = $('.iui-close').index($(this));
       // Show modal
       if (sure == 0)
       {
        $('#sureModal').modal('show');
        console.log('modal opened');
        //event.stopImmediatePropagation();
        return false; 
       }
       // Dont Delete
       if (sure == 2)
       {
        console.log('Not deleting')
        sure = 0;
        //event.stopImmediatePropagation();
        return false;
       }
       // Delete
       if (sure == 1){
        sure = 0;
        console.log('deleting ...')
        return true;
       }
   });
}




$( document ).ready(function() {
   srcs =  $('.input-images')[0].dataset;
   for (var s in srcs)
   {
       pre.push({'id' : s, 'src' : srcs[s]})
   }

   $('.input-images').imageUploader({
    extensions: ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    mimes: ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml'],
    maxSize: undefined,
    maxFiles: undefined,
    imagesInputName:'my_pictures',
    preloaded : pre,
  })

  referesh();

  // When mouseover the image-uplaoder div, referesh listeners to newly added images
  $('.input-images').on('mouseover', function(e){
    referesh();
  })

  // When submit btn pressed, find which submit button and send action accordingly.
  save_arr = ['#save-btn','#save-add-btn','#save-continue-btn','#delete-btn'];
  pre_img = [];
  prepre = {'images':[]};
  for (let i = 0; i < save_arr.length; i++)
  {
    $(save_arr[i]).on('click', function(e)
    {
        e.preventDefault();

        // Get the remaining preloaded images and add to the hidden input to send
        prev = $('.uploaded-image');
        for (let i = 0; i < prev.length; i++)
        {
            if (prev[i].getAttribute('data-preloaded') == 'true')
            {
                prev_imgs = (prev[i].getElementsByTagName('img'));
                for (let j = 0; j < prev_imgs.length; j++)
                {
                    pre_img.push(prev_imgs[j].getAttribute('src'));
                }
            }
        }

        prepre.images = pre_img
        
        $('#pre-images').attr('value', JSON.stringify(prepre));
        newval = save_arr[i].replace('#','');
        $('#action-input').attr('value', (newval));

        // Check if any required input is empty
        var req_input = $('.req-input');
        for (let i = 0; i < req_input.length; i ++)
        {
            if (req_input[i].value == '')
            {
                e.preventDefault();
                req_input[i].style.border = '2px solid red';
                req_input[i].focus();
                sd = $('.small-div');
                for (let i = 0; i < sd.length; i ++)
                {
                    sd[i].style.display = 'flex';
                }
            }
            else{
                $('#gallery-form').submit();
            }
        }

      

    })
  }
});


  



