var elementList;

function datasourceChange(id){
    dstCol = $("#pop_typea_src_column");
    dstCol.empty();
    selectElem = $('#pop_typea_tables');
    dataSource = selectElem.val();
    if(dataSource == '')
        return;

    var request = $.ajax({
            url:"/links/data-list/" + dataSource,
            type:"POST",
            success: function(data, status){
                dstCol = $("#pop_typea_src_column");
                dstCol.empty();
                dstCol.append("<option value=''>선택 필요</option>")
                for(var i = 0; i < data.data.length; i ++) {
                    var option = document.createElement("option");
                    option.text = data.data[i].column_name;
                    option.value = data.data[i].column_name;
                    dstCol.append(option);
                }
                if (id !== 'undefined'){
                    row = $('#demo-foo-filtering').DataTable().data()[id];
                    $('#pop_typea_src_column').val(row.src_columns_name);
                }

            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
}

function handleShowAddStep0(){
    $('#modal-popup').modal();

}

function handleAddStep0Submit(){
    elementType = $("input[name=pop_step0]:checked").val();
    $('#modal-popup').modal('toggle');

    if( elementType == "TypeA"){
        InitAddModalTypeA();
    }
    else{
        InitAddModalTypeB();
    }

}

function InitAddModalTypeA(){
    $('#modal-popup-typea').modal();
    $('#pop_typea_tables option:eq(0)').prop('selected', true);
    $("#pop_typea_src_column").val('');
    datasourceChange();
    $("#pop_typea_dst_column").val('');
    $('#pop_typea_desc').val('');
    $('input[name=pop_typea_dst_use]:input[value=Y]')[0].checked = true;
    $('#btnAddTypeA_Submit').show();
    $('#btnEditTypeA_Submit').hide();
    $('#popup-form-a').parsley().reset();
}

function InitAddModalTypeB(){

    $('#modal-popup-typeb').modal();
    $("#pop_typeb_name").val('');
    $("#pop_typeb_desc").val('');
    $('#pop_typeb_src_type0 option:eq(0)').prop('selected', true);
    $('#pop_typeb_src_col0 option:eq(0)').prop('selected', true);
    $('#pop_typeb_src_col_op0 option:eq(0)').prop('selected', true);
    $('#pop_typeb_op_col1_col2 option:eq(0)').prop('selected', true);
    $('#pop_typeb_src_type1 option:eq(0)').prop('selected', true);
    $('#pop_typeb_src_col1 option:eq(0)').prop('selected', true);
    $('#pop_typeb_src_col_op1 option:eq(0)').prop('selected', true);
    $('input[name=pop_typeb_dst_use]:input[value=Y]')[0].checked = true;
    $('#pop_typeb_dst_use').val('Y');
    //시간 제약 부분
    $("#pop_typeb_time_limit_enabled")[0].checked = false;
    $("#pop_typeb_timelimit_opt").val('');
    $("#pop_typeb_timespan_opt").val('');
    $("#pop_timelimit_equal").val('');
    $("#pop_timelimit_range_opt0").val('<');
    $("#pop_timelimit_range_val0").val('');
    $("#pop_timelimit_range_opt1").val('<');
    $("#pop_timelimit_range_val1").val('');
    onPop_typeb_timelimit_opt_changed();

    $("#pop_typeb_timespan_opt").val('h');
    $("#pop_typeb_cycle_value").val('1');
    $("#pop_typeb_cycle_opt").val('d');
    $('#btnAddTypeB_Submit').show();
    $('#btnEditTypeB_Submit').hide();
    initPopElementList('pop_typeb_src_type0','pop_typeb_src_col0');
    initPopElementList('pop_typeb_src_type1','pop_typeb_src_col1');
    $("#pop_typeb_add_col").val("+");
    $('.pop_typeb_add_col_div').hide();
    $('#timelimitoption').hide();
    $('#popup-form-b').parsley().reset();
}


function handleAddTypeASubmit (){
    var _form  = $('#popup-form-a')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.type = $('#pop_typea_tables').val();
        postData.src_column = $("#pop_typea_src_column").val();
        postData.dst_column = $("#pop_typea_dst_column").val();
        postData.desc = $('#pop_typea_desc').val();
        postData.use_yn = $("input[name=pop_typea_dst_use]:checked").val();

        var request = $.ajax({
            url:"/links/type-a",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup-typea').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditTypeASubmit (){
    var _form  = $('#popup-form-a')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.seq = $("#pop_typea_seq").val();
        postData.type = $('#pop_typea_tables').val();
        postData.src_column = $("#pop_typea_src_column").val();
        postData.dst_column = $("#pop_typea_dst_column").val();
        postData.desc = $('#pop_typea_desc').val();
        postData.use_yn = $("input[name=pop_typea_dst_use]:checked").val();

        var request = $.ajax({
            url:"/links/type-a/"+ postData.seq,
            type:"PUT",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup-typea').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function showEditTypeADialog(id){
    //datasourceChange();
    row = $('#demo-foo-filtering').DataTable().data()[id];

    $('#pop_typea_seq').val(row.id);
    $('#pop_typea_tables').val(row.src_type);
    datasourceChange(id);
    $('#pop_typea_src_column').val(row.src_columns_name);
    //$('#pop_typea_src_column option[value="'+ row.src_columns_name +'"]').attr("selected", true);
    $('#pop_typea_dst_column').val(row.column_name);
    $('#pop_typea_desc').val(row.description);
    $('input[name=pop_typea_dst_use]:input[value='+row.use_yn +']')[0].checked = true;
    $('#btnAddTypeA_Submit').hide();
    $('#btnEditTypeA_Submit').show();
    $('#modal-popup-typea').modal();

}

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/links/getlist",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_type = $("#search_type").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();
                    },
                    error: function(xhr, error, thrown) {
                        alert(error);
                        error(xhr, error, thrown);
                    }
                },
                dataFilter: function(data){
                var json = jQuery.parseJSON( data );
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                json.data = json.data;

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
            autoWidth : true,
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
                    data : "column_name",
                    label: "패턴(URI)"
                },{
                    data : "description",
                    label: "설명"
                },{
                    data : "source",
                    label: "종류"
                },
                {
                    data: "src_type",
                    label: "탐지점"
                },
                {
                    data : "cre_dt",
                    label: "패턴 등록경로"
                },
                {
                    data : "mod_dt",
                    label: "등록일"
                }
            ],
            columnDefs : [
                {
                    targets : 0,
                    render : function (data, type, row, meta) {

                        var btnHtml = "<input type='checkbox' name='dtSelector' value='"+row.source[0]+ meta.row+ "'/>";

                        return btnHtml;
                    }
                }
            ],
            select: {
                style:    'os',
                selector: 'td:first-child'
            },
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

//추가 모달 팝업에 요소 유형 선택 Select박스 Init
function getElementList(){

    var request = $.ajax({
            url:"/links/element-list",
            type:"GET",
            success: function(data, status){
                elementList = jQuery.parseJSON(data);
                initPopElementList('pop_typeb_src_type0','pop_typeb_src_col0');
                initPopElementList('pop_typeb_src_type1','pop_typeb_src_col1');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
}

function initPopElementList(srcElement, dstElement){
    if(elementList == null)
        return;
    type = $("#"+srcElement).val();
    targetElement = $("#"+dstElement);
    targetElement.empty();

    for( i =0; i < elementList[type].length; i++){
        var option = document.createElement("option");
        option.text = elementList[type][i].dst_columns_name;
        option.value = elementList[type][i].id;
        targetElement.append(option);
    }

}

function pop_typeb_add_col_click(){
    if( $('#pop_typeb_add_col').val() == '+' ){
        $('.pop_typeb_add_col_div').show();
        $('#pop_typeb_add_col').val('-');
    }else{
        $('.pop_typeb_add_col_div').hide();
        $('#pop_typeb_add_col').val('+');
    }
}

function timelimitoption_click(){
//    $('#timelimitoption').toggle();
       if ($("input:checkbox[id='pop_typeb_time_limit_enabled']").is(":checked") == true){
            $('#timelimitoption').show();
       }
       else {
            $('#timelimitoption').hide();
       }
}

function showEditTypeBDialog(id){
    InitAddModalTypeB();
    row = $('#demo-foo-filtering').DataTable().data()[id];

    $('#pop_typea_tables').val(row.src_type);

    $('#pop_typeb_seq').val(row.id);
    $('#pop_typeb_name').val(row.column_name);
    $('#pop_typeb_desc').val(row.description);

    //Parse Operate Function
    opData = JSON.parse(row.operate_function);
    for (k = 0; k < opData.org_elements.length; k ++)
    {
        if(k > 0)
            pop_typeb_add_col_click();

        $("#pop_typeb_op_col1_col2").val(opData.operate_between);

        $("#pop_typeb_src_type"+k).val(opData.org_elements[k].org_type);
        initPopElementList("pop_typeb_src_type"+k, "pop_typeb_src_col"+k )
        $("#pop_typeb_src_col"+k).val(opData.org_elements[k].org_id);
        //$("#pop_typeb_src_col"+k).val(1);
        $("#pop_typeb_src_col_op"+k).val(opData.org_elements[k].operate);
    }

    timestan_val = row.timespan.substr(0, row.timespan.length-1);
    timestan_opt = row.timespan.substr(row.timespan.length-1, 1);
    $("#pop_typeb_timespan_opt").val(timestan_opt);

    cycle_val = row.analysis_cycle.substr(0, row.analysis_cycle.length-1);
    cycle_opt = row.analysis_cycle.substr(row.analysis_cycle.length-1, 1);
    $("#pop_typeb_cycle_value").val(cycle_val);
    $("#pop_typeb_cycle_opt").val(cycle_opt);

    $('input[name=pop_typeb_dst_use]:input[value='+row.use_yn +']')[0].checked = true;
    $('#pop_typeb_dst_use').val(row.use_yn);

    //시간 제약 부분
    if(opData.time_range != null){
        $("#pop_typeb_time_limit_enabled").prop("checked",true);
        $("#pop_typeb_timelimit_op").val(opData.time_range.op);
        $("#pop_typeb_timelimit_unit").val(opData.time_range.unit);
        onPop_typeb_timelimit_opt_changed();
        if(opData.time_range.op == "equal"){
            $("#pop_timelimit_equal_val").val(opData.time_range.value[0]);
        }
        else{
            $("#pop_timelimit_range_val0").val(opData.time_range.value[0]);
            $("#pop_timelimit_range_val1").val(opData.time_range.value[1]);
        }
    }

    if ($("input:checkbox[id='pop_typeb_time_limit_enabled']").is(":checked") == true)
    {
            $('#timelimitoption').show();
    }
    else
    {
            $('#timelimitoption').hide();
    }


    $('#btnAddTypeB_Submit').hide();
    $('#btnEditTypeB_Submit').show();
    $('#modal-popup-typeb').modal();
}

function handleAddTypeBSubmit (){
    var _form  = $('#popup-form-b')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.name = $('#pop_typeb_name').val();
        postData.desc = $('#pop_typeb_desc').val();
        postData.src_type0 = $("#pop_typeb_src_type0").val();
        postData.src_column0 = $("#pop_typeb_src_col0").val();
        postData.src_column_op0 = $("#pop_typeb_src_col_op0").val();
        postData.timespan_opt = $("#pop_typeb_timespan_opt").val();
        postData.cycle_value = $("#pop_typeb_cycle_value").val();
        postData.cycle_opt = $("#pop_typeb_cycle_opt").val();
        //postData.use_yn = $("input[name=pop_typeb_dst_use]:checked").val();
        postData.use_yn = $("#pop_typeb_dst_use").val();

        if($("#pop_typeb_add_col").val() == "-") {
            postData.colCnt = 2;
            postData.op = $("#pop_typeb_op_col1_col2").val();
            postData.src_type1 = $("#pop_typeb_src_type1").val();
            postData.src_column1 = $("#pop_typeb_src_col1").val();
            postData.src_column_op1 = $("#pop_typeb_src_col_op1").val();
        }
        else{
            postData.colCnt = 1;
        }

        timeLimitIsChecked = $("#pop_typeb_time_limit_enabled").prop("checked");
        if(timeLimitIsChecked){
            postData.tr_op = $("#pop_typeb_timelimit_op").val();
            postData.tr_unit = $("#pop_typeb_timelimit_unit").val();
            if( postData.tr_op == "equal"){
                postData.tr_value0 = $("#pop_timelimit_equal_val").val();
            }
            else{
                postData.tr_value0 = $("#pop_timelimit_range_val0").val();
                postData.tr_value1 = $("#pop_timelimit_range_val1").val();
            }
        }

        var request = $.ajax({
            url:"/links/type-b",
            type:"POST",
            data:postData,
            success: function(data, status){
                getElementList();   //링크요소 목록 reload
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup-typeb').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditTypeBSubmit (){
    var _form  = $('#popup-form-b')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var seq = $('#pop_typeb_seq').val();

        var postData = new Object();
        postData.name = $('#pop_typeb_name').val();
        postData.desc = $('#pop_typeb_desc').val();
        postData.src_type0 = $("#pop_typeb_src_type0").val();
        postData.src_column0 = $("#pop_typeb_src_col0").val();
        postData.src_column_op0 = $("#pop_typeb_src_col_op0").val();
        postData.timespan_opt = $("#pop_typeb_timespan_opt").val();
        postData.cycle_value = $("#pop_typeb_cycle_value").val();
        postData.cycle_opt = $("#pop_typeb_cycle_opt").val();
        //postData.use_yn = $("input[name=pop_typeb_dst_use]:checked").val();
        postData.use_yn = $("#pop_typeb_dst_use").val();

        if($("#pop_typeb_add_col").val() == "-") {
            postData.colCnt = 2;
            postData.op = $("#pop_typeb_op_col1_col2").val();
            postData.src_type1 = $("#pop_typeb_src_type1").val();
            postData.src_column1 = $("#pop_typeb_src_col1").val();
            postData.src_column_op1 = $("#pop_typeb_src_col_op1").val();
        }
        else{
            postData.colCnt = 1;
        }

        timeLimitIsChecked = $("#pop_typeb_time_limit_enabled").prop("checked");
        if(timeLimitIsChecked){
            postData.tr_op = $("#pop_typeb_timelimit_op").val();
            postData.tr_unit = $("#pop_typeb_timelimit_unit").val();
            if( postData.tr_op == "equal"){
                postData.tr_value0 = $("#pop_timelimit_equal_val").val();
            }
            else{
                postData.tr_value0 = $("#pop_timelimit_range_val0").val();
                postData.tr_value1 = $("#pop_timelimit_range_val1").val();
            }
        }

        var request = $.ajax({
            url:"/links/type-b/"+ seq,
            type:"PUT",
            data:postData,
            success: function(data, status){
                getElementList();   //링크요소 목록 reload
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup-typeb').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function onPop_typeb_timelimit_opt_changed(){

    opt = $("#pop_typeb_timelimit_op").val();
    if( opt == "equal"){
        $("#pop_timelimit_div_equal").css("display","inline");
        $("#pop_timelimit_div_range").hide();
    }
    else if( opt == "range"){
        $("#pop_timelimit_div_equal").hide();
        $("#pop_timelimit_div_range").css("display","inline");
    }
}

function deleteItem(){

    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('삭제 할 아이템을 선택 해 주세요');
        return;
    }

    var rowval = $('input[name=dtSelector]input:checked')[0].value

    var type = rowval[0].toLowerCase();
    var rownum = rowval.substr(1, rowval.length - 1);
    seq = $('#demo-foo-filtering').DataTable().data()[rownum].id;

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    if( result) {
        url = "/links/type-" + type + "/";

        var request = $.ajax({
            url: url + seq,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                getElementList();   //링크요소 목록 reload
                $('#demo-foo-filtering').DataTable().ajax.reload();
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function showEditDialogSetp0(){

    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('수정 할 아이템을 선택 해 주세요');
        return;
    }

    var type = $('input[name=dtSelector]input:checked')[0].value;
    if ( type[0] == 'A') {
        id = type.substr(1, type.length - 1);
        showEditTypeADialog(id);
    }
    if ( type[0] == 'B') {
        id = type.substr(1, type.length -1 );
        showEditTypeBDialog(id);
    }


}