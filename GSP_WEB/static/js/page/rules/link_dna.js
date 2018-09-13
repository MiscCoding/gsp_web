function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var pattern_ui = makePostData();

        var json = JSON.stringify(pattern_ui);
        var postData = Object();
        postData.group_code = $("#search_profile_group").val();
        postData.name = $("#search_profile_name").val();
        postData.description = $("#search_profile_description").val();
        postData.pattern_ui = json;

        var request = $.ajax({
            url:"/rules/profile",
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

        var pattern_ui = makePostData();

        var json = JSON.stringify(pattern_ui);
        var postData = Object();
        postData.group_code = $("#search_profile_group").val();
        postData.name = $("#search_profile_name").val();
        postData.description = $("#search_profile_description").val();
        postData.pattern_ui = json;
        var request = $.ajax({
            url:"/rules/profile/"+ $('#pop_seq').val(),
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
    json = JSON.parse(row.pattern_ui);

    $('#pop_seq').val(row.seq);
    $("#search_profile_name").val(row.name);
    $("#search_profile_description").val(row.description);

     var _keys = Object.keys(json);
     for( i =0 ; i < _keys.length; i++)
     {
         $("#"+_keys[i]).val(json[_keys[i]]);
     };

    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();
}

function deleteItem(seq){

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/rules/profile/" + seq,
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
                    url:"/rules/linkdna/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.group_code = $("#search_type").val();
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
                    data : "group_name",
                    label: "패턴명"
                },
                {
                    data : "name",
                    label: "패턴명"
                },{
                    data : "description",
                    label: "설명"
                },{
                    data : "cre_dt",
                    label: "등록일"
                },{
                    data : null,
                    label: "관리"
                }
            ],
            columnDefs : [
                {
                    "targets": -1,
                    "class" : "syst-btn",
                    "render" :function (data, type, row, meta){
                        var btnHtml = '';
                        btnHtml += '<p class="syst-ok back-bg" onclick="showEditDialog(\'' + meta.row + '\')">수정</p>';
                        btnHtml += '<p class="syst-cans" onclick="deleteItem('+row.seq+')" >삭제</p>'
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
    GetGroupList();
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

function GetGroupList(){
    if ($('#demo-foo-filtering2').length !== 0) {
        dtTable = $('#demo-foo-filtering2').DataTable({
                ajax: {
                    url:"/rules/linkdna/group/list",
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
              $('#divGroupTotal').text("총 "+json.recordsFiltered.toLocaleString() + "건");
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
                    data : "name",
                    label: "패턴명"
                },{
                    data : "description",
                    label: "설명"
                },{
                    data : "cre_dt",
                    label: "등록일"
                },{
                    data : null,
                    label: "관리"
                }
            ],
            columnDefs : [
                {
                    "targets": -1,
                    "class" : "syst-btn",
                    "render" :function (data, type, row, meta){
                        var btnHtml = '';
                        btnHtml += '<p class="syst-ok back-bg" onclick="showEditGroupDialog(\'' + meta.row + '\')">수정</p>';
                        btnHtml += '<p class="syst-cans" onclick="deleteGroupItem('+row.seq+')" >삭제</p>'
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

function handleAddGroupSubmit (){
    var _form  = $('#formProfileGroup')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        if( $("#pop-time-gubun").val() != '' && $("#pop-time-value").val().trim() == '' ){
            alert('주기를 입력 해 주세요');
            $("#pop-time-value").focus();
            return false;
        }

        var postData = Object();
        postData.name = $("#pop-group-name").val();
        postData.description = $("#pop-group-desc").val();
        postData.time_gubun = $("#pop-time-gubun").val();
        postData.time_value = $("#pop-time-value").val();

        var request = $.ajax({
            url:"/rules/linkdna/group",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering2').DataTable().ajax.reload();
                $('#modal-Profile-Group').modal('toggle');
                reloadGroup();
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditGroupSubmit (){
    var _form  = $('#formProfileGroup')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {
        if( $("#pop-time-gubun").val() != '' && $("#pop-time-value").val().trim() == '' ){
            alert('주기를 입력 해 주세요');
            $("#pop-time-value").focus();
            return false;
        }


        var pattern_ui = makePostData();

        var json = JSON.stringify(pattern_ui);
        var postData = Object();
        postData.name = $("#pop-group-name").val();
        postData.description = $("#pop-group-desc").val();
        postData.time_gubun = $("#pop-time-gubun").val();
        postData.time_value = $("#pop-time-value").val();

        var request = $.ajax({
            url:"/rules/linkdna/group/"+ $('#pop_group_seq').val(),
            type:"PUT",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering2').DataTable().ajax.reload();
                $('#modal-Profile-Group').modal('toggle');
                reloadGroup();
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function showEditGroupDialog(id){
    row = $('#demo-foo-filtering2').DataTable().data()[id];

    $('#pop_group_seq').val(row.seq);
    $("#pop-group-name").val(row.name);
    $("#pop-group-desc").val(row.description);
    $("#pop-time-gubun").val(row.time_gubun);
    $("#pop-time-gubun").change();
    $("#pop-time-value").val(row.time_value);

    $('#btnAddGroupSubmit').hide();
    $('#btnEditGroupSubmit').show();
    $('#modal-Profile-Group').modal();
}

function deleteGroupItem(seq){

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/rules/linkdna/group/" + seq,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#demo-foo-filtering2').DataTable().ajax.reload();
                reloadGroup();
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function reloadGroup(){
    var request = $.ajax({
        url: "/rules/linkdna/group/namelist",
        type: "GET",
        success: function (data, status) {
            //alert('success');
            $("#search_profile_group").empty();
            $("#search_type").empty();
            $("#search_type").append( $('<option>', {
                value: '',
                text : '전체'
            }) );

            for(i = 0; i < data['data'].length; i ++) {
                $("#search_profile_group").append($('<option>', {
                    value: data['data'][i].seq,
                    text : data['data'][i].name
                }));

                $("#search_type").append($('<option>', {
                    value: data['data'][i].seq,
                    text : data['data'][i].name
                }));
            }

        },
        error: function (err, status) {
            alert(err.responseText);
        }
    });
}