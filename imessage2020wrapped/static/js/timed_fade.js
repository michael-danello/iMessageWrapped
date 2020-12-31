$(".fadeMe").hide().each(function(i) {
  var extraDelay = 0
  if (i > 3) {
    extraDelay = 14000;
  }
  $(this).delay(i*8000+extraDelay).fadeIn(0);
});


$(".fadeFast").hide().each(function(i) {
  var delay = 3 * 8000
  $(this).delay(delay+i*2000).fadeIn(1000);
});

$(document).ready(function(){
		$(".shrink").each(function(i){
    	var text_int = .94**i*100
	    var	text_size = text_int.toString().concat("%");
    	$(this).css("font-size", text_size);
    });
});


$(window).on("load",function() {
  $(window).scroll(function() {
    var windowBottom = $(this).scrollTop() + $(this).innerHeight();
    $(".fadeScroll").each(function() {
      /* Check the location of each desired element */
      var objectTop = $(this).offset().top;
      $(this).css("opacity", "0");
      /* If the element is completely within bounds of the window, fade it in */
      if (objectTop < windowBottom) { //object comes into view (scrolling down)
        if ($(this).css("opacity")==0) {$(this).fadeTo(2000,1);}
      };
    });
  }).scroll(); //invoke scroll-handler on page-load
});
