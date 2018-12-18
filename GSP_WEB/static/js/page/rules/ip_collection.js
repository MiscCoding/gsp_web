function isFileValidate(){
    if ($("#pop_file").val() == '' )
        return false;
    else
        return true;
}

function fileSubmit(){

//    var _form  = $('#formUpload');
//    _form.parsley().validate();

//    if( _form.parsley().validationResult) {

        if( !isFileValidate())
        {
            alert("업로드할 파일을 선택 해 주세요");
            return false;
        }

        var formData = new FormData($("#formUpload")[0]);
//        formData.append("name", $("#pop_name").val());
//        formData.append("target_type", $("#pop_link").val()[0]);
//        formData.append("target_seq", $("#pop_link").val().substr(1));
        formData.append("file", $("#pop_file")[0].files[0]);

        var request = $.ajax({
            url:"/rules/ip-collection/uploadlist",
            type:"POST",
            data:formData,
            processData:false,
            contentType: false,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup-file').modal('toggle');
                $('#pop_file_name').val("");
                $('.filebox .upload-hidden').val("");

            },
            error: function(err, status, err2){
                 $('#demo-foo-filtering').DataTable().ajax.reload();
                 $('#pop_file_name').val("");
                 $('.filebox .upload-hidden').val("");
                 $('#modal-popup-file').modal('toggle');
                 alert(err.responseJSON.message);


            }
        });
//    }

//    return false;

}

function downloadExcel(){

    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
        //search_type : $("#search_type").val(),
        //search_security_level : $("#search_security_level").val(),
        //search_keyword_type : $("#search_keyword_type").val(),
        search_keyword : $("#search_keyword").val(),
        //timeFrom : $("#dateFrom").val(),
        //timeTo : $("#dateTo").val()
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
    form.setAttribute('action', "/rules/ip-collection/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.pattern = $("#pop_pattern").val();
//        postData.size = $("#pop_size").val();
//        postData.source = $("#pop_source").val();
        postData.mask = $("#pop_mask").val();
        postData.detection_point = $('#pop_detection_point').val();
        postData.etc = $('#pop_etc').val();
        postData.description = $("#pop_desc").val();
        postData.use_yn = $('#pop_use_yn').val();
       // postData.url = $('#pop_url').val();

        var request = $.ajax({
            url:"/rules/ip-collection",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
            },
            error: function(err, status, err2, temp){
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
        //postData.size = $('#pop_size').val();
        postData.pattern = $("#pop_pattern").val();
        postData.mask = $("#pop_mask").val();
        postData.detection_point = $("#pop_detection_point").val();
        postData.etc = $('#pop_etc').val();
        postData.description = $("#pop_desc").val();
        postData.use_yn = $('#pop_use_yn').val();

//        postData.source = $("#pop_source").val();
//        postData.desc = $('#pop_desc').val();
//        postData.url = $('#pop_url').val();

        var request = $.ajax({
            url:"/rules/ip-collection/"+ postData.seq,
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
    if($('input[name=editFeature]input:checked').length == 0){
        alert('수정할 아이템을 선택하세요!');
        return
    }

    var rownum = $('input[name=editFeature]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    $('#pop_seq').val(row.seq);
    $('#pop_pattern').val(row.ip);
    $("#pop_mask").val(row.mask);
    $('#pop_detection_point').val(row.detection_point);
    $('#pop_etc').val(row.etc);
    $('#pop_desc').val(row.description);
    $('#pop_use_yn').val(row.use_yn);
//    $('#pop_desc').val(row.description);
//    $('#pop_url').val(row.url);
    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();
}

function deleteItem(){

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');
    var rownum = $('input[name=editFeature]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    if( result) {

        var request = $.ajax({
            url: "/rules/ip-collection/" + row.seq,
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
                    url:"/rules/ip-collection/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();
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
            "scrollY" : "600px",
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
                    data : "ip",
                    label: "패턴(URI)"
                },
                {
                    data : "mask",
                    label: "패턴(URI)"
                },
//                {
//                    data : "etc",
//                    label: "비고"
//                },
                {
                    data : "description",
                    label: "설명"
                },
                {
                    data : "use_yn",
                    label: "사용여부"
                },
                {
                    data : "cre_dt",
                    label: "등록일",
                    mDataProp: 'cre_dt',
                    mRender: function(value) {
                             return formatDate(value);
                             }
                }
                
            ],
            columnDefs : [
                /*{
                    "targets": -1,
                    "class" : "syst-btn", 
                    "render" :function (data, type, row, meta){
                        var btnHtml = '';
                        //btnHtml += "<input type=\"checkbox\" class=\"syst-cans\" id=\"horns\" name=\"feature\" value=\"horns\" />"
                        btnHtml += '<p class="syst-ok back-bg" onclick="showEditDialog(\'' + meta.row + '\')">수정</p>';
                        btnHtml += '<p class="syst-cans" onclick="deleteItem('+row.seq+')" >삭제</p>';
                        return btnHtml;
                    }
                },*/
                {
                    "targets": 0,
                    orderable: false,
                    className: 'select-checkbox',
                   "render" :function (data, type, row, meta){
                        var btnHtml = '';
                        btnHtml = '<input type="checkbox" id="horns" name="editFeature" value="'+meta.row+'"/>';
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

function getReadableFileSizeString(fileSizeInBytes) {
    var i = -1;
    var byteUnits = [' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
    do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
    } while (fileSizeInBytes > 1024);

    return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
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

    return [year, month, day].join('-') + "<br>" + [hour, minutes, seconds].join(':');
}