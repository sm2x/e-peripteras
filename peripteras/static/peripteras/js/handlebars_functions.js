var theTemplateScript = $("#kiosks").html();



var query = "/api/kiosks/?format=json"
var currentPage = 0;
var numPerPage = 15;
var ajaxNotRuning=true;

function send_query(url){
	if (ajaxNotRuning) {
		ajaxNotRuning=false;
		$('#loading').css({'display':'block'});
		$("#holder").css({'display':'none'});
		$.ajax({
				url: url,
				success: function(data) {
					// Compile the template
					var theTemplate = Handlebars.compile(theTemplateScript);
					var context = {
						kiosks:data
					}
					var theCompiledHtml = theTemplate(context);
					$("#holder").html(theCompiledHtml);
					$('#loading').css({'display':'none'});
					$("#holder").css({'display':'block'});
					paginate();
					query = "/api/kiosks/?format=json"; //clean the query after success
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
	    var $pager = $('<div class="pager col-lg-12"></div>');
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
	
	send_query(query);
});

Handlebars.registerHelper('times', function(n, block) {
    var accum = '';
    for(var i = 1; i <= n; ++i)
        accum += block.fn(i);
    return accum;
});