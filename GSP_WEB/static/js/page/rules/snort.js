function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.name = $("#pop_name").val();
        postData.pattern = $("#pop_pattern").val();
        postData.level = $("#pop_level").val();
        postData.description = $("#pop_desc").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/rules/snort",
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
        postData.name = $("#pop_name").val();
        postData.pattern = $("#pop_pattern").val();
        postData.level = $("#pop_level").val();
        postData.description = $("#pop_desc").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/rules/snort/"+ postData.seq,
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
    $("#pop_name").val(row.name);
    $('#pop_pattern').val(row.pattern);
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
            url: "/rules/snort/" + seq,
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
                    url:"/rules/snort/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();
                        d.columnIndex = window.localStorage.getItem('columnIndex');
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
            bLengthChange: true,
            processing: true,
            searching: false,
            sort: false,
            "ordering": false,
            paging: true,
            info: false,
            deferRender: true,
            responsive: true,
            "jQueryUI": true,
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    data : null
                },
                {
                    data : "name",
                    label: "패턴명 (탐지명)"
                },{
                    data : "pattern",
                    label: "패턴"
                },{
                    data : "level",
                    label: "위험도"
                },{
                    data : "description",
                    label: "설명"
                },
                /*{
                    data : "source_name",
                    label: "패턴 등록경로"
                },*/
                {
                    data : "mod_dt",
                    label: "수정일"

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

                 var theTableName = "snortPatternPage";
                 setTimeout(function(){
                        if((sessionStorage.getItem(theTableName) !== null))
                        {
                            if (sessionStorage.getItem(theTableName).length >= 1)
                            {
                                        var theTableWidth = parseInt(window.sessionStorage.getItem(theTableName));

                                        $(".dataTables_scrollHeadInner").width(theTableWidth);
                                        $(".table .table-striped .table-bordered .toggle-circle .m-b-0 .dataTable .no-footer").width(theTableWidth);

                                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();

                            }
                        }

                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                 }, 350);

                if(sessionStorage.getItem(theTableName) === null)
                {
                    sessionStorage.setItem(theTableName, $(".dataTables_scrollHeadInner").width());
                }


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



//$("#pName").click(function(){
////    $('#demo-foo-filtering').DataTable().ajax.reload();
//    window.localStorage.setItem('columnIndex','name');
//    DatatableReload();
//
//});
