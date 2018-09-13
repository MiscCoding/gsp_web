
function handleAddWhiteIPSubmit (){
    var _form  = $('#formWhiteIP')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.ip = $('#pop-white-ip').val();
        postData.desc = $('#pop-white-desc').val();

        var request = $.ajax({
            url:"/system/ip-white",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#dtWhiteIP').DataTable().ajax.reload();
                $('#modal-WhiteList').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditWhiteIPSubmit (){
    var _form  = $('#formWhiteIP')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.ip = $('#pop-white-ip').val();
        postData.desc = $('#pop-white-desc').val();

        var request = $.ajax({
            url:"/system/ip-white/"+ postData.ip,
            type:"PUT",
            data:postData,
            success: function(data, status){
                $('#dtWhiteIP').DataTable().ajax.reload();
                $('#modal-WhiteList').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleAddBlackIPSubmit (){
    var _form  = $('#formBlackIP')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.ip = $('#pop-black-ip').val();
        postData.desc = $('#pop-black-desc').val();

        var request = $.ajax({
            url:"/system/ip-black",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#dtBlackIP').DataTable().ajax.reload();
                $('#modal-BlackList').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditBlackIPSubmit (){
    var _form  = $('#formBlackIP')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.ip = $('#pop-black-ip').val();
        postData.desc = $('#pop-black-desc').val();

        var request = $.ajax({
            url:"/system/ip-black/"+postData.ip,
            type:"PUT",
            data:postData,
            success: function(data, status){
                $('#dtBlackIP').DataTable().ajax.reload();
                $('#modal-BlackList').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleAddAccountSubmit(){
    var _form  = $('#formAddAccount')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.account = $('#id').val();
        postData.password = $('#password').val();
        postData.email = $('#email').val();
        postData.mobile = $('#mobile').val();
        postData.role = $('#role').val();
        postData.culture = $('#culture').val();
        postData.comment = $('#comment').val();

        var request = $.ajax({
            url:"/system/account/"+$('#id').val(),
            type:"POST",
            data:postData,
            success: function(data, status){
                //alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-Add').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
};

function handleEditAccountSubmit(){
    var _form  = $('#formAddAccount')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.account = $('#id').val();
        postData.password = $('#password').val();
        postData.email = $('#email').val();
        postData.mobile = $('#mobile').val();
        postData.role = $('#role').val();
        postData.culture = $('#culture').val();
        postData.comment = $('#comment').val();
        $('#formAddAccount').parsley().reset();

        var request = $.ajax({
            url:"/system/account/"+$('#id').val(),
            type:"PUT",
            data:postData,
            success: function(data, status){
                alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-Add').modal('toggle');
            },
            error: function(err, status){
                 alert(err.responseText);
                 $('#modal-Add').modal('toggle');
            }
        });
    }

    return false;
};

var handleDataTableDefault = function() {
    GetAccountList();
    GetWhiteList();
    GetBlackList();
};

function deleteAccount(id){

    var result = confirm('해당 계정을 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/system/account/" + id,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
                if( my_id == id.trim()) {
                    window.location.assign('/login');
                }
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function editAccount(id){
    row = $('#demo-foo-filtering').DataTable().data()[id];
    $('#id').prop('disabled', true);
    $('#id').val(row['id']);
    $('#password').val('');
    $('#passwordConfirm').val('');
    $('#password').attr('data-parsley-required',false);
    $('#email').val(row['email']);
    $('#mobile').val(row['mobile']);
    $('#role').val(row['role_id']);
    $('#culture').val(row['culture']);
    $('#comment').val(row['comment']);
    $('#btnAddAccountSubmit').hide();
    $('#btnEditAccountSubmit').show();
    $('#modal-Add').modal();
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

function GetAccountList(){
    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: "/system/account/accountlist",
                dataFilter: function(data){
                var json = jQuery.parseJSON( data );
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                json.data = json.list;

                return JSON.stringify( json ); // return JSON string
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
            paging: false,
            info: false,
            deferRender: true,
            responsive: true,
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    data : "id",
                    label: "id"
                },{
                    data : "email",
                    label: "email"
                },{
                    data : "mobile",
                    label: "mobile"
                },{
                    data : "role_id",
                    label: "권한",
                    render : function(data, type, row){
                        if(data == "002")
                            return "읽기전용";
                        else if (data == "003")
                            return "모니터링";
                        else if(data == "001")
                            return "모든권한";
                        else
                            return "차단";
                    }
                },{
                    data : "culture",
                    label: "문화권",
                    render : function(data, type, row){
                        if(data == "en-US")
                            return "영어";
                        else if (data == "ja-JP")
                            return "일본어";
                        else
                            return "한국어";
                    }
                },{
                    data : "comment",
                    label: "설명"
                },{
                    data : null,
                    label: "관리"
                }
            ],
            columnDefs : [ {
                "targets": -1,
                "class" : "syst-btn",
                "render" :function (data, type, row, meta){
                    html = '<p class="syst-ok back-bg" onclick="editAccount(\''+meta.row+'\')">수정</p>';
                    if ( role_id == "001" )
                        html += '<p class="syst-cans" onclick="deleteAccount(\''+row.id+' \')" >삭제</p>';
                    return html;
                }
            } ]
        });

        //$('#dtData').footable();
        $("#dtTableToolbar").insertBefore( "#demo-foo-filtering_paginate" );

    }
}

function GetWhiteList(){
    if ($('#dtWhiteIP').length !== 0) {
        dtTable = $('#dtWhiteIP').DataTable({
            ajax: "/system/ip-white/whitelist",
            dataFilter: function (data) {
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                json.data = json.list;

                return JSON.stringify(json); // return JSON string
            },
            error: function (xhr, error, thrown) {
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
            paging: false,
            info: false,
            deferRender: true,
            responsive: true,
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    data: "ip",
                    label: "IP"
                }, {
                    data: "description",
                    label: "설명"
                }, {
                    data: null,
                    label: "관리"
                }
            ],
            columnDefs: [{
                "targets": -1,
                "class": "syst-btn",
                "render": function (data, type, row, meta) {
                    return '<p class="syst-ok back-bg" onclick="editWhiteList(\'' + meta.row + '\')">수정</p><p class="syst-cans" onclick="deleteWhiteList(\'' + row.ip + ' \')" >삭제</p>'
                }
            }]
        });
    }
}

function deleteWhiteList(ip){

    var result = confirm('해당 IP를 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/system/ip-white/" + ip,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                $('#dtWhiteIP').DataTable().ajax.reload();
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function editWhiteList(id){
    row = $('#dtWhiteIP').DataTable().data()[id];
    $('#pop-white-ip').prop('disabled', true);
    $('#pop-white-ip').val(row['ip']);
    $('#pop-white-desc').val(row['description']);
    $('#btnWhiteIPAddSubmit').hide();
    $('#btnWhiteIPEditSubmit').show();
    $('#modal-WhiteList').modal();
}

function showWhiteListModal(){
    row = $('#dtWhiteIP').DataTable().data()[id];
    $('#pop-white-ip').prop('disabled', false);
    $('#pop-white-ip').val('');
    $('#pop-white-desc').val('');
    $('#btnWhiteIPAddSubmit').show();
    $('#btnWhiteIPEditSubmit').hide();
    $('#modal-WhiteList').modal();
}

function GetBlackList(){
    if ($('#dtBlackIP').length !== 0) {
        dtTable = $('#dtBlackIP').DataTable({
            ajax: "/system/ip-black/blacklist",
            dataFilter: function (data) {
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                json.data = json.list;

                return JSON.stringify(json); // return JSON string
            },
            error: function (xhr, error, thrown) {
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
            paging: false,
            info: false,
            deferRender: true,
            responsive: true,
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    data: "ip",
                    label: "IP"
                }, {
                    data: "description",
                    label: "설명"
                }, {
                    data: null,
                    label: "관리"
                }
            ],
            columnDefs: [{
                "targets": -1,
                "class": "syst-btn",
                "render": function (data, type, row, meta) {
                    return '<p class="syst-ok back-bg" onclick="editBlackList(\'' + meta.row + '\')">수정</p><p class="syst-cans" onclick="deleteBlackList(\'' + row.ip + ' \')" >삭제</p>'
                }
            }]
        });
    }
}

function deleteBlackList(ip){

    var result = confirm('해당 IP를 삭제 하시겠습니까?');

    if( result) {

        var request = $.ajax({
            url: "/system/ip-black/" + ip,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                $('#dtBlackIP').DataTable().ajax.reload();
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function editBlackList(id){
    row = $('#dtBlackIP').DataTable().data()[id];
    $('#pop-black-ip').prop('disabled', true);
    $('#pop-black-ip').val(row['ip']);
    $('#pop-black-desc').val(row['description']);
    $('#btnBlackIPAddSubmit').hide();
    $('#btnBlackIPEditSubmit').show();
    $('#modal-BlackList').modal();
}

function showBlackListModal(){
    $('#pop-black-ip').prop('disabled', false);
    $('#pop-black-ip').val('');
    $('#pop-black-desc').val('');
    $('#btnBlackIPAddSubmit').show();
    $('#btnBlackIPEditSubmit').hide();
    $('#modal-BlackList').modal();
}

function ChangeIpAllowSetting(value){

    var PostData = Object();
    if( value == "black") {
        PostData.value = "black";
        PostData.description = "모두 허가하고 해당 IP만 차단한다.";
    }
    else {
        PostData.value = "white";
        PostData.description = "모두 차단하고 해당 IP만 허용한다.";
    }

    var request = $.ajax({
            url: "/system/ip-allow",
            type: "POST",
            data: PostData,
            success: function (data, status) {
                //alert('success');
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });

    return false;
}