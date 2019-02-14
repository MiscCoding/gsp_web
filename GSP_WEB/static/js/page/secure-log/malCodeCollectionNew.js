function downloadExcel(){

    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
//        search_type : $("#search_type").val(),
//        search_source : $("#search_source").val(),
//        search_security_level : $("#search_security_level").val(),
        search_keyword_type : $("#search_keyword_type").val(),
        search_keyword : $("#search_keyword").val(),
        timeFrom : $("#dateFrom").val(),
        timeTo : $("#dateTo").val(),
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
    form.setAttribute('action', "/secure-log/malCodeCollectionNew/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.type = $('#pop_type').val();
        postData.uri = $("#pattern_uri").val();
        postData.detection_source = $("#pop_detection_source").val();
       // postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/secure-log/cnc-manage",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditSubmit (){
//    var _form  = $('#popup-form')
//    _form.parsley().validate();

//    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.seq = $("#pop_seq").val();
//        postData.type = $('#pop_type').val();
//        postData.pattern_uri = $("#pattern_uri").val();
//        postData.detection_source = $("#pop_detection_source").val();
        //postData.source = $("#pop_source").val();
        postData.comment = $('#pop_desc').val();

        var request = $.ajax({
            url:"/secure-log/malCodeCollectionNew/"+ postData.seq,
            type:"PUT",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
//    }

    return false;
}

function showEditDialog(){

    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('수정 할 아이템을 선택 해 주세요');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    $('#pop_seq').val(row.id);
//    $('#pop_type').val(row.rule_type);
//    $('#pattern_uri').val(row.pattern_uri);
    $('#pop_desc').val(row.comment);
//    $("#pop_detection_source").val(row.detection_source);
    //$('#pop_source').val(row.source)
    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();
}

function deleteItem(){

    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('삭제 할 아이템을 선택 해 주세요');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value
    seq = $('#demo-foo-filtering').DataTable().data()[rownum].id;

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/secure-log/malCodeCollectionNew/" + seq,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/secure-log/malCodeCollectionNew/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
//                        d.search_type = $("#search_type").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = String($("#search_keyword").val());

//                        d.search_type = $("#search_type").val();
                        d.search_security_level = $("#search_security_level").val();
                        d.search_keyword_type = $("#search_keyword_type").val();
                        d.search_keyword = $("#search_keyword").val();
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
              $('#divTotal').text("총 "+json.recordsFiltered.toLocaleString() + "건");
            },
            error: function(xhr, error, thrown) {
                alert(error);
                error(xhr, error, thrown);
            },
            dom: 'Bfrtip',
            "pagingType": "full_numbers",
            fixedHeader: true,
            "scrollY" : "750px",
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
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    data : null
                },
                {
                    data : "cre_dt",
                    label: "등록일",
                    mDataProp: 'cre_dt',
                    mRender: function(value) {
                               if(value == null || value == "" || value == ''){
                                  return "";
                                 } else{
                                 return formatDate(value);
//                                   return value.toLocaleDateString();
                                 }
                              }
                },
                {
                    data : "url",
                    label: "URL"
//                    ,
//                    mDataProp: 'url',
//                    mRender: function(value) {
//                                  return value.truncStr(60);
//                              }
                },
                {
                    data : "ip",
                    label: "IP"
                },
                {
                    data : "country_code",
                    label: "국가코드"
                },

                {
                    data : null,
                    label: "파일정보"
                },
                {
                    data : "detect_info",
                    label: "탐지명" //column name changed
                },
                {
                    data : "collect_point",
                    label: "탐지점"
                },
                {
                    data : "comment",
                    label: "비고"
                }
            ],
            columnDefs : [
                {
                    targets : 0,
                    render : function (data, type, row, meta) {

                        var btnHtml = "<input type='checkbox' name='dtSelector' value='"+ meta.row + "'/>";

                        return btnHtml;
                    }
                },
                {
                    "targets" : 1,
                    "render" : function ( data, type,row, meta){
                        var html = '<div style="max-width:630px;word-wrap:break-word">'+data+'</div>';
                        return html;
                    }
                },
                {
                    "targets" : 2,
                    "render" : function ( data, type,row, meta){
                        var uri = row.url;
                        var html = '<div class="syst-sm-bg" data-toggle="tooltip" title="'+ uri +'">' + uri.truncStr(90) + '</div>';
                        return html;
                    }
                },
                {
                    "targets" : 5,
                    "render" : function ( data, type,row, meta){
                        var file_name = row.file_name;
                        var md5 = row.md5;
                        var btnHtml = '<p>File: '+ file_name.truncStr(30) +"<br>MD5: "+ md5.truncStr(40) +"</p>";
                        return btnHtml;
                    }
                },
                {
                    "targets" : 6,
                    "render" : function ( data, type,row, meta){
                        var detectionNames = (row.detect_info).split(',');
                        var stringInMiddle = "";
                        for(var i = 0; i<detectionNames.length; i++)
                        {
                            stringInMiddle += detectionNames[i] + "<br>";
                        }
                        stringInMiddle = stringInMiddle.substring(0, stringInMiddle.length - 4);
                        var btnHtml = '<p>'+ stringInMiddle +"</p>";
                        return btnHtml;
                    }
                },
                {
                    "targets" : 7,
                    "render" : function ( data, type,row, meta){
                        var collectPoints = (row.collect_point).split(',');
                        var stringInMiddle = "";
                        for(var i = 0; i<collectPoints.length; i++)
                        {
                            stringInMiddle += collectPoints[i] + "<br>";
                        }
                        stringInMiddle = stringInMiddle.substring(0, stringInMiddle.length - 4);
                        var btnHtml = '<p>'+ stringInMiddle +"</p>";
                        return btnHtml;
                    }
                }
            ],
            "drawCallback" : function(setting,data){
                    $("input:checkbox").on('click', function() {
                    // in the handler, 'this' refers to the box clicked on
                    var $box = $(this);
                    if ($box.is(":checked")) {
                        // the name of the box is retrieved using the .attr() method
                        // as it is assumed and expected to be immutable
                        var group = "input:checkbox[name='" + $box.attr("name") + "']";
                        // the checked state of the group/box on the other hand will change
                        // and the current value is retrieved using .prop() method
                        $(group).prop("checked", false);
                        $box.prop("checked", true);
                    } else {
                        $box.prop("checked", false);
                    }
                });
            }
        }).on('draw.dt', function(){
            //dtTable.rowsgroup.update();
            $('[data-toggle="tooltip"]').tooltip({html: true});
        });

        // $('#dtData').footable();
        // $("#dtTableToolbar").insertBefore( "#demo-foo-filtering_paginate" );

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
//    if ($('#search_keyword_type').val() === "file_name" && $('#search_keyword').val() != ""){
//        return alert("검색타입 선택 하세요!")
//    }
    $('#demo-foo-filtering').DataTable().ajax.reload(function(data){
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
    });
}

String.prototype.truncStr = String.prototype.truncStr ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '&hellip;' : this;
      };

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

        hour = ("0" + hour).slice(-2);
        minutes = ("0" + minutes).slice(-2);
        seconds = ("0" + seconds).slice(-2);


    return [year, month, day].join('-') + " " + [hour, minutes, seconds].join(':');
}