var ajaxNotRuning=true;

$(document).ready(function() {
	
// // this is the id of the form
// $("#loginForm").submit(function(e) {
// 	if (ajaxNotRuning) {
// 		ajaxNotRuning=false;
// 	$.ajax({
// 			type: "POST",
// 			url: '/login/',
// 			data: $("#loginForm").serialize(), // serializes the form's elements.
// 			success: function(data){
// 				console.log(data); 
// 				if (data.result=="success") {
// 					$('#loginCoolMsg').removeClass("hide");
// 					setTimeout(function(){
// 						$('#loginCoolMsg').addClass("hide");
// 						// location.reload();
// 						// window.location.replace('/second-step/');
// 					}, 900);
// 				}
// 				else {
// 					$('#loginErrorMsg').removeClass("hide");
// 					setTimeout(function(){
// 						$('#loginErrorMsg').addClass("hide");
// 						location.reload();
// 					}, 1000);
// 				}
// 			}
// 		});
// 	}

// 	e.preventDefault(); // avoid to execute the actual submit of the form.
// });

// this is the id of the form
$("#registerForm").submit(function(e) {

	$.ajax({
			type: "POST",
			url: '/register/',
			data: $("#registerForm").serialize(), // serializes the form's elements.
			success: function(data){
				console.log(data); 
				if (data.result=="success") {
					$('#registerCoolMsg').removeClass("hide");
					setTimeout(function(){
						$('#registerCoolMsg').addClass("hide");
					}, 3000);
				}
				else {
					$('#registerErrorMsg').removeClass("hide");
					setTimeout(function(){
						$('#registerErrorMsg').addClass("hide");
					}, 3000);
				}
			}
		});

	e.preventDefault(); // avoid to execute the actual submit of the form.
});



}); //$(document).ready(