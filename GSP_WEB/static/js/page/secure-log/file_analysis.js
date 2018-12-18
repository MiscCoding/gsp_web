function downloadExcel(){

    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
        search_type : $("#search_type").val(),
        search_security_level : $("#search_security_level").val(),
        search_keyword_type : $("#search_keyword_type").val(),
        search_keyword : $("#search_keyword").val(),
        timeFrom : $("#dateFrom").val(),
        timeTo : $("#dateTo").val()
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
    form.setAttribute('action', "/secure-log/file-anlaysis/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
    $("#filedownloadBtn").prop('disabled', true);
    setTimeout(function(){
        $("#filedownloadBtn").prop('disabled', false);
    }, 5000);

}

function GetList(){
    if ($('#demo-foo-filtering_paginate').length !== 0) {
        dtTable = $('#demo-foo-filtering_paginate').DataTable({
                ajax: {
                    url:"/secure-log/file-anlaysis/getlist",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_type = $("#search_type").val();
                        d.search_security_level = $("#search_security_level").val()
                        d.search_keyword_type = $("#search_keyword_type").val()
                        d.search_keyword = $("#search_keyword").val();
//                        d.search_keyword = d.search_keyword.replace(/^https?:\/\//, '');
//                        d.search_keyword = d.search_keyword.replace (/-/g, "*");
//                        d.search_keyword = d.search_keyword.replace (/_/g, "*");
                        d.search_keyword = d.search_keyword.replace (/\//g, "*");
                       // d.search_keyword = d.search_keyword.replace (/[.]/g, "?");
                        d.timeFrom = $("#dateFrom").val();
                        d.timeTo = $("#dateTo").val();
                    }
                },
                dataFilter: function(data){
                var json = jQuery.parseJSON( data );
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                json.data = json.list;

                return JSON.stringify( json ); // return JSON string
            },
            "initComplete": function(settings, json){
              $('#divTotal').text("총 "+json.recordsFiltered + "건");
            },
            error: function(xhr, error, thrown) {
                alert(error);
                error(xhr, error, thrown);
            },
            dom: 'Bfrtip',
            "pagingType": "full_numbers",
            fixedHeader: true,
            "scrollY" : "700px",
            serverSide: true,
            pageLength: $("#perpage").val(),
            bLengthChange: false,
            processing: true,
            searching: false,
            sort: false,
            paging: true,
            info: false,
            deferRender: true,
            responsive: true,
            autoWidth : true,
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                    {
                        data : "category",
                        label: "카테고리"
                    },
                    {
                        data : "collect_uri",
                        label: "다운로드 경로"
                    },
                    {
                        data : "md5",
                        label: "해시값"
                    },
                    {
                        data : "file_name",
                        label: "파일명"
                    },
                    {
                        data : "data_from",
                        label: "분석 장비"
                    },
                    {
                        data : "result",
                        label: "악성여부"
                    },
                    {
                        data : "timestamp",
                        label: "등록일"
                    }
//                    ,
//                    {
//                        data : "file_name",
//                        label: "파일명"
//                    },
//                    {
//                        data : "result",
//                        label: "분석 결과"
//                    }


//                    {
//                        data : "timestamp",
//                        label: "등록일"
//                    },{
//                        data : "category",
//                        label: "카테고리"
//                    },{
//                        data : "file_name",
//                        label: "파일명"
//                    },{
//                        data : "md5",
//                        label: "해시값"
//                    },{
//                        data : "collect_uri",
//                        label: "다운로드 경로"
//                    },{
//                        data : "data_from",
//                        label: "분석 장비"
//                    },{
//                        data : "result",
//                        label: "분석 결과"
//                    }

//                {
//                    data : "timestamp",
//                    label: "등록일"
//                },{
//                    data : "file_name",
//                    label: "파일명"
//                },{
//                    data : "md5",
//                    label: "해시값"
//                },{
//                    data : "collect_uri",
//                    label: "다운로드 경로"
//                },{
//                    data : "category",
//                    label: "카테고리"
//                },{
//                    data : "data_from",
//                    label: "분석 장비"
//                },{
//                    data : "result",
//                    label: "분석 결과"
//                }
            ]
        });

        //$('#dtData').footable();
        //$("#dtTableToolbar").insertBefore( "#demo-foo-filtering_paginate" );

    }
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

var handleDataTableDefault = function() {
    GetList();
};

function DatatableReload(){
    if ($('#search_keyword_type').val() === "file_name" && $('#search_keyword').val() != ""){
        return alert("검색타입 선택 하세요!")
    }
    if ($('#search_type').val() === ""){
        return alert("장비타입 선택 하세요!")
    }

    $("#searchBtn").prop('disabled', true);
    setTimeout(function(){
        $("#searchBtn").prop('disabled', false);
    }, 5000);

    $('#demo-foo-filtering_paginate').DataTable().ajax.reload(function(data){
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
        dtTable.page.len($("#perpage").val()).draw();
    });
}

function convertLocalDateToUTCDate(date, toUTC) {
    date = new Date(date);
    //Local time converted to UTC
    console.log("Time: " + date);
    var localOffset = date.getTimezoneOffset() * 60000;
    var localTime = date.getTime();
    if (toUTC) {
        date = localTime + localOffset;
    } else {
        date = localTime - localOffset;
    }
    date = new Date(date);
    console.log("Converted time: " + date);
    return date;
}

function formatDate(date) {
    date = date.replace(" GMT", "");
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    var hour = d.getHours(),
        minutes = d.getMinutes(),
        seconds = d.getSeconds();

    return [year, month, day].join('-') + " " + [hour, minutes, seconds].join(':');
}