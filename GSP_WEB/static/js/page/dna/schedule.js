function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.dna_id = $("#pop_dna").val();
        postData.desc = $('#pop_desc').val();
        postData.cycle_value = $('#pop_cycle_value').val();
        postData.cycle_opt = $('#pop_cycle_opt').val();
        postData.start_time = $("#pop_start_time").val();
        postData.filter_ip = $("#pop_filter_ip").val();
        postData.filter_data_type = $('#pop_filter_data_type').val();

        var request = $.ajax({
            url:"/dna/schedule",
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
        postData.seq = $('#pop_seq').val();
        postData.dna_id = $("#pop_dna").val();
        postData.desc = $('#pop_desc').val();
        postData.cycle_value = $('#pop_cycle_value').val();
        postData.cycle_opt = $('#pop_cycle_opt').val();
        postData.start_time = $("#pop_start_time").val();
        postData.filter_ip = $("#pop_filter_ip").val();
        postData.filter_data_type = $('#pop_filter_data_type').val();

        var request = $.ajax({
            url:"/dna/schedule/"+ postData.seq,
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

function restartRequestSubmit(id){
        $body.addClass("loading");
        var postData = new Object();
        postData.seq = id;


        var request = $.ajax({
            url:"/dna/scheduleRestart/"+ postData.seq,
            type:"PUT",
            data:postData,
            success: function(data, status){

                $('#bt-' + id).unbind( "click");
                $('#bt-' + id).text("요청중");
                $('#bt-' + id).css("background-color", "#A9A9A9");
                $body.removeClass("loading");
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
                 $body.addClass("loading");
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
    $("#pop_dna").val(row.dna_id);
    $('#pop_desc').val(row.description);
    $('#pop_cycle_value').val(row.cycle[0]);
    $('#pop_cycle_opt').val(row.cycle.substr(1,row.cycle.length-1));
    $("#pop_start_time").val(row.start_time);
    $("#pop_filter_ip").val(row.filter_ip);
    $('#pop_filter_data_type').val(row.filter_data_type)
    $('#popup-form').parsley().reset();
    $("#btnAddSubmit").hide();
    $("#btnEditSubmit").show();
    $(".xdsoft_datetimepicker").css("z-index", "9999999");
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
            url: "/dna/schedule/" + seq,
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
                    url:"/dna/schedule/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_type = $("#search_type").val();
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
            "scrollY" : "750px",
            autoWidth : true,
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
                    data : "id",
                    label: "ID"
                },{
                    data : "description",
                    label: "설명"
                },{
                    data : "cycle",
                    label: "주기"
                },{
                    data : "cre_dt",
                    label: "등록일"
                },{
                    data : "start_time",
                    label: "시작일"
                },{
                    data : "cre_id",
                    label: "등록자 아이디"
                },{
                    data : "proceed_state",
                    label: "진행상황"
                },{
                    data : null,
                    label: "재시작"
                }
            ],
            columnDefs : [
                {
                    "targets": 3,
                    "class": "syst-btn",
                    "render": function (data, type, row, meta) {
                        var cycle_opt = row.cycle.substr(1,row.cycle.length-1);
                        var display_opt = "";
                        if( cycle_opt == "d")
                            display_opt = " day(s)";
                        else if( cycle_opt == "h")
                            display_opt = " hour(s)"
                        else
                            display_opt = " minute(s)"

                        display_opt = row.cycle[0] + display_opt;
                        return display_opt;
                    }
                },
                {
                    targets : 0,
                    render : function (data, type, row, meta) {

                        var btnHtml = "<input type='checkbox' name='dtSelector' value='"+meta.row+ "'/>";

                        return btnHtml;
                    }
                },
                {
                    targets : -1,
                    render : function (data, type, row, meta) {


                        if(row.restart_request === 0){
                            statusIndication = "요청";
                            var btnHtml = '<div id="bt-'+ row.id +'" class="syst-sm-bg-black" onclick="restartRequestSubmit(\''+ row.id +'\');">'+statusIndication+'</div>';
                        } else {
                            statusIndication = "요청중";
                            var btnHtml = '<div id="bt-'+ row.id +'" class="syst-sm-bg-black" style="background-color:#A9A9A9">'+statusIndication+'</div>';
                        }



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
    $('#demo-foo-filtering').DataTable().ajax.reload(function(data){
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
        dtTable.page.len($("#perpage").val()).draw();
    });
}