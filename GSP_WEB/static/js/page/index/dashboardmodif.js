function handleEditLink (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.link = $('#pop_link').val();

        var request = $.ajax({
            url:"/modifindex/DashboardLinkModif",
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
        url: "/modifindex/getTopBoardModif",
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

            $("#total_collected_url_today").text("URL:" + data.uri.toLocaleString());
            $("#total_collected_file_today").text("FILE:" + data.file.toLocaleString());


//            $('#today_file_analysis_counter').text(data.totalTodayMaliciousFileCount.toLocaleString());

            $('#imas_file_analysis_today').text("IMAS:" + data.totalTodayMaliciousFileCountIMAS.toLocaleString());
            $('#npc_file_analysis_today').text("NPC:" + data.totalTodayMaliciousFileCountNPC.toLocaleString());
            $('#zombie_file_analysis_today').text("ZombieZero:" + data.totalTodayMaliciousFileCountZombieZero.toLocaleString());


            $('#total_important_DNA_count').html("<span id='total_important_DNA_value' data-toggle='tooltip' data-placement='top' title=''>"+data.highestImportantDNATotalCount.toLocaleString()+"</span>");
            $('#total_important_DNA_value').prop("title", data.highestImportantDNAName.toLocaleString());
//            $('#total_important_DNA_value').text(data.highestDNANameTotal.toLocaleString());

//            $('#whitelisted_important_DNA_count').html("<span href='#' id='whitelisted_important_DNA_value' data-toggle='tooltip' data-placement='top' title=''>"+"WhiteList:"+data.highestImportantDNAWhitelistedCount.toLocaleString()+"</span>");
            $('#whitelisted_important_DNA_count').html("<span href='#' id='whitelisted_important_DNA_value' data-toggle='tooltip' data-placement='top' title='' style='color:white;'>'</span>");
            $('#whitelisted_important_DNA_value').prop("title", data.highestImportantDNAName.toLocaleString());

            $('#today_link_result_count').text(data.todayLinkResultCount.toLocaleString());
            $('#total_link_result_count').text(data.totalLinkResultCount.toLocaleString());


            $('#today_link_analysis_count').text(data.todayLinkAnalysisCount.toLocaleString());
            $('#total_link_analysis_count').text(data.totalLinkAnalysisCount.toLocaleString());


            $('#today_collected_link').text(data.todayCollectedLink.toLocaleString());
            $('#total_collected_link').text(data.totalCollectedLink.toLocaleString());

            $('#collected_url_today').text(data.todayCollectedURLCount.toLocaleString());
            $('#collected_url_total').text(data.totalCollectedURLCount.toLocaleString());

//            $('#counter_sub_today_file_analysis').text("어제:"+data.totalYesterdayMaliciousFileCount.toLocaleString());
            $('#today_crawled_elements').text(data.todayCrawledElementCount.toLocaleString());
            $('#total_crawled_elements').text(data.totalCrawledElementCount.toLocaleString());

            $('#counter_total_malicious_url').text(data.totalAnalysisCountElasticsearch.toLocaleString());


            $('#3rd_party_analysis_result_today').text(data.todayAnalysisCountElasticsearch.toLocaleString());
            $('#3rd_party_analysis_result_total').text(data.totalAnalysisCountElasticsearch.toLocaleString());

            $('#mal_code_count_today').text(data.todayMaliciousFileCountRDBMS.toLocaleString());
            $('#mal_code_count_total').text(data.totalMaliciousFileCountRDBMS.toLocaleString());

            $('#counter_bcode').text(data.bcode.toLocaleString());
            $('#counter_sub_bcode').text("어제:"+data.before_bcode.toLocaleString());
        }
    });
}

//link DNA collection chart
function getLineChart(){
    $('#chartLineChart').loading();

    $.ajax({
        url: "/modifindex/getLineChartModif",
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
                    "axisColor": "#DADADA",
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
                    "title": "NetFlow 갯수",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 10,
                    "bulletBorderColor": "#ffffff",
                    "bulletBorderAlpha": 1,
                    "bulletBorderThickness": 2,
                    "valueField": "netflowCount"
                }, {
                    "title": "Traffic 갯수",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 10,
                    "bulletBorderColor": "#ffffff",
                    "bulletBorderAlpha": 1,
                    "bulletBorderThickness": 2,
                    "valueField": "trafficCount"
                }, {
                    "title": "Syslog 갯수",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 10,
                    "bulletBorderColor": "#ffffff",
                    "bulletBorderAlpha": 1,
                    "bulletBorderThickness": 2,
                    "valueField": "syslogCount"
                }],
                "chartScrollbar": {
                    "enabled" : false
                },
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
            setTimeout(function(){
//                    $('.amcharts-scrollbar-horizontal').css("visibility", "hidden");
//                    $('[aria-label="Zoom chart using cursor arrows"]').css("visibility", "hidden");
            }, 2000);
        }
    });
}

function getBarChart(){
    $('#chartBarChart').loading();

    $.ajax({
        url: "/modifindex/getBarChartModif",
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
                    "axisColor": "#DADADA",
                    "axisThickness": 1,
                    "axisAlpha": 1,
                    "position": "left"
                }],
                "graphs": [{
                    "title": "Link DNA TI",
                    "balloonText": "[[title]]: <b>[[value]]</b>",
                    "bullet": "round",
                    "bulletSize": 1,
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 0,
                    "fillAlphas": 1,
                    "lineAlpha": 1,
                    "valueField": "DNA_count",
                    "type": "column"
                }],
                "chartScrollbar": {
                    "enabled" : false
                },
                "chartCursor": {
                    "zoomable": false
                },
                "categoryField": "DNA_name",
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
            setTimeout(function(){
//                    $('.amcharts-scrollbar-horizontal').css("visibility", "hidden");
//                    $('[aria-label="Zoom chart using cursor arrows"]').css("visibility", "hidden");
            }, 2000);
        }
    });
}


function getWorldChart() {

    $('#worldchart').loading();

    $.ajax({
        url: "/modifindex/getWorldChartModif",
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
        url: "/modifindex/getGridModif",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            for(var i =0; i < data.length; i ++) {
                var tr = "<tr>";
                var td = "<td>{0}</td>".format(data[i].date);
                td += "<td>{0}</td>".format(data[i].Netflow.toLocaleString());
                td += "<td>{0}</td>".format(data[i].Syslog.toLocaleString());
                td += "<td>{0}</td>".format(data[i].Traffic.toLocaleString());
                td += "<td>{0}</td>".format(data[i].total.toLocaleString());
                html = tr + td + "</tr>";
                $("#tblCountry-tbody1").append(html);
                setTimeout(function(){
                    $('.amcharts-scrollbar-horizontal').css("visibility", "hidden");
                    $('[aria-label="Zoom chart using cursor arrows"]').css("visibility", "hidden");
                }, 2000);
            }
        }
    });
}

//1st chart of the 1st line and stacked bar chart graphs for file/url collection status chart
function getLineChartMalcode(){
    $('#chartLineChart2').loading();

    $.ajax({
        url: "/modifindex/getLineChartModifMaliciousCodeInfoDaily",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartLineChart2", {
                "type": "serial",
                "theme": "none",
                "legend": {
                    "useGraphSettings": true,
                    "equalWidths" : false,
                    "spacing" : 30
                },
                "dataProvider": data.data,
                "synchronizeGrid":true,
                "valueAxes": [
                    {
                    "stackType": "regular",
                    "axisAlpha": 0.3,
                    "gridAlpha": 0
                    }
//                {
//                    "id":"v1",
//                    "axisColor": "#DADADA",
//                    "axisThickness": 2,
//                    "axisAlpha": 1,
//                    "position": "left"
//                }
//                ,
//                {
//                    "id":"v2",
//                    "axisColor": "#FCD202",
//                    "axisThickness": 2,
//                    "axisAlpha": 1,
//                    "position": "right"
//                }
//                ,
//                {
//                    "id":"v3",
//                    "axisColor": "#B0DE09",
//                    "axisThickness": 2,
//                    "gridAlpha": 0,
//                    "offset": 50,
//                    "axisAlpha": 1,
//                    "position": "left"
//                }
                ],
                "graphs": [
                 {
                    "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                        "fillAlphas": 0.8,
                        "labelText": "[[value]]",
                        "lineAlpha": 0.3,
                        "title": "URL 수집 건수",
                        "type": "column",
                        "color": "#000000",
                        "valueField": "totalUrlCollectionCount"
                }
                ,
                {
                        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                        "fillAlphas": 0.8,
                        "labelText": "[[value]]",
                        "lineAlpha": 0.3,
                        "title": "파일 수집 건수",
                        "type": "column",
                        "color": "#000000",
                        "valueField": "totalFileCollectionCount"
                }
//                    {
//                        "title": "IMAS",
//                        "balloonText": "[[title]]: <b>[[value]]</b>",
//                        "bullet": "round",
//                        "bulletSize": 10,
//                        "bulletBorderColor": "#ffffff",
//                        "bulletBorderAlpha": 1,
//                        "bulletBorderThickness": 2,
//                        "valueField": "imas_count"
//                    }
//                , {
//                    "title": "ZombieZero",
//                    "balloonText": "[[title]]: <b>[[value]]</b>",
//                    "bullet": "round",
//                    "bulletSize": 10,
//                    "bulletBorderColor": "#ffffff",
//                    "bulletBorderAlpha": 1,
//                    "bulletBorderThickness": 2,
//                    "valueField": "zombie_count"
//                }
//                , {
//                    "title": "Syslog 갯수",
//                    "balloonText": "[[title]]: <b>[[value]]</b>",
//                    "bullet": "round",
//                    "bulletSize": 10,
//                    "bulletBorderColor": "#ffffff",
//                    "bulletBorderAlpha": 1,
//                    "bulletBorderThickness": 2,
//                    "valueField": "syslogCount"
//                }
                ],
                "chartScrollbar": {
                    "enabled" : false
                },
                "chartCursor": {
                    "zoomable": false
                },
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "gridAlpha": 0,
                    "position": "left"
                },
                "export": {
                    "enabled": true,
                    "position": "bottom-right"
                }
            } );

            $('#chartLineChart2').loading('stop');
            setTimeout(function(){
//                    $('.amcharts-scrollbar-horizontal').css("visibility", "hidden");
//                    $('[aria-label="Zoom chart using cursor arrows"]').css("visibility", "hidden");
             }, 2000);
        }
    });
}

//2nd chart of the 1st line it is a stacked graph now.
function getBarChartMalcode(){
    $('#chartBarChart2').loading();

    $.ajax({
        url: "/modifindex/getBarChartModifMalcode",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartBarChart2", {
                "type": "serial",
                "theme": "none",
                "legend": {
//                    "horizontalGap": 10,
//                    "maxColumns": 1,
//                    "position": "right",
                    "useGraphSettings": true,
                    "equalWidths" : false,
                    "spacing" : 20


//                    "markerSize": 10
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
                      "stackType": "regular",
                        "axisAlpha": 0.3,
                        "gridAlpha": 0
//                    "id":"v1",
//                    "axisColor": "#DADADA",
//                    "axisThickness": 1,
//                    "axisAlpha": 1,
//                    "position": "left"
                }],
                "graphs": [{
//                    "title": "악성코드 탐지 TOP3",
//                    "balloonText": "[[title]]: <b>[[value]]</b>",
//                    "bullet": "round",
//                    "bulletSize": 1,
//                    "useLineColorForBulletBorder": true,
//                    "bulletBorderThickness": 0,
//                    "fillAlphas": 1,
//                    "lineAlpha": 1,
//                    "valueField": "count",
//                    "type": "column"
                       "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                        "fillAlphas": 0.8,
                        "labelText": "[[value]]",
                        "lineAlpha": 0.3,
                        "title": "전체 파일 분석 요청 건수",
                        "type": "column",
                        "color": "#000000",
                        "valueField": "TotalDailyFileCount"
                }
                ,
                {
                        "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                        "fillAlphas": 0.8,
                        "labelText": "[[value]]",
                        "lineAlpha": 0.3,
                        "title": "악성 판정 건수",
                        "type": "column",
                        "color": "#000000",
                        "valueField": "TotalDailyMalFileCount"
                }],
                "chartScrollbar": {
                    "enabled" : false
                },
                "chartCursor": {
                    "zoomable": false
                },
                "categoryField": "xaxis",
                "categoryAxis": {
//                    "axisColor": "#DADADA",
//                    "minorGridEnabled": false
                        "gridPosition": "start",
                        "axisAlpha": 0,
                        "gridAlpha": 0,
                        "position": "left"
                },
                "export": {
                    "enabled": true,
                    "position": "bottom-right"
                }
            } );

            $('#chartBarChart2').loading('stop');
             setTimeout(function(){
//                    $('.amcharts-scrollbar-horizontal').css("visibility", "hidden");
//                    $('[aria-label="Zoom chart using cursor arrows"]').css("visibility", "hidden");
             }, 2000);
        }
    });
}


function getWorldChartMalCode() {

    $('#worldchart').loading();

    $.ajax({
        url: "/modifindex/getWorldChartModif",
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

function getGridMalcode() {

    $.ajax({
        url: "/modifindex/getGridModifTotalMalCodeByMonth",
        //data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            for(var i =0; i < data.length; i ++) {
                var tr = "<tr>";
                var td = "<td>{0}</td>".format(data[i].date.toLocaleString());
                td += "<td>{0}</td>".format(data[i].collection.toLocaleString());
                td += "<td>{0}</td>".format(data[i].analyzed.toLocaleString());
//                td += "<td>{0}</td>".format(data[i].Traffic);
                td += "<td>{0}</td>".format(data[i].total.toLocaleString());
                html = tr + td + "</tr>";
                $("#tblCountry-tbody2").append(html);

                setTimeout(function(){
//                    $('.amcharts-scrollbar-horizontal').css("visibility", "hidden");
//                    $('[aria-label="Zoom chart using cursor arrows"]').css("visibility", "hidden");
                }, 500);
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