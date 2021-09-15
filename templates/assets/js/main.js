function responsiveCollapseView() {
    let desktopView = $(document).width();
    if(desktopView >= "1200"){
        $('.show-xl, .show-lg, .show-md, .show-sm').addClass('show')
    }
    else if(desktopView >= "992"){
        $('.show-lg, .show-md, .show-sm').addClass('show')
        $('.show-xl').removeClass('show')
    }
    else if(desktopView >= "768"){
        $('.show-md, .show-sm').addClass('show')
        $('.show-lg, .show-xl').removeClass('show')
    }
    else if(desktopView >= "576"){
        $('.show-sm').addClass('show')
        $('.show-xl, .show-lg, .show-md').removeClass('show')
    }
    else {
        $('.show-xl, .show-lg, .show-md, .show-sm').removeClass('show')
    }
}
$(function() {
    responsiveCollapseView();
    $(window).resize(function () {
        responsiveCollapseView()
    })

});

  $('.overlay').click(function(){
    $('#sidebar').removeClass('show');
   });
   $('.nav-link').on('click', (evt) => {
   console.log(evt.target)
   $('.nav-link').removeClass('active');
   evt.target.classList.add('active');
   console.log('done');
   
  
 }); 
 