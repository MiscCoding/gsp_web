var curpage = 1;
var columnList = [];
var columnDef = {};



function downloadExcel(){
    var ids = [];
    $("[name='search_type_a']:checked").each(function(){
        ids.push(this.id.substr(4));
    });

    data = {
        requestColumnList : ids,
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
        search_src_ip : $("#search_src_ip").val().replace(/\s/g,''),
        search_dst_ip : $("#search_dst_ip").val().replace(/\s/g,'')
    };
    requestColumnList = jQuery.parseJSON(JSON.stringify(data));

    var form = document.createElement('form');

    var objs, value;
    for (var key in requestColumnList) {
        value = requestColumnList[key];
        objs = document.createElement('input');
        objs.setAttribute('type', 'hidden');
        objs.setAttribute('name', key);
        objs.setAttribute('value', value);
        form.appendChild(objs);
    }

    form.setAttribute('method', 'post');
    form.setAttribute('action', "/links/analysis_result/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

//return an array of values that match on a certain key
function getValues(obj, key) {
    var objects = [];
    for (var i in obj) {
        if (!obj.hasOwnProperty(i)) continue;
        if (typeof obj[i] == 'object') {
            objects = objects.concat(getValues(obj[i], key));
        } else if (i == key) {
            objects.push(obj[i]);
        }
    }
    return objects;
}

//return an array of keys that match on a certain value
function getKeys(obj, val) {
    var objects = [];
    for (var i in obj) {
        if (!obj.hasOwnProperty(i)) continue;
        if (typeof obj[i] == 'object') {
            objects = objects.concat(getKeys(obj[i], val));
        } else if (obj[i] == val) {
            objects.push(i);
        }
    }
    return objects;
}

function showWhoisResult(_ip){

    $body.addClass("loading");

    urlREST = 'http://whois.kisa.or.kr/openapi/whois.jsp?query={0}&key=2018032013435689368141&answer=json'.format(_ip);
    var postData = new Object();
    postData._ip = _ip;

    console.log( ($.support.cors) );
    var request = $.ajax({
            //url:urlREST,
            url: "/links/analysis_result/whoisrequest",
//            type: "GET",
            type:"POST",
            data:postData,
            success: function(data, status){



               // var data = JSON.parse(data);
                var query = getValues(data, 'query')[0];
                var countryCode = (getValues(data, 'countryCode')[0]);
                var orgName = (getValues(data, 'orgName')[0]);
                var range = (getValues(data, 'range')[0]);
                var servName = (getValues(data, 'servName')[0]);
                var wholeResponse = JSON.stringify(data, null, 2)

                var myObject = {};
                myObject.query = query;
                myObject.countryCode = countryCode;
                myObject.orgName = orgName;
                myObject.range = range;
                myObject.servName = servName;

                var jsonStr = JSON.stringify(myObject, null, 2);


                $("#majorInfo").val(jsonStr);
                $("#totalInfo").val(wholeResponse);


                $body.removeClass("loading");

                $('#modal-popup-detailed-analysis').modal();
            },
            error: function(err, status, err2){
                 $body.removeClass("loading");
                  $('#imas').val("");
                  $('#zombie').val("");
                 alert(err.responseJSON);
            }
        });
}




function selectColumns(colGroup, isSelect){
    $("[name='"+colGroup+"']").each(function(){
        this.checked = isSelect;
    });
    return false;
}

function DatatableReload(){

    var ids = [];
    /*
    $("[name='search_type_a']:checked").each(function(){
        ids.push(this.id.substr(4));
    });
    $("[name='search_type_b']:checked").each(function(){
        ids.push(this.id.substr(4));
    });*/
    $.merge(ids, $("#select_type_a").val());
    $.merge(ids, $("#select_type_b").val());

    if(ids.length <= 0){
        alert('최소한 한개 이상의 컬럼을 선택 해야 합니다.');
        return false;
    }

    // window.location = "/links/analysis_result?src_ip={0}&dst_ip={1}&type={2}&chart_type={3}"
    //     .format($("#search_src_ip").val(),$("#search_dst_ip").val(), $("#search_type").val(), $("#search_chart_type").val())

    columnList = null;
    columnDef = null;

    $("#dtTable_wrapper").empty();
    $("#dtTable_wrapper").remove();
    $("#dtTable_div").append("<table id='dtTable'></table>");

    handleDataTableDefault();

    // $('#dtTable').DataTable().ajax.reload(function(data){
    //     $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
    //     dtTable.page.len($("#perpage").val()).draw();
    // });

}

function DrawChart(chartDiv, seriesData, dataType){
    /* Add a basic data series with six labels and values */

//    dataColumn = chartDiv.substring(0, chartDiv.length - 1);

    var data = {
        //labels: ['1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6'],
        series: [
            {
                data: seriesData
            }
        ]
    };

    /* Set some base options (settings will override the default settings in Chartist.js *see default settings*). We are adding a basic label interpolation function for the xAxis labels. */
    var options = {
        axisX: {
            showLabel: false,
            labelInterpolationFnc: function(value) {
                return 'Calendar Week ' + value;
            }
        }
    };

    var optionsFlaglist = {
              width: '230px',
              height: '130px'
    };



    /* Now we can specify multiple responsive settings that will override the base settings based on order and if the media queries match. In this example we are changing the visibility of dots and lines as well as use different label interpolations for space reasons. */
    var responsiveOptions = [
        ['screen and (min-width: 350px) and (max-width: 350px)', {
            showPoint: false,
            axisX: {
                labelInterpolationFnc: function(value) {
                    return 'Week ' + value;
                }
            }
        }],
        ['screen and (max-width: 350px)', {
            showLine: false,
            axisX: {
                labelInterpolationFnc: function(value) {
                    return 'W' + value;
                }
            }
        }]
    ];

    /* Initialize the chart with the above settings */
    if (dataType == "single_list") {
//               flag_names = ["FIN", "SYN","SYNFIN", "RST",
//                                "RSTFIN", "RSTFIN", "RSTSYN", "RSTSYNFIN",
//                                "PSH", "PSHFIN", "PSHSYN", "PSHSYNFIN",
//                                "PSHRST", "PSHRSTFIN","PSHRSTSYN", "PSHRSTSYNFIN",
//                                "ACK", "ACKFIN", "ACKSYN", "ACKSYNFIN",
//                                "ACKRST", "ACKRSTSYN", "ACKRSTSYNFIN", "ACKPSH",
//                                "ACKPSHSYN", "ACKPSHSYN", "ACKPSHSYNFIN", "ACKPSHRST",
//                                "ACKPSHRSTFIN", "ACKPSHRSTSYN", "ACKPSHRSTSYNFIN", "URG", "URGFIN",
//                                "URGSYN", "URGSYNFIN","URGRST","URGRSTFIN",
//                                "URGRSTSYN","URGRSTSYNFIN","URGPSH","URGPSHFIN",
//                                "URGPSHSYN","URGPSHSYNFIN","URGPSHRST","URGPSHRSTFIN",
//                                "URGPSHRSTSYN","URGPSHRSTSYNFIN","URGACK","URGACKFIN",
//                                "URGACKSYN","URGACKSYNFIN","URGACKRST","URGACKRSTFIN",
//                                "URGACKRSTSYN","URGACKRSTSYNFIN","URGACKPSH","URGACKPSHFIN",
//                                "URGACKPSHSYN","URGACKPSHSYNFIN","URGACKPSHRST","URGACKPSHRSTFIN",
//                                "URGACKPSHRSTSYN","URGACKPSHRSTSYNFIN","nonOne","nonTwo"];
//
//               function sort(arr){
//                           var len = arr.length;
//                           for (var i = 0; i<=len-1; i++){ //loop for array length-1 times(because first index starts fom 0)
//                                for(var j = i+1; j<=len-1; j++){ // loop every time starting from i value till length-1 of array
//                                   if(arr[i]<arr[j]){ // this condition do the checking if current ith value is bigger than current jth value. You can alter this condition if you need descending array.
//                                      var temp = arr[i];
//
//                                         arr[i] = arr[j];
//                                         arr[j] = temp;
//                                      var tempName = flag_names[i];
//                                         flag_names[i] = flag_names[j];
//                                         flag_names[j] = tempName;
//                                      }
//                                   }
//                                }
//                            return arr;
//                        }
//
//          sortedSeriesData = sort(seriesData);
//          topFiveHighestValues = [];
//          topFiveHighestNames = [];
//
//         for(var i = 0; i<5; i++){
//            topFiveHighestValues.push(sortedSeriesData[i]);  // This code sorts the flag list elements and extracts top ten highest values in the pie chart.
//            topFiveHighestNames.push(flag_names[i].substring(0,4));
//         }
//
//        data = {
//            labels: topFiveHighestNames,
//            series: topFiveHighestValues//topTenHighestValues//   // This code the flag list elements in histogram.
//        }
//
//        distributeSeriesObj = {
//            distributeSeries: true
//        }

        new Chartist.Line('#'+chartDiv, data, options, responsiveOptions);
        //new Chartist.Bar('#'+chartDiv, data, distributeSeriesObj);
        //new Chartist.Bar('#'+chartDiv, data, distributeSeriesObj); // This code the flag list elements in histogram.
    }  else {
        new Chartist.Line('#'+chartDiv, data, options, responsiveOptions);
    }

}

function openWhoisWindow(ip){
    url = 'http://whois.kisa.or.kr/openapi/whois.jsp?query={0}&key=2018032013435689368141&answer=xml'.format(ip);
    window.open(url, 'Whois', "width=1280", "height=720");
}


function getColdef(_columnList){
    colDef = [];

    linkDef = {
        "targets" : 0,
        "width" : "100px",
        "render" : function(data,type,row,meta){
            var htmlsrcip = row._source.src_ip;
            var htmldstip = row._source.dst_ip;
//            if( row._source.src_country_code != "")
//                html += " (" + row._source.src_country_code + ")";

            url = 'http://whois.kisa.or.kr/openapi/whois.jsp?query={0}&key=2018032013435689368141&answer=xml';
                        //window.open(url, 'ServerCon', "width=1280", "height=720");
            var html = '<a style="text-decoration-line: underline" onclick="showWhoisResult(\'' + row._source.src_ip + '\');">'+ htmlsrcip+'</a>' + '→' + '<a style="text-decoration-line: underline" onclick="showWhoisResult(\'' + row._source.dst_ip + '\');">'+ htmldstip+'</a>'
//            return '<a style="text-decoration-line: underline" onclick="openWhoisWindow(\'' + row._source.src_ip + '\');">'+ html+'</a>'
            return html;

//            return data.replace('_',' → ');
        }
    }
    colDef.push(linkDef);

    for( var i = 1; i < _columnList.length; i ++){
        var div_id = String(_columnList[i].title);

        var _def =
         {
            "targets": i,
             "width" : "300px",
             "title" : div_id,
            "render": function (data, type, row, meta) {
                if(columnList.length <= meta.col)
                    return '';

                var rowHtml = '<div id="' + columnList[meta.col].title + meta.row+'" class="treeview">\r\n';
                rowHtml += '</div>';

                return rowHtml;
            }
        }

        colDef.push(_def);
    }

    columnDef = colDef;

    return colDef;
}

var handleDataTableDefault = function() {
    var ids = [];
    $.merge(ids, $("#select_type_a").val());
    $.merge(ids, $("#select_type_b").val());
    /*
    $("[name='search_type_a']:checked").each(function(){
        ids.push(this.id.substr(4));
    });
    $("[name='search_type_b']:checked").each(function(){
        ids.push(this.id.substr(4));
    });*/

    data = {ids : ids };
    requestColumnList = jQuery.parseJSON(JSON.stringify(data));

    //$.ajaxSettings.traditional = true;
    $.ajax({
        url: "/links/analysis_result/columnlist?type="+$("#search_type").val(),
        traditional:true,
        method: 'POST',
        data: requestColumnList,
        dataType: "json",
        success: function (colData) {
            columnList = colData;

            getColdef(columnList);

            if ($('#dtTable').length !== 0) {
                dtTable = $('#dtTable').DataTable({
                    "drawCallback": function (settings) {
                        $("#dtTable").parent().addClass('ui container special')
                    },
                    ajax: {
                        url: "/links/analysis_result/list?type=a",
                        traditional:true,
                        "type": 'POST',
                        "data": function (d) {
                            var ids = [];
                            $("[name='search_type_a']:checked").each(function(){
                                ids.push(this.id.substr(4));
                            });

                            d['curpage'] = curpage;
                            d['perpage'] = $("#perpage").val();
                            d['search_src_ip'] = $("#search_src_ip").val().replace(/\s/g,'');
                            d['search_dst_ip'] = $("#search_dst_ip").val().replace(/\s/g,'');
                            d['search_type'] = $("#search_type").val();
                            d['search_chart_type'] = $("#search_chart_type").val();
                            d['requestColumnList'] = ids;
                            $('#tblDetail').empty();
                        }
                    },
                    dataFilter: function (data) {
                        var json = jQuery.parseJSON(data);
                        json.recordsTotal = json.total;
                        json.recordsFiltered = json.total;
                        json.data = json.list;

                        return JSON.stringify(json); // return JSON string
                    },
                    "initComplete": function (settings, json) {
                        $("#divSearch").loading('stop');
                        $('#tblDetail').empty();
                        $('#divTotal').text("총 "+json.total.toLocaleString() + "건");

                    },
                    error: function (xhr, error, thrown) {
                        alert(error);
                        $("#divSearch").loading('stop');
                        error(xhr, error, thrown);
                    },
                    dom: 'Bfrtip',
                    "pagingType": "full_numbers",
                    fixedHeader: true,
                    serverSide: true,
                    pageLength: $("#perpage").val(),
                    bLengthChange: false,
                    processing: true,
                    searching: false,
                    //bPaginate: true,
                    "scrollX": true,
                    "scrollY" : "800px",
                    scroller: {
                        rowHeight: 170
                    },
                    sort: false,
                    paging: true,
                    info: false,
                    deferRender: true,
                    select: 'true',
                    "fixedColumns":   {
                        leftColumns: 1
                    },
                    "jQueryUI": true,
                    "sPaginationType": "full_numbers",
                    columns: colData,
                    columnDefs : columnDef,
                    "drawCallback" : function(setting,data){
                        $("#dtTable").css('float','left');
                        dtTable.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                            var data = this.data();

                            for (var colName in data._source) {

                                var _id = colName + rowIdx;
                                try{
                                    if( $("#"+_id) == null)
                                    continue;
                                }
                                catch (exception){
                                    continue;
                                }

                                //차트 그리기와 RowData그리기의 분기
                                if( $("#search_type").val() =="b" || $("#search_chart_type").val() != "RowData" ) {
                                    _col = getColumnInColumnList(colName);
                                    if(_col == null)
                                        continue;
                                    if( Array.isArray(data._source[colName])) {
                                        if(data._source[colName].length > 1 && (colName !== "sport" && colName !== "dport")) { //)
                                            DrawChart(_id, data._source[colName], _col.data_type);
                                        }
                                        else if (colName === "sport" || colName === "dport") {
                                            $("#" + _id).text(data._source[colName].length + " 개");
                                        }
                                         else
                                            $("#" + _id).text(data._source[colName]);

                                        continue;
                                    }
                                    else{
                                        $("#" + _id).text(data._source[colName]);
                                        continue;
                                    }
                                }

                                cellVal = data._source[colName];

                                //링크요소 A타입 데이터를 TreeViewNode로 반환한다.
                                if( Array.isArray(cellVal) && !Array.isArray(cellVal[0])){
                                    var html = "[";
                                    for(var i =0; i < cellVal.length; i ++){
                                        if(i > 0)
                                            html += ", ";
                                        html += cellVal[i];
                                    }
                                    html += "]";
                                    $("#"+_id).text(html);
                                }
                                else if( Array.isArray(cellVal)) {
                                    rowData = getTypeADataToTreeViewNode(cellVal);

                                    $("#" + _id).treeview({
                                        data: rowData,
                                        showBorder: false,
                                        selected: false,
                                        expanded: false,
                                        expandIcon: "glyphicon glyphicon-stop"
                                    });
                                }
                                else{

                                }

                            }

                        });

                    }
                });
                $.fn.dataTable.ext.errMode = 'none';

            };

            $('#dtTable_paginate').attr('class', 'pagination pagination-split footable-pagination m-t-10 m-b-0');
            $('#dtTable_paginate').css('margin', '0 auto');
            $('.pagination').css('display','table');



        }
    });

}

var TableManageDefault = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleDataTableDefault();
        }
    };
}();

//링크요소 A타입 데이터를 TreeViewNode로 반환한다.
function getTypeADataToTreeViewNode(cellVal){

    var rowData = [{
        text: 'week',
        state: {
            expanded: false
        },
        nodes: []
    }]

    if (Array.isArray(cellVal[0])) {

        for (var i = 0; i < cellVal.length; i++) {

            var node_2 =
                {
                    text: 'day of week[' + i + ']',
                    nodes: []
                };
            rowData[0].nodes.push(node_2);

            for (var k = 0; k < cellVal[i].length; k++) {
                var node_3 =
                    {
                        text: 'hours[' + k + ']',
                        nodes: []
                    };

                rowData[0].nodes[i].nodes.push(node_3);

                for (var j = 0; j < cellVal[i][k].length; j++) {
                    var node_4 = {
                        text: cellVal[i][k][j]
                    }
                    rowData[0].nodes[i].nodes[k].nodes.push(node_4);
                }

            }

        }
    }
    else if( cellVal.length == 1 ){
        var rowData = [{
            text: cellVal[0]
        }]
    }
    else {
        var rowData = [{
            text: 'DataList',
            state: {
                expanded: false
            },
            nodes:[]
        }]
        for (var i = 0; i < cellVal.length; i++) {
            var node_2 =
                {
                    text: cellVal[i]
                };
            rowData[0].nodes.push(node_2);
        }

    }


    return rowData
}

function getColumnInColumnList(columnName){
    for(var i =0; i < columnList.length; i++){
        if( columnList[i].title == columnName)
            return columnList[i];
    }
    return null;
}