$(document).ready(function() {
	kiosk_init_items();	

	$( '.filter' ).click(function() {
		$('.filter').removeClass('filter-active');
		$(this).addClass('filter-active');
		
		get_items_cat(this.id);	
		
	});

	$( '#filter-online' ).click(function() {
		kiosk_init_items()		
	});


});

var kiosk_id = $('#kiosk_id').val();
var theTemplateScript2nd = $("#kiosk-items").html();

function kiosk_init_items(){


		$.ajax({
				url: '/api/kiosk/items/',
				type: "GET",
				data: {
			        kiosk_id : kiosk_id,
			        online_offer: 1
			    },
			    statusCode: {
					206: function(data) {
						
						console.log(data)
						ajaxNotRuning=true;						
					},
					200: function(data) {

						var theTemplate = Handlebars.compile(theTemplateScript2nd);
						var context = {
							kiosk_items:data,
						}
						var theCompiledHtml = theTemplate(context);
						$("#items-ajax").html(theCompiledHtml);
						ajaxNotRuning=true;

					},
					500: function(data) {
						console.log(data.responseText)
					},
				},
		});
}

function get_items_cat(slug){
	$.ajax({
			url: '/api/kiosk/items/',
			type: "GET",
			data: {
		        kiosk_id : kiosk_id,
		        category__slug: slug
		    },
		    statusCode: {
				206: function(data) {
					console.log(data)						
					ajaxNotRuning=true;
				},
				200: function(data) {
					var theTemplate = Handlebars.compile(theTemplateScript2nd);
					var context = {
						kiosk_items:data,
					}
					var theCompiledHtml = theTemplate(context);
					$("#items-ajax").html(theCompiledHtml);
					ajaxNotRuning=true;
					$('#filter-header').css({'display':'none'});
					

				},
				500: function(data) {
					console.log(data.responseText)
				},
			},
	});
}