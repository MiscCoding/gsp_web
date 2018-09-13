function handleEditLink (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.link = $('#pop_link').val();

        var request = $.ajax({
            url:"/index/DashboardLink",
            type:"PUT",
            data:postData,
            success: function(data, status){
                window.location.reload();
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

/*timer = setInterval( function(){
    getTopBoard();
} , 5000);
*/
function getTopBoard(){

    $.ajax({
        url: "/index/getTopBoard",
        dataType: "json",
        success: function (data) {
            $('#counter_link').text(data.link.toLocaleString());
            $('#counter_sub_link').text("어제:"+data.before_link.toLocaleString());
            $('#counter_uri').text(data.uri.toLocaleString());
            $('#counter_sub_uri').text("어제:"+data.before_uri.toLocaleString());
            $('#counter_file').text(data.file.toLocaleString());
            $('#counter_sub_file').text("어제:"+data.before_file.toLocaleString());

            $('#today_url_analysis_counter').text(data.totalTodayUriAnalysisCount.toLocaleString());
            $('#counter_sub_today_url_analysis').text("어제:"+data.totalYesterdayMaliciousUrlCount.toLocaleString());

            $('#imas_url_analysis_today').text("IMAS:" + data.totalTodayUriAnalysisCountIMAS.toLocaleString());
            $('#npc_url_analysis_today').text("NPC:" + data.totalTodayUriAnalysisCountNPC.toLocaleString());

            $('#today_file_analysis_counter').text(data.totalTodayMaliciousFileCount.toLocaleString());

            $('#imas_file_analysis_today').text("IMAS:" + data.totalTodayMaliciousFileCountIMAS.toLocaleString());
            $('#npc_file_analysis_today').text("NPC:" + data.totalTodayMaliciousFileCountNPC.toLocaleString());
            $('#zombie_file_analysis_today').text("ZombieZero:" + data.totalTodayMaliciousFileCountZombieZero.toLocaleString());

            $('#counter_sub_today_file_analysis').text("어제:"+data.totalYesterdayMaliciousFileCount.toLocaleString());


            $('#counter_total_malicious_url').text(data.totalMaliciousUrlCount.toLocaleString());
//            $('#counter_spread').text(data.spread.toLocaleString());
//            $('#counter_sub_spread').text("어제:"+data.before_spread.toLocaleString());
            $('#counter_cnc').text(data.cnc.toLocaleString());
            //$('#counter_sub_cnc').text("어제:"+data.before_cnc.toLocaleString());
            $('#counter_bcode').text(data.bcode.toLocaleString());
            $('#counter_sub_bcode').text("어제:"+data.before_bcode.toLocaleString());
        }
    });
}

function getLineChart(){
    $('#chartLineChart').loading();

    $.ajax({
        url: "/index/getLineChart",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartLineChart", {
                "type": "serial",
                "theme": "light",
                "legend": {
                    "useGraphSettings": false
                },
                "dataProvider": data.data,
                "synchronizeGrid":true,
                "valueAxes": [{
                    "id":"v1",
                    "axisColor": "#FF6600",
                    "axisThickness": 2,
                    "axisAlpha": 1,
                    "position": "left"
                }, {
                    "id":"v2",
                    "axisColor": "#FCD202",
                    "axisThickness": 2,
                    "axisAlpha": 1,
                    "position": "right"
                }, {
                    "id":"v3",
                    "axisColor": "#B0DE09",
                    "axisThickness": 2,
                    "gridAlpha": 0,
                    "offset": 50,
                    "axisAlpha": 1,
                    "position": "left"
                }],
                "graphs": [{
                    "title": "악성코드 유포지",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 10,
                    "bulletBorderColor": "#ffffff",
                    "bulletBorderAlpha": 1,
                    "bulletBorderThickness": 2,
                    "valueField": "spread"
                }, {
                    "title": "C&C 서버",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 10,
                    "bulletBorderColor": "#ffffff",
                    "bulletBorderAlpha": 1,
                    "bulletBorderThickness": 2,
                    "valueField": "CNC"
                }, {
                    "title": "악성코드",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 10,
                    "bulletBorderColor": "#ffffff",
                    "bulletBorderAlpha": 1,
                    "bulletBorderThickness": 2,
                    "valueField": "bcode"
                }],
                "chartScrollbar": {},
                "chartCursor": {
                    "zoomable": false
                },
                "categoryField": "date",
                "categoryAxis": {
                    "axisColor": "#DADADA",
                    "minorGridEnabled": false
                },
                "export": {
                    "enabled": true,
                    "position": "bottom-right"
                }
            } );

            $('#chartLineChart').loading('stop');
        }
    });
}

function getBarChart(){
    $('#chartBarChart').loading();

    $.ajax({
        url: "/index/getBarChart",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartBarChart", {
                "type": "serial",
                "theme": "light",
                "legend": {
                    "useGraphSettings": true
                },
                "dataProvider": data.data,
                "synchronizeGrid":true,
                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },
                "valueAxes": [{
                    "id":"v1",
                    "axisColor": "#FF6600",
                    "axisThickness": 1,
                    "axisAlpha": 1,
                    "position": "left"
                }],
                "graphs": [{
                    "title": "전체 위협정보",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 1,
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 0,
                    "fillAlphas": 1,
                    "lineAlpha": 1,
                    "valueField": "value",
                    "type": "column"
                }],
                "chartScrollbar": {},
                "chartCursor": {
                    "zoomable": false
                },
                "categoryField": "date",
                "categoryAxis": {
                    "axisColor": "#DADADA",
                    "minorGridEnabled": false
                },
                "export": {
                    "enabled": true,
                    "position": "bottom-right"
                }
            } );

            $('#chartBarChart').loading('stop');
        }
    });
}


function getWorldChart() {

    $('#worldchart').loading();

    $.ajax({
        url: "/index/getWorldChart",
        data: {'timeSetting': $("#worldchartDate").val()},
        dataType: "json",
        success: function (data) {
            $('#worldchart').loading('stop');

            // get min and max values
            var minBulletSize = 3;
            var maxBulletSize = 70;
            var min = Infinity;
            var max = -Infinity;
            for (var i = 0; i < data.mapData.length; i++) {
                var value = data.mapData[i].value;
                if (value < min) {
                    min = value;
                }
                if (value > max) {
                    max = value;
                }
            }

// it's better to use circle square to show difference between values, not a radius
            var maxSquare = maxBulletSize * maxBulletSize * 2 * Math.PI;
            var minSquare = minBulletSize * minBulletSize * 2 * Math.PI;

// create circle for each country
            var images = [];
            for (var i = 0; i < data.mapData.length; i++) {
                var dataItem = data.mapData[i];
                var value = dataItem.value;
                // calculate size of a bubble
                var square = (value - min) / (max - min) * (maxSquare - minSquare) + minSquare;
                if (square < minSquare) {
                    square = minSquare;
                }
                var size = Math.sqrt(square / (Math.PI * 2));
                var id = dataItem.code;

                images.push({
                    "type": "circle",
                    "theme": "light",
                    "width": size,
                    "height": size,
                    "color": dataItem.color,
                    "longitude": data.latlong[id].longitude,
                    "latitude": data.latlong[id].latitude,
                    "title": dataItem.name + " : " + value.toLocaleString(),
                    "value": value
                });
            }

// build map
            var map = AmCharts.makeChart("worldchart", {
                "type": "map",
                "projection": "eckert6",
                "titles": [{
                    "text": "",
                    "size": 14
                }, {
                    "text": "",
                    "size": 11
                }],
                "areasSettings": {
                    //"unlistedAreasColor": "#000000",
                    //"unlistedAreasAlpha": 0.1
                },
                "dataProvider": {
                    "map": "worldLow",
                    "images": images
                },
                "export": {
                    "enabled": false
                }
            });

            //Bind DataTable
            $('#tblCountry-tbody').empty();
            for (var i = 0; i < data.mapData.length; i++) {
                if (i < 5)
                    $('#tblCountry-tbody').append('<tr><td>'+data.mapData[i].name+'</td><td>'+data.mapData[i].value.toLocaleString()+'</td></tr>');
            }

            $("demo-foo-filtering").DataTable();
        }
    });
}

function getGrid() {

    $.ajax({
        url: "/index/getGrid",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            for(var i =0; i < data.length; i ++) {
                var tr = "<tr>";
                var td = "<td>{0}</td>".format(data[i].date);
                td += "<td>{0}</td>".format(data[i].spread);
                td += "<td>{0}</td>".format(data[i].cnc);
                td += "<td>{0}</td>".format(data[i].bcode);
                td += "<td>{0}</td>".format(data[i].total);
                html = tr + td + "</tr>";
                $("#tblCountry-tbody1").append(html);
            }
        }
    });
}

String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
}