var timeSetting = $("#timeSetting").val();
//var timeSetting = '3d';

function getTopBoard(){

    $.ajax({
        url: "/index/getTopBoard",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            $('#counter_File_Gether').text(data.count_file_total.toLocaleString());
            $('#counter_File_Analysis').text(data.count_file_analysis.toLocaleString());
            $('#counter_File_Warning').text(data.count_file_danger.toLocaleString());
            $('#counter_File_Normal').text(data.count_file_normal.toLocaleString());

            $('#counter_URI_Gether').text(data.count_file_total.toLocaleString());
            $('#counter_URI_Analysis').text(data.count_file_analysis.toLocaleString());
            $('#counter_URI_Warning').text(data.count_file_danger.toLocaleString());
            $('#counter_URI_Normal').text(data.count_file_normal.toLocaleString());
        }
    });
}

function getSendBytes(){

    $('#chartSendBytes').loading();

    $.ajax({
        url: "/index/getChart-SendBytes",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartSendBytes", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return formatFileSize(value);
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "송신량: <b>" + formatFileSize(item.values.value) + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "수신 bytes",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "평균 송신량: <b>" + formatFileSize(item.values.value) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + formatFileSize(item.values.value) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45,
                    "equalSpacing" : true
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartSendBytes').loading('stop');
        }
    });
}

function getRecvBytes(){
    $('#chartRecvBytes').loading();
    $.ajax({
        url: "/index/getChart-RecvBytes",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartRecvBytes", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return formatFileSize(value);
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "수신량: <b>" + formatFileSize(item.values.value) + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "수신 bytes",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "평균 수신량: <b>" + formatFileSize(item.values.value) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + formatFileSize(item.values.value) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartRecvBytes').loading('stop');
        }
    });
}

function formatFileSize(value) {
  if (value >= 1073741824)
    return (Math.round(value / 1073741824 * 100) / 100) + "TB";
  else if (value >= 1048576)
    return (Math.round(value / 1048576 * 100) / 100) + "MB";
  else if (value >= 1024)
    return Math.round(value / 1024) + "KB";
  else
    return value + "B";
}

function getSendPkts(){
    $('#chartSendPkts').loading();

    $.ajax({
        url: "/index/getChart-SendPkts",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartSendPkts", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return value.toLocaleString();
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "송신 패킷: <b>" + item.values.value.toLocaleString() + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "송신 패킷",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "평균 송신 패킷: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartSendPkts').loading('stop');
        }
    });
}

function getRecvPkts(){
    $('#chartRecvPkts').loading();

    $.ajax({
        url: "/index/getChart-RecvPkts",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartRecvPkts", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return value.toLocaleString();
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "수신 패킷: <b>" + item.values.value.toLocaleString() + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "수신 패킷",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "평균 수신 패킷: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartRecvPkts').loading('stop');
        }
    });
}

function getSessionTime(){

    $('#chartSessionTime').loading();

    $.ajax({
        url: "/index/getChart-SessionTime",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartSessionTime", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return value.toLocaleString();
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "세션 유지시간: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "초</b>";
                    },
                    "fillAlphas": 1,
                    "title": "수신 패킷",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "평균 세션 유지시간: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartSessionTime').loading('stop');
        }
    });
}

function getSessionCount(){

    $('#chartSessionCount').loading();

    $.ajax({
        url: "/index/getChart-SessionCount",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartSessionCount", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return value.toLocaleString();
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "세션 수: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "수신 수",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "평균 세션 수: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartSessionCount').loading('stop');

        }
    });
}

function getServerCon(){

    $('#chartServerCon').loading();

    $.ajax({
        url: "/index/getChart-ServerCon",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartServerCon", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return value.toLocaleString();
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "접속 수: <b>" + item.values.value.toLocaleString() + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "접속수",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "접속 수: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartServerCon').loading('stop');
        }
    });
}

function getClientCon(){
    $('#chartClientCon').loading();

    $.ajax({
        url: "/index/getChart-ClientCon",
        data: {'timeSetting': timeSetting},
        dataType: "json",
        success: function (data) {
            var chart = AmCharts.makeChart( "chartClientCon", {
                "type": "serial",
                "addClassNames": true,
                "theme": "light",
                "autoMargins": true,

                "balloon": {
                    "adjustBorderColor": false,
                    "horizontalPadding": 10,
                    "verticalPadding": 8,
                    "color": "#ffffff"
                },

                "dataProvider": data.data,
                "valueAxes": [ {
                    "axisAlpha": 0,
                    "position": "left",
                    "labelFunction" : function(value) {
                        return value.toLocaleString();
                    }
                } ],
                "startDuration": 1,
                "graphs": [ {
                    "alphaField": "alpha",
                    "balloonFunction":  function(item) {
                        return "접속 수: <b>" + item.values.value.toLocaleString() + "</b>";
                    },
                    "fillAlphas": 1,
                    "title": "접속수",
                    "type": "column",
                    "valueField": "yaxis",
                    "dashLengthField": "dashLengthColumn"
                }, {
                    "id": "graph2",
                    "balloonFunction":  function(item) {
                        return "접속 수: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "avg",
                    "dashLengthField": "dashLengthLine"
                }, {
                    "id": "graph3",
                    "balloonFunction":  function(item) {
                        return "표준 편차: <b>" + item.values.value.toLocaleString(undefined, {maximumFractionDigits:2}) + "</b>";
                    },
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 7,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "fillAlphas": 0,
                    "lineAlpha": 1,
                    "title": "평균",
                    "valueField": "std_dev",
                    "dashLengthField": "dashLengthLine"
                } ],
                "categoryField": "xaxis",
                "categoryAxis": {
                    "gridPosition": "start",
                    "axisAlpha": 0,
                    "tickLength": 0,
                    "labelRotation" : 45
                },
                "export": {
                    "enabled": true
                },
                "marginBottom": 100,
                "marginLeft" : 30
            } );

            $('#chartClientCon').loading('stop');
        }
    });
}


$.fn.digits = function(){
    return this.each(function(){
        $(this).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
    })
}



function getWorldChart() {

    $('#worldchart').loading();

    $.ajax({
        url: "/index/getWorldChart",
        data: {'timeSetting': timeSetting},
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
                    "text": "분석결과 악성 URI",
                    "size": 14
                }, {
                    "text": "지역별 분포토",
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
                    "enabled": true
                }
            });

            //Bind DataTable
            $('#tblCountry-tbody').empty();
            for (var i = 0; i < data.mapData.length; i++) {
                if (i < 7)
                    $('#tblCountry-tbody').append('<tr><td>'+data.mapData[i].name+'</td><td>'+data.mapData[i].value.toLocaleString()+'</td></tr>');
            }

            //$("demo-foo-filtering").DataTable();
        }
    });
}

