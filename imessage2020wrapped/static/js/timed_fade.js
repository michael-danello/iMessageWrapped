$(".fadeMe").hide().each(function(i) {
  var extraDelay = 0
  if (i > 3) {
    extraDelay = 33000;
  }
  $(this).delay(i*10000+extraDelay).fadeIn(0);
});


$(".fadeFast").hide().each(function(i) {
  var delay = 3 * 10000
  $(this).delay(delay+i*3000).fadeIn(1000);
});

$(document).ready(function(){
		$(".shrink").each(function(i){
    	var text_int = .94**i*100
	    var	text_size = text_int.toString().concat("%");
    	$(this).css("font-size", text_size);
    });
});
