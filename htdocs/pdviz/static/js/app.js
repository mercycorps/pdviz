$(document).ready(function() {
    $('body').on('change', 'select#id_region', function() {
        var selected_region = $(this).val();
        var url ;
        if (selected_region == undefined || selected_region == -1 || selected_region == '') {
            url = '/api/v1/countries/';
        } else {
            url = "/dataviz/countries_by_region/" + selected_region + "/";
        }    
		$.getJSON(url, function(countries) {
			var options = "<option value=''>-- Filter by Country --</option>";
			for (var i = 0; i < countries.length; i++) {
				options += '<option value="' + countries[i].country_id + '">' + countries[i].name + '</option>';
			}
			$("select#id_country").html(options);
			$("select#id_country option:first").attr('selected', 'selected'); 
		});
        
    });

    $('.dateinput').datepicker({
        dateFormat: 'yy-mm-dd',
    });

});

function createAlert (type, message) {
    $("#alerts").append(
        $(
            "<div class='alert alert-" + type + " alert-dismissable'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<p>" + message + "</p>" +
            "</div>"
        )
    );
    // Remove the alert after 30 seconds if the user does not close it.
    $(".dynamic-alert").delay(300000).fadeOut("slow", function () { $(this).remove(); });
}