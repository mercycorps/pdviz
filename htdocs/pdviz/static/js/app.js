$(document).ready(function() {
    $('body').on('change', 'select#id_region', function() {
        var selected_region = $(this).val();
        if (selected_region == undefined || selected_region == -1 || selected_region == '') {
            $("select#id_country").html("<option value=''>-- Filter by Country --</option>");
        } else {
            var url = "/dataviz/countries_by_region/" + selected_region + "/";
            
            $.getJSON(url, function(countries) {
                var options = "<option value=''>-- Filter by Country --</option>";
                for (var i = 0; i < countries.length; i++) {
                    options += '<option value="' + countries[i].country_id + '">' + countries[i].name + '</option>';
                }
                $("select#id_country").html(options);
                $("select#id_country option:first").attr('selected', 'selected'); 
            });
        }
    });

    $('.dateinput').datepicker({
        dateFormat: 'yy-mm-dd',
    });

});