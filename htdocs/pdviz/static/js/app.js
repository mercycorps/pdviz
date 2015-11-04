$(document).ready(function() {
    $('body').on('change', 'select#id_region', function() {
        var selected_region = $(this).val();
        var url ;
        if (selected_region == undefined || selected_region == -1 || selected_region == '' || selected_region == 0) {
            url = '/api/v1/countries/';
        } else {
            url = "/dataviz/countries_by_region/" + selected_region + "/";
        }    
        $.getJSON(url, function(countries) {
            var options = "<option value=''>-- Country --</option>";
            for (var i = 0; i < countries.length; i++) {
                options += '<option value="' + countries[i].country_id + '">' + countries[i].name + '</option>';
            }
            $("select#id_country").html(options);
            $("select#id_country option:first").attr('selected', 'selected'); 
        });
    });

    $('body').on('change', 'select#id_sector', function() {
        var selected_sector = $(this).val();
        var url;
        if (selected_sector == undefined || selected_sector == -1 || selected_sector == '' || selected_sector == 0) {
            url = '/api/v1/subsector/';
        } else {
            url = '/api/v1/subsector/?sector=' + selected_sector;
        }
        $.getJSON(url, function(subsectors) {
            var options = "<option value=''>--Area of Focus--</option>";
            for (var i = 0; i < subsectors.length; i++) {
                options += '<option value="' + subsectors[i].subsector_id + '">' + subsectors[i].name + '</option>';
            }
            $('select#id_subsector').html(options);
            $('select#id_subsector option:first').attr('selected', 'selected');
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
    $(".dynamic-alert").delay(3000).fadeOut("slow", function () { $(this).remove(); });
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
                if (item == 'drilldown') { continue };
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
                //console.log(name);
                if (name == 'drilldown') {
                    continue;
                }
                if (eval("data[" + i + "].hasOwnProperty('" + name + "')")) {
                    row.appendChild(createTD(eval('data[' + i + '].' + name)));
                } else {
                    row.appendChild(createTD(''));
                }
            }
            tbody.appendChild(row);
        }
        pTable.appendChild(tbody);
        pTable.setAttribute("id", "chart_data");
        pTable.setAttribute("class", "table table-striped table-bordered");
        pTable.setAttribute("cellspacing", "0");
        //pTable.setAttribute("width", "100%");
    }
    return pTable;
};
// <div id="test"> </div>
/*
var table = "[{'Country':'mycity','Name':'abc','Age':'29','Email':'test@mail.com'}," +
       "{'Name':'abcd','Age':'39','Email':'test1@mail.com'}," +
       "{'Name':'abcde','Age':'30','Email':'test2@mail.com'}," +
       "{'Age':'30','Sex':'male','Name':'abcde'}]";
*/
//table = eval('' + table + '');
//var c = new tableObject(table);
//document.getElementById("test").appendChild(c);