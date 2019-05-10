function isFileValidate(){
    if ($("#pop_file").val() == '' )
        return false;
    else
        return true;
}

function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
//        postData.type = $("#pop_type").val();
        postData.url = $("#pop_url_addr").val();
        postData.depth = $("#pop_depth").val();
        postData.comment = $("#pop_desc").val();
//        postData.source = $("#pop_source").val();
//        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/rules/crawl",
            type:"POST",
            data:postData,
            success: function(data, status){
                DatatableReload();
                $('#modal-popup').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
                 DatatableReload();
            }
        });
    }

    return false;
}

function downloadExcelSample(){

    data = {
        sample: "yes"

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
    form.setAttribute('action', "/rules/crawl/sample-excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

function fileSubmit(){


        if( !isFileValidate())
        {
            alert("업로드할 파일을 선택 해 주세요");
            return false;
        }

        var formData = new FormData($("#formUpload")[0]);
        $body.addClass("loading");

        formData.append("file", $("#pop_file")[0].files[0]);
//        var nowTime = new Date().getTime();
//        formData.append("timestamp" nowTime);

        $('#modal-popup-file').modal('toggle');
        var request = $.ajax({
            url:"/rules/crawl/batchUpload",
            type:"POST",
            data:formData,
            processData:false,
            contentType: false,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();

                $('#pop_file_name').val("");
                $('.filebox .upload-hidden').val("");
                $body.removeClass("loading");

            },
            error: function(err, status, err2){
                 $('#demo-foo-filtering').DataTable().ajax.reload();
                 $('#pop_file_name').val("");
                 $('.filebox .upload-hidden').val("");
//                 $('#modal-popup-file').modal('toggle');
                 alert(err.responseJSON.message);
                 $body.removeClass("loading");
            }
        });
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

function pageMoveFeature(){
    $body.addClass("loading");
    var pageIndexValue = $('#page_move_no_input').val();
    var table = $('#demo-foo-filtering').DataTable();
    var currentPageindex = table.page.info().page;
    var totalPages = table.page.info().pages;

    if(pageIndexValue <= 1)
    {
        pageIndexValue = 1
    }
    if(pageIndexValue >= (totalPages))
    {
        pageIndexValue = (totalPages);
    }

    $('#page_move_no_input').val("");

    table.page(pageIndexValue-1).draw( 'page' );
//    $body.removeClass("loading");

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
            fixedHeader: true,
            pageLength: $("#perpage").val(),
            bLengthChange: false,
            processing: true,
            searching: false,
            sort: false,
            paging: true,
            info: false,
            ordering: false,
            deferRender: true,
            responsive: true,
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
//                {
//                    data : "_source.uri",
//                    label: "크롤링 URI",
//                    width: "30%"
//                },{
//                    data : "_source.depth",
//                    label: "Depth"
//                },{
//                    data : "_source.desc",
//                    label: "설명"
//                },{
//                    data : "_source.register_path_text",
//                    label: "패턴 등록경로"
//                },{
//                    data : "_source.min_timestamp",
//                    label: "등록일"
//                },{
//                    data : null,
//                    label: "관리"
//                }
                {
                    data : "url",
                    label: "크롤링 URI",
                    width: "30%"
                },{
                    data : "depth",
                    label: "Depth"
                },{
                    data : "comment",
                    label: "설명"
                },
                {
                    data : "register_from",
                    label: "패턴 등록경로"
                },
                {
                    data : "result_yn",
                    label: "완료여부"
                },
                {
                    data : "register_date",
                    label: "등록일"
                },
                {
                    data : null,
                    label: "관리"
                }
            ],
            columnDefs : [
                {
                    "targets" : 0,
                    "width" : "30%",
                    "render" : function(data,type, row,meta){
                        var btnHtml = '<div style="max-width:740px;word-wrap:break-word">'+ row.url+'</div>';
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
                          var completionResult = row.result_yn;
                          if (completionResult == 'y'){
                            return "완료";
                          } else {
                            return "미완료";
                          }

                      }

                 },
                {
                  "targets" : 5,
                  "render" : function(data,type,row,meta){
//                      var date = new Date(row["register_date"]);
//                      return date.toLocaleDateString() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
                      return formatDate(row["register_date"]);
                  }
                },
                {
                    "targets": -1,
                    "width" : "15%",
                    "class" : "syst-btn",
                    "render" :function (data, type, row, meta){
                        var date = new Date(row["register_date"]);
                        var dataday = date.getFullYear()+'.'+('0' + (date.getMonth() + 1)).slice(-2)+'.'+('0' + date.getDate()).slice(-2);
                        var btnHtml = '';
//                        if(row._source.register_path == '사용자 입력') {
//
//                            btnHtml += '<p class="syst-cans" onclick="deleteItem(\''+row._id+'\'' + ', \'' + dataday+'\')" >삭제</p>'
//                        }
                        if(row) {

                            btnHtml += '<p class="syst-cans" onclick="deleteItem(\''+row.idx+'\'' + ', \'' + dataday+'\')" >삭제</p>'
                        }
                        return btnHtml;
                    }
                }
            ],
            "drawCallback" : function(setting,data){
//                    $("input:checkbox").on('click', function() {
//                    // in the handler, 'this' refers to the box clicked on
//                    var $box = $(this);
//                    if ($box.is(":checked")) {
//                        // the name of the box is retrieved using the .attr() method
//                        // as it is assumed and expected to be immutable
//                        var group = "input:checkbox[name='" + $box.attr("name") + "']";
//                        // the checked state of the group/box on the other hand will change
//                        // and the current value is retrieved using .prop() method
//                        $(group).prop("checked", false);
//                        $box.prop("checked", true);
//                    } else {
//                        $box.prop("checked", false);
//                    }
//                });
                $body.removeClass("loading");
                setTimeout(function(){
                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                        $("#chkBoxes").removeClass("sorting_asc");
                }, 350);

                var table = $('#demo-foo-filtering').DataTable();
                var currentPageindex = table.page.info().page;
                var totalPages = table.page.info().pages;

//
                $('#demo-foo-filtering_next').on( 'click', function () {
                       $body.addClass("loading");
                       var nextPageIndex = currentPageindex + 1;
                       if(nextPageIndex >= totalPages){
                          nextPageIndex = totalPages - 1;
                       }
                       table.page(nextPageIndex).draw( 'page' );
                });

                 $('#demo-foo-filtering_previous').on( 'click', function () {
                        $body.addClass("loading");
                        var previousPageIndex = currentPageindex - 1;
                        if (previousPageIndex < 0){
                            previousPageIndex = 0;
                        }
                        table.page(previousPageIndex).draw( 'page' );
                 });
            }
        }).on('error.dt', function(e, settings, technote, message){
            $body.removeClass("loading");
            alert("MySQL connection timeout error, or  Cannot retrieve data from MySQL ");
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
            postData.removalPeriod = $('#removal_time_period').val();

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