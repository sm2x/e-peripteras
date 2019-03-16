var theTemplateScript = $("#orders-items").html();

var audio = new Audio('https://e-peripteras.gr/static/js/go.mp3');

var currentPage = 0;
var numPerPage = 15;
var ajaxNotRuning=true;
var kiosk_id = $('#kiosk_id').val();
var query = "/managers/api/orders/all/?kiosk_id="+kiosk_id

var tid = setInterval(send_query, 10000);
// 10sec

function send_query(url, init){
	if (url===undefined) {
		url = query
	}
	if (ajaxNotRuning) {
		console.log('query sent')
		ajaxNotRuning=false;
		$('#loading').css({'display':'block'});
		$("#holder").css({'display':'none'});
		$.ajax({
				url: url,
				success: function(data) {
					// Compile the template
					var theTemplate = Handlebars.compile(theTemplateScript);
					var context = {
						orders:data
					}
					var theCompiledHtml = theTemplate(context);
					$("#order-ajax").html(theCompiledHtml);
					paginate();

					if (init==1) {
						localStorage.setItem("orders_cnt", data.length);
					}

					if (data.length > 0 ) {
						// console.log(localStorage.getItem("orders_cnt") )
						if (localStorage.getItem("orders_cnt") < data.length){
							localStorage.setItem("orders_cnt", data.length);
							audio.play();

						}

						$('title').html('('+data.length+') Διαχείρηση περιπτέρου')
					}
					else{
						$('title').html('Διαχείρηση περιπτέρου')
					}
					query = "/managers/api/orders/all/?kiosk_id="+kiosk_id; //clean the query after success
					ajaxNotRuning=true;
				}
		});
	}
}

function paginate(){
    $('.paginated').each(function() {

	    
	    var $table = $(this);
	    $table.bind('repaginate', function() {
	        $table.find('.row').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
	    });
	    $table.trigger('repaginate');
	    var numRows = $table.find('.row').length;
	    var numPages = Math.ceil(numRows / numPerPage);
	    var $pager = $('<div class="pager"></div>');
	    for (var page = 0; page < numPages; page++) {
	        $('<span class="page-number"></span>').text(page + 1).bind('click', {
	            newPage: page
	        }, function(event) {
	            currentPage = event.data['newPage'];
	            $table.trigger('repaginate');
	            $(this).addClass('active').siblings().removeClass('active');
	            $(this).addClass('visible');
	        }).appendTo($pager).addClass('clickable');
	    }
	    $('.pager').fadeOut().remove();
	    $pager.fadeIn().insertAfter($table).find('span.page-number:first').addClass('active');
  });
}

$(document).ready(function() {
	
	send_query(query, 1);	
	

});

Handlebars.registerHelper('times', function(n, block) {
    var accum = '';
    for(var i = 1; i <= n; ++i)
        accum += block.fn(i);
    return accum;
});

Handlebars.registerHelper("math", function(lvalue, operator, rvalue, options) {
    lvalue = parseFloat(lvalue);
    rvalue = parseFloat(rvalue);
        
    return {
        "+": lvalue + rvalue,
        "-": lvalue - rvalue,
        "*": lvalue * rvalue,
        "/": lvalue / rvalue,
        "%": lvalue % rvalue
    }[operator];
});