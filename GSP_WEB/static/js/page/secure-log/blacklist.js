function downloadExcel(){

    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
        search_type : $("#search_type").val(),
        search_source : $("#search_source").val(),
        search_security_level : $("#search_security_level").val(),
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
    form.setAttribute('action', "/secure-log/black-list/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.rule_name = $("#pop_category").val();
        postData.mal_file_name = $("#pop_fname").val();
        postData.pattern = $("#pop_pattern").val();
        postData.uri = $("#pop_url").val();
        postData.analysis_device=$("#pop_description").val();
        postData.detection_source = $("#pop_detection_source").val();
        //postData.size = $("#pop_size").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/secure-log/black-list",
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
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.seq = $("#pop_seq").val();
        //postData.mal_file_name =
        postData.rule_name = $("#pop_category").val();
        postData.mal_file_name = $("#pop_fname").val();
        postData.pattern = $("#pop_pattern").val();
        postData.uri = $("#pop_url").val();
        postData.analysis_device=$("#pop_description").val();
        postData.detection_source = $("#pop_detection_source").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/secure-log/black-list/"+ postData.seq,
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
    }

    return false;
}

function showEditDialog(){
    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('수정 할 아이템을 선택 해 주세요');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    $('#pop_seq').val(row.seq);
    $("#pop_category").val(row.rule_name);
    $("#pop_fname").val(row.mal_file_name);
    $('#pop_pattern').val(row.md5);
    $("#pop_url").val(row.uri);
    $("#pop_description").val(row.analysis_device);
    $("#pop_detection_source").val(row.detection_source);
    //$("#pop_size").val(row.size);
    $('#pop_desc').val(row.description);
    $('#pop_source').val(row.source)
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
    seq = $('#demo-foo-filtering').DataTable().data()[rownum].seq;

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/secure-log/black-list/" + seq,
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
                    url:"/secure-log/black-list/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();

                        d.search_type = $("#search_type").val();
                        d.search_security_level = $("#search_security_level").val()
                        d.search_keyword_type = $("#search_keyword_type").val()
                        d.search_keyword = $("#search_keyword").val();
                        d.timeFrom = $("#dateFrom").val();
                        d.timeTo = $("#dateTo").val();
                    }
                },
                dataFilter: function(data){
                var json = jQuery.parseJSON( data );
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                for(var i = 0; i < json.list.length; i++){
                     json.list[i].uri.truncStr(5)
                }
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
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                  data:null
                },
                {
                    data : "rule_name",
                    label: "카테고리", //New UI requirement, column name changed.
                    mDataProp: 'rule_name',
                    mRender: function(value) {
                                  return value.truncStr(20);
                              }
                },
                {
                    data : "uri",
                    label: "URL", //New UI requirement, column name changed.
                    mDataProp: 'uri',
                    mRender: function(value) {
                                  return value.truncStr(30);
                              }
                },
                {
                    data : "md5",
                    label: "유해파일(MD5)", //New UI requirement, column name changed.
                    mDataProp: 'md5',
                    mRender: function(value) {
                                  return value.truncStr(30);
                              }
                },
                {
                    data : "mal_file_name",
                    label: "파일명", //New UI requirement, column name changed.
                    mDataProp: 'mal_file_name',
                    mRender: function(value) {
                                  return value.truncStr(25);
                              }
                },
                {
                    data : "analysis_device",
                    label: "분석장비"
                },
                {
                    data : "analysis_result",
                    label: "결과"
                },
                {
                    data : "cre_dt",
                    label: "등록일"
                },
                {
                    data : "detection_source",
                    label: "탐지점"
                },
                {
                    data : "description",
                    label: "설명"
                }
            ],
            columnDefs : [
                {
                    targets : 0,
                    render : function (data, type, row, meta) {

                        var btnHtml = "<input type='checkbox' name='dtSelector' value='"+ meta.row + "'/>";

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
                 setTimeout(function(){
                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                 }, 350);
            }
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
    $('#demo-foo-filtering').DataTable().ajax.reload(function(data){
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
    });
}

function getReadableFileSizeString(fileSizeInBytes) {
    var i = -1;
    var byteUnits = [' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
    do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
    } while (fileSizeInBytes > 1024);

    return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
};

String.prototype.truncStr = String.prototype.truncStr ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '&hellip;' : this;
      };