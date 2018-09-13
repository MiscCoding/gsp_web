function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.type = $("#pop_type").val();
        postData.pattern = $("#pop_pattern").val();
        postData.depth = $("#pop_depth").val();
        postData.description = $("#pop_desc").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/rules/crawl",
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
        postData.index = $("#pop_index").val();
        postData.seq = $("#pop_seq").val();
        postData.type = $("#pop_type").val();
        postData.pattern = $("#pop_pattern").val();
        postData.depth = $("#pop_depth").val();
        postData.description = $("#pop_desc").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/rules/crawl",
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

function showEditDialog(id){
    row = $('#demo-foo-filtering').DataTable().data()[id];
    $('#pop_seq').val(row._id);
    $("#pop_index").val(row._index);
    $("#pop_pattern").val(row._source.uri);
    $('#pop_depth').val(row._source.depth);
    $('#pop_desc').val(row._source.desc);
    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();
}

function deleteItem(seq, date){

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');


    if( result) {
        var postData = new Object();
        postData.u_id = seq;
        postData.u_datadate = date;
        var request = $.ajax({
            url: "/rules/crawldelete", //+ seq,
            type: "POST",
            data:postData,
            success: function (data, status) {
                //alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
            },
            error: function (err, status) {
                alert(err.responseText);
                $('#demo-foo-filtering').DataTable().ajax.reload();
            }
        });
    }

    return false;
}

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/rules/crawl/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.pageLength = $("#perpage").val();
                        d.search_source = $("#search_source").val();
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
            serverSide: true,
            pageLength: 10,
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
                    data : "_source.uri",
                    label: "크롤링 URI",
                    width: "30%"
                },{
                    data : "_source.depth",
                    label: "Depth"
                },{
                    data : "_source.desc",
                    label: "설명"
                },{
                    data : "_source.register_path_text",
                    label: "패턴 등록경로"
                },{
                    data : "_source.min_timestamp",
                    label: "등록일"
                },{
                    data : null,
                    label: "관리"
                }
            ],
            columnDefs : [
                {
                    "targets" : 0,
                    "width" : "30%",
                    "render" : function(data,type, row,meta){
                        var btnHtml = '<div style="max-width:740px;word-wrap:break-word">'+ row._source.uri+'</div>';
                        return btnHtml;
                    }
                },
                {
                    "targets" : 1,
                    "width" : "10%"
                },
                {
                    "targets" : 2,
                    "width" : "25%"
                },
                {
                  "targets" : 4,
                  "render" : function(data,type,row,meta){
                      var date = new Date(row._source["min_timestamp"]);
                      return date.toLocaleDateString() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
                  }
                },
                {
                    "targets": -1,
                    "width" : "15%",
                    "class" : "syst-btn",
                    "render" :function (data, type, row, meta){
                        var date = new Date(row._source["min_timestamp"]);
                        var dataday = date.getFullYear()+'.'+('0' + (date.getMonth() + 1)).slice(-2)+'.'+('0' + date.getDate()).slice(-2);
                        var btnHtml = '';
                        if(row._source.register_path == '005') {

                            btnHtml += '<p class="syst-cans" onclick="deleteItem(\''+row._id+'\'' + ', \'' + dataday+'\')" >삭제</p>'
                        }
                        return btnHtml;
                    }
                }
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
    $('#demo-foo-filtering').DataTable().ajax.reload(function(data){
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
    });
}

function handleBtnSaveClick(){
    var isOk = confirm('저장 하시겠습니까?')
    if (isOk){
        var _form  = $('#formSetting')
        _form.parsley().validate();

        if( _form.parsley().validationResult) {

            var postData = new Object();
            postData.extionsions = $('#input_ext').val();
            postData.depth = $('#input_depth').val();
            postData.maxsize = $('#input_size').val();
            postData.timeout = $('#input_timeout').val();

            var request = $.ajax({
                url:"/system/crawling",
                type:"POST",
                data:postData,
                success: function(data, status){
                    alert('저장 완료.');
                },
                error: function(err, status, err2){
                    alert(err.responseJSON.message);
                }
            });
        }

        return false;
    }
}