function showFlashMessage(message){
		var template = "{% include 'alert.html' with message='" + message + "' %}"
		console.log(template)
		$("body").append(template);
		$(".container-alert-flash").fadeIn();
		setTimeout(function(){
			$(".container-alert-flash").fadeOut();
		}, 2000)
} // End of showFlashMessage