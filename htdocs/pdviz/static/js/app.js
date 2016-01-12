var $loading = $('#loading');

/* 
 * A global ajaxComplete method that shows you any messages that are set in Django's view
 */
$( document )
    .ajaxStart( function() {
        $loading.show();
    })
    .ajaxStop( function() {
        $loading.hide();
    })
    .ajaxComplete(function(e, xhr, settings) {
        var contentType = xhr.getResponseHeader("Content-Type");
        if (contentType == "application/javascript" || contentType == "application/json") {
            var json = $.parseJSON(xhr.responseText);
            show_django_ajax_messages(json);
        }
    })
    .ajaxError(function(e, xhr, settings, thrownError) {
        createAlert("danger", "Error " + xhr.status + ": " +  thrownError, false);
    });


function show_django_ajax_messages(json, whereToAppend) {
    if (json.error != undefined) {
        $.each(json.django_messages, function (i, item) {
            createAlert(item.extra_tags, item.message, true, whereToAppend);
        });
    }
}

$(document).ready(function() {

    $("#id_region").select2({ placeholder: "Region", allowClear: true });
    $("#id_country").select2({ placeholder: "Country", allowClear: true });
    $("#id_donor").select2({ placeholder: "Donor", allowClear: true });
    $("#id_sector").select2({placeholder: "Sector", allowClear: true,});
    $("#id_subsector").select2({placeholder: "Area of Focus", allowClear: true,});
    $("#id_theme").select2({placeholder: 'Theme', allowClear: true,});
    $("#id_methodology").select2({placeholder: 'Methodology', allowClear: true,});
    $("#id_status").select2({  placeholder: "Status", allowClear: true });
    
    $('.dateinput').datepicker({  dateFormat: 'yy-mm-dd', });

});

$('body').on('change', 'select#id_region', function() {
    var selected_region = $(this).val();
    var url = '/api/v1/countries/';
    if (selected_region != undefined && selected_region != -1 && selected_region != '' && selected_region != 0) {
       url = url + '?region=' + selected_region;
    }
    $.getJSON(url, function(countries) {
        var options = "";
        for (var i = 0; i < countries.length; i++) {
            options += '<option value="' + countries[i].country_id + '">' + countries[i].name + '</option>';
        }

        $("select#id_country").html(options);
        $("select#id_country").val('').trigger("change");
    });
});

$('body').on('change', 'select#id_sector', function() {
    var selected_sector = $(this).val();
    var url = '/api/v1/subsector/';
    if (selected_sector != undefined && selected_sector != -1 && selected_sector != '' && selected_sector != 0) {
        url = url + '?sector=' + selected_sector;
    }
    $.getJSON(url, function(subsectors) {
        var options = "<option value=''></option>";
        for (var i = 0; i < subsectors.length; i++) {
            options += '<option value="' + subsectors[i].subsector_id + '">' + subsectors[i].name + '</option>';
        }
        $('select#id_subsector').html(options);
        $("select#id_subsector").val('').trigger("change");
    });
});

function createAlert (type, message, fade) {
    $("#alerts").append(
        $(
            "<div class='alert dynamic-alert alert-" + type + " alert-dismissable'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<p>" + message + "</p>" +
            "</div>"
        )
    );
    if (fade == true) {
        // Remove the alert after 30 seconds if the user does not close it.
        $(".dynamic-alert").delay(3000).fadeOut("slow", function () { $(this).remove(); });
    }
}

       
var tableObject = function (json) {
    var headerCount = new Object();

    var createTHEAD = function () {
        var thead = document.createElement('thead');
        return thead;
    }

    var createTBODY = function () {
        var tbody = document.createElement('tbody');
        return tbody;
    }

    var createTR = function (id) {
        var tr = document.createElement("tr");
        tr.ID = id;
        return tr;
    };

    var createTH = function (html) {
        var th = document.createElement("th");
        th.innerHTML = html;
        return th;
    };

    var createTD = function (html) {
        var td = document.createElement("td");
        td.innerHTML = html;
        return td;
    };

    var getName = function (id) {
        for (var name in headerCount) {
            if (eval("headerCount." + name) == id) {
                return name;
            }
        }
    };
    var data = json.slice();
    //data.forEach(function(v){ delete v.drilldown });
    var pTable;
    if (data.length > 0) {
        var index = 0;
        pTable = document.createElement("table");
        var thead = createTHEAD();
        var head = createTR();
        for (var i = 0; i < data.length; i++) {
            for (var item in data[i]) {
                if (item == 'drilldown'  || item == 'y') { continue };
                if (!headerCount.hasOwnProperty(item)) {
                    head.appendChild(createTH(item));
                    eval('headerCount.' + item + "=" + index);
                    index++;
                }
            }
        }
        thead.appendChild(head);
        pTable.appendChild(thead);
        var tbody = createTBODY();
        for (var i = 0; i < data.length; i++) {
            var row = new createTR(i);
            for (var j = 0; j < index; j++) {
                var name = getName(j);
                if (eval("data[" + i + "].hasOwnProperty('" + name + "')")) {
                    var cell_value = eval('data[' + i + '].' + name);
                    if (name == 'gait_id') {
                        cell_value = "<a href='https://gait.mercycorps.org/editgrant.vm?GrantID=" + cell_value + "' target='_blank'>" + cell_value + "</a>";
                    }
                    row.appendChild(createTD(cell_value));
                }
            }
            tbody.appendChild(row);
        }
        pTable.appendChild(tbody);
        pTable.setAttribute("id", "donor_with_num_of_grants_table");
        pTable.setAttribute("class", "table table-striped table-bordered table-hover table-condensed");
    }
    return pTable;
};
/* 
 * ********* USAGE *******
 * <div id="test"> </div>
 * var table = "[{'Country':'mycity','Name':'abc','Age':'29','Email':'test@mail.com'}," +
       "{'Name':'abcd','Age':'39','Email':'test1@mail.com'}," +
       "{'Name':'abcde','Age':'30','Email':'test2@mail.com'}," +
       "{'Age':'30','Sex':'male','Name':'abcde'}]";
 *
 * table = eval('' + table + '');
 * var c = new tableObject(table);
 * document.getElementById("test").appendChild(c);
 *
 */
 
 
 
/*
 * Get a cookie by name.
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/*
 * Set the csrf header before sending the actual ajax request
 * while protecting csrf token from being sent to other domains
 */
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});