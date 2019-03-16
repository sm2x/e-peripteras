var ajaxNotRuning=true;
var kiosk_id = $('#kiosk_id').val();

$(document).ready(function() {
	update_basket();

	$( '.add-to-basket' ).click(function() {
		var item = {
				item_id : $(this).attr('id'),
				csrf 	: $('#csrf').val(),
		}
		send_data(item);
	});


	// $( 'i' ).click(function() {
	// 	console.log('ok')
	// 	// var item = {
	// 	// 		item_id : $(this).attr('data-add'),
	// 	// 		csrf 	: $('#csrf').val(),
	// 	// }
	// 	// var curent = $(this).html();
	// 	// $(this).html(curent + 1)
	// 	// send_data(item);
	// });

	

});

function plus_to_basket(id) {
	var item = {
			item_id : id,
			csrf 	: $('#csrf').val(),
	}
	send_data(item);

}

function remove_from_basket(id) {
	var item = {
			item_id : id,
			csrf 	: $('#csrf').val(),
	}
	send_to_remove_data(item);

}


function is_empty(field) {
	if (field === "undefined" || field==='' || field===' ' || field===false) {
		return true;
	}
	return false;
}


function send_data(data){
	if (ajaxNotRuning) {
		ajaxNotRuning=false;

		console.log(data)

		$.ajax({
				url: '/user/api/basket/add/?format=json',
				type: "GET",
			    data: {
			        item_id : data.item_id,
			        kiosk_id: kiosk_id,
			        csrfmiddlewaretoken : data.csrf
			    },
			    statusCode: {
					206: function(data) {
						
						console.log(data)						
						ajaxNotRuning=true;
					},
					200: function(data) {

						$('#msg').slideToggle().html(data.msg);

						setTimeout(function(){
							$('#msg').slideToggle();
						}, 2000);

						ajaxNotRuning=true;
						update_basket()
					},
					500: function(data) {
						console.log(data.responseText)
					},
				},
		});
	}
}

function send_to_remove_data(data){
	if (ajaxNotRuning) {
		ajaxNotRuning=false;

		console.log("removing from basket")

		$.ajax({
				url: '/user/api/basket/remove/?format=json',
				type: "GET",
			    data: {
			        item_id : data.item_id,
			        kiosk_id: kiosk_id,
			        csrfmiddlewaretoken : data.csrf
			    },
			    statusCode: {
					206: function(data) {
						
						console.log(data)						
						ajaxNotRuning=true;
					},
					200: function(data) {

						$('#msg').slideToggle().html(data.msg);

						setTimeout(function(){
							$('#msg').slideToggle();
						}, 2000);

						ajaxNotRuning=true;
						update_basket()
					},
					500: function(data) {
						console.log(data.responseText)
					},
				},
		});
	}
}

var theTemplateScript = $("#items").html();
function update_basket(){

	if (ajaxNotRuning) {
		ajaxNotRuning=false;

		$.ajax({
				url: '/user/api/basket/get/?format=json',
				type: "GET",
				data: {
			        kiosk_id : kiosk_id,
			    },
			    statusCode: {
					206: function(data) {
						
						console.log(data)						
						ajaxNotRuning=true;
					},
					200: function(data) {
						console.log(data)
						var sum = 0

						$.each(data, function (index, obj) {
							sum = sum + (obj.price * obj.times);
						});

						console.log(sum)

						$(".basket").css({"display":"none"});
						$("#basket-ajax").css({"display":"block"});

						var theTemplate = Handlebars.compile(theTemplateScript);
						var context = {
							items:data,
							total_sum:sum.toFixed(2)
						}
						var theCompiledHtml = theTemplate(context);
						$("#basket-ajax").html(theCompiledHtml);

						ajaxNotRuning=true;
					},
					500: function(data) {
						console.log(data.responseText)
					},
				},
		});
	}
}