$(document).ready(function() {
    $('body').on('change', 'select#region_dropdown', function() {
        var selected_region = $(this).val();
        if (selected_region == undefined || selected_region == -1 || selected_region == '') {
            $("select#country_dropdown").html("<option>-- Filter by Country --</option>");
        } else {
            var url = "/dataviz/countries_by_region/" + selected_region + "/";
            
            $.getJSON(url, function(countries) {
                var options = "<option>-- Filter by Country --</option>";
                for (var i = 0; i < countries.length; i++) {
                    options += '<option value="' + countries[i].pk + '">' + countries[i].name + '</option>';
                }
                $("select#country_dropdown").html(options);
                $("select#country_dropdown option:first").attr('selected', 'selected'); 
            });
        }
    });

});