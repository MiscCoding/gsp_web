$(function() {
		
	/*wid();
	$(window).resize(function(){
			wid();
	});

	function wid(){
		var windowWidth = $(window).innerWidth();
		console.log(windowWidth);
		if(windowWidth < 1000) {
			$(document).ready(function(){
				$("#wrapper").addClass("enlarged");
			});
					
		} else {
			$(document).ready(function(){
				$("#wrapper").removeClass("enlarged");
			});		

		}
	}*/

	$(document).ready(function(){ 
		setTimeout(function(){
		$(".footable-page-arrow:eq(0)").addClass("paging01");
		$(".footable-page-arrow:eq(1)").addClass("paging02");
		$(".footable-page-arrow:eq(2)").addClass("paging03");
		$(".footable-page-arrow:eq(3)").addClass("paging04");
		},100);
	});

});


