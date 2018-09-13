var elementList = null; //링크요소 목록
var stdataList = null;  //표준데이터 목록
//var country_code_identifier = null; //국가코드를 위한 Global variable.
var input_sub_list = [0];
var dna_sector_confirmed = false;

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
    form.setAttribute('action', "/dna/list/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}


function handleShowAdd(){
    $('#modal-popup').modal();
    initInputPopup();

    $('#btnAdd_Submit').show();
    $('#btnEdit_Submit').hide();
}

function initInputPopup(){
    input_div = $("[name='pop_input_sub']");

    $("#pop_name").val('');

    pop_link_e_changed('pop_link_e_0','pop_st_data_0');
    pop_op_type_changed('pop_op_type_0','pop_op_0');

    for(var i = 1; i < input_div.length; i ++){
        input_div[i].remove();
        input_sub_list = [0];
        dna_sector_confirmed = false;
    }
}

var TableManageDefault = function () {
	"use strict";
    return {
        //main function
        init: function () {
            GetList();
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

function LoadStData(){

    var request = $.ajax({
            url:"/links/st_data/full-list",
            type:"GET",
            success: function(data, status){
                stdataList = new Array();

                for(i = 0; i < data.length; i++){
                    var dict = {}
                    dict["id"] = data[i].id;
                    dict["name"] = data[i].name;
                    dict["target_type"] = data[i].target_link_type;
                    dict["target_seq"] = data[i].target_link_seq;
                    stdataList.push(dict);
                }

            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });

}

function LoadInitData(){

    var request = $.ajax({
            url:"/links/element-list",
            type:"GET",
            success: function(data, status){
                _elementList = jQuery.parseJSON(data);
                elementList = new Array();
                for(i = 0; i < _elementList.TypeA.length; i++){
                    var dict = {}
                    dict["id"] = "a" + _elementList.TypeA[i].id;
                    dict["name"] = _elementList.TypeA[i].dst_columns_name;
                    dict["dst_data_type"] = _elementList.TypeA[i].dst_data_type;
                    elementList.push(dict);
                }
                for(i = 0; i < _elementList.TypeB.length; i++){
                    var dict = {}
                    dict["id"] = "b" + _elementList.TypeB[i].id;
                    dict["name"] = _elementList.TypeB[i].dst_columns_name;
                    dict["dst_data_type"] = _elementList.TypeB[i].dst_data_type;
                    elementList.push(dict);
                }

                initPopAddDnaDiv('0');

            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });

}

function GetList(){

    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/dna/list",
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
            pageLength: $("#perpage").val(),
            fixedHeader: true,
            "scrollY" : "700px",
            autoWidth : true,
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
                    label: "id"
                },{
                    data : "dna_name",
                    label: "DNA 이름"
                },{
                    data : "operate_function",
                    label: "설명"
                },{
                    data : "cre_dt",
                    label: "등록일"
                },{
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
                },
                {
                    "targets": 3,
                    "class": "syst-btn",
                    "render": function (data, type, row, meta) {
                        opData = JSON.parse(row.operate_function);
                        var btnHtml = '';

                        for(var i = 0; i < opData.dna_name_list.length; i ++){
                            if(i > 0)
                                btnHtml += ", "

                            if(opData.dna_name_list[i].isImportantDNA)
                                btnHtml += "<label style='color:red;display:inline' >" + opData.dna_name_list[i].dna_name + "</label>";
                            else
                                btnHtml += "<label style='display:inline'>" + opData.dna_name_list[i].dna_name + "</label>";
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

                dtTable.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                    var data = this.data();

                    var _id = "list_data_" + rowIdx;
                    try {
                        if ($("#" + _id) != null)
                            DrawChart(_id, jQuery.parseJSON(data.list_data));
                    }
                    catch (exception) {
                    }

                });
            }
        });

        // $('#dtData').footable();
        // $("#dtTableToolbar").insertBefore( "#demo-foo-filtering_paginate" );

    }
}

function initPopAddDnaDiv(rownum){
    pop_link_e_init('pop_link_e_'+rownum);
    pop_op_type_changed('pop_op_type_0', 'pop_op_0');
    clear_dna_sector();
}

function pop_link_e_init(id){
    $("#"+id).empty();
    clear_dna_sector();
    for( i = 0; i < elementList.length; i++){
        //option = new Option(elementList[i].id, elementList[i].name);
        $("#"+id).append( $('<option>', {
            value:elementList[i].id,
            text : elementList[i].name
        }) );
    }
}

function pop_link_e_changed(link_e, stdata_e){
    $("#"+stdata_e).empty();
    var selectedID = $("#"+link_e).val();
    var selectedElement = null;

    for (var i = 0; i < elementList.length; i++) {
        if (elementList[i].id == selectedID) {
            selectedElement = elementList[i];
        }
    }

    if(selectedElement.dst_data_type == "list" || selectedElement.dst_data_type == "single_list"){
        $("#"+stdata_e).append( $('<option>', {
                value:"-1",
                text : "표준데이터 선택"
            }) );

        for( var i = 0; i < stdataList.length; i ++){
            if ( selectedElement.id == stdataList[i].target_type + stdataList[i].target_seq) {
                $("#" + stdata_e).append($('<option>', {
                    value: stdataList[i].id,
                    text: stdataList[i].name
                }));
            }
        }
    }
    else if (selectedElement.name == "src_country_code" || selectedElement.name == "dst_country_code") {

        $("#"+stdata_e).append( $('<option>', {
                value: "country",
                text : "국가명 입력"
            }) );
    }
    else if(selectedElement.dst_data_type == "single" && !(selectedElement.name == "src_country_code" || selectedElement.name == "dst_country_code")){
        $("#"+stdata_e).append( $('<option>', {
                value:"",
                text : "단일 값 비교"
            }) );


    }

    else{
        $("#"+stdata_e).append( $('<option>', {
                value:"in",
                text : "포함 여부 비교"
            }) );
    }

    clear_dna_sector();

    var rowNum = link_e[link_e.length - 1];
    $("#link_element_column_text_for_row_"+rowNum).html("<p>"+selectedElement.name+"</p>");

    pop_st_data_changed( stdata_e);

}

function pop_op_type_changed(id_src, id_target){

    clear_dna_sector();
    $("#"+id_target).empty();
    var rownum = id_src.replace('pop_op_type_','');

    type = $("#"+id_src).val();
    $("#"+id_target).change = null;
    if( type == "bool"){
        var option0 = new Option( ">", ">" );
        var option1 = new Option( "<", "<" );
        var option2 = new Option( ">=", ">=" );
        var option3 = new Option( "<=", "<=" );
        var option4 = new Option( "=", "=" );
        var option5 = new Option( "!=", "!=" );
        $("#"+id_target).append(option0);
        $("#"+id_target).append(option1);
        $("#"+id_target).append(option2);
        $("#"+id_target).append(option3);
        $("#"+id_target).append(option4);
        $("#"+id_target).append(option5);
        $("#"+id_target).change(function(){
           pop_op_changed_simple(id_target, 'pop_value_table_' + rownum);
        });
    }
    else if(type == "range"){
        var option0 = new Option( "3", "3" );
        var option1 = new Option( "4", "4" );
        var option2 = new Option( "5", "5" );
        $("#"+id_target).append(option0);
        $("#"+id_target).append(option1);
        $("#"+id_target).append(option2);

        $("#"+id_target).change(function(){
           pop_op_changed_range(id_target, 'pop_value_table_' + rownum);
        });
    }
    else if(type == "strbool") {
        var option0 = new Option( "===", "===" );
        var option1 = new Option( "!==", "!==" );
        $("#"+id_target).append(option0);
        $("#"+id_target).append(option1);

        $("#"+id_target).change(function(){
           pop_op_changed_country(id_target, 'pop_value_table_' + rownum);
        });
    }
    else if(type=="in"){
        var option0 = new Option("in", "in")
        $("#"+id_target).append(option0);
        $("#"+id_target).change(function(){
           pop_op_changed_in(id_target, 'pop_value_table_' + rownum);
        });
    }
    $("#"+id_target).change();

}

function pop_op_changed_simple(id_src, id_target){

    clear_dna_sector();

    var type = $("#"+id_src).val();
    var rownum = id_src.replace('pop_op_','');
    $("#"+id_target).empty();
    var input_id = 'pop_input_simple_' + rownum;




         tr0 = "<tr>\n" +
            "    <td><label style='font-size:20px;vertical-align:baseline;'> "+$("#"+id_src).val()+"</label></td><td><input id='"+input_id+"' name='pop_input_simple' type=\"text\" ></td>\n" +
            "</tr>";


    $("#" + id_target).append(tr0);

}

function pop_op_changed_country(id_src, id_target){

    clear_dna_sector();

    var type = $("#"+id_src).val();
    var rownum = id_src.replace('pop_op_','');
    $("#"+id_target).empty();
    var input_id = 'pop_input_simple_' + rownum;




    tr0 = "<tr>\n" +
    "    <td><label style='font-size:20px;vertical-align:baseline;'> "+$("#"+id_src).val()+"</label></td><td><input id='"+input_id+"' name='pop_input_simple' type=\"text\" ></td>\n" +
    "</tr>";



    $("#" + id_target).append(tr0);

}


function pop_op_changed_range(id_src, id_target){
    clear_dna_sector();

    var type = $("#"+id_src).val();
    var rownum = id_src.replace('pop_op_','');

    $("#"+id_target).empty();

    tr_first = "<tr>\n" +
            "    <td style='font-size:20px;vertical-align:baseline;'></td><td><label style='text-align:center;font-size:25px;vertical-align:baseline;'>&lt;</label></td><td><input style='width:100px' type=\"text\" ></td>\n" +
            "</tr>";
    $("#" + id_target).append(tr_first);

    for( i = 2; i < type; i ++){
        tr_middle = "<tr>\n" +
            "    <td><input style='width:100px' type=\"text\" ></td><td><label style='text-align:center;font-size:25px;vertical-align:baseline;'>~</label></td> <td><input style='width:100px' type=\"text\" ></td>\n" +
            "</tr>";
        $("#" + id_target).append(tr_middle);
    }

    tr_last = "<tr>\n" +
            "    <td><input style='width:100px' type=\"text\" ></td><td><label style='text-align:center;font-size:25px;vertical-align:baseline;'>&lt;</label></td><td style='font-size:20px;vertical-align:baseline;'></td>\n" +
            "</tr>";
    $("#" + id_target).append(tr_last);

}

function pop_op_changed_in(id_src, id_target){

    clear_dna_sector();

    var type = $("#"+id_src).val();
    var rownum = id_src.replace('pop_op_','');
    $("#"+id_target).empty();
    var input_id = 'pop_input_simple_' + rownum;

    tr0 = "<tr>\n" +
            "    <td><label style='font-size:17px;vertical-align:baseline;'> "+"</label></td><td><input id='"+input_id+"' name='pop_input_simple' type=\"text\" placeholder=', 로 구분'></td>\n" +
            "</tr>";

    $("#" + id_target).append(tr0);

}

function pop_st_data_changed(stdata){
    clear_dna_sector();

    e_st_data = $("#"+stdata);
    rownum = stdata[stdata.length-1];

    $("#pop_op_type_"+rownum).empty();

    if( e_st_data.val() != "in" && !(e_st_data.val() == "country")){
        var option0 = new Option( ">,<,=", "bool"  );
        var option1 = new Option( "A ~ B (Range)", "range" );
        $("#pop_op_type_"+rownum).append(option0);
        $("#pop_op_type_"+rownum).append(option1);
       // country_code_identifier = "";
    }
    else if(e_st_data.val() == "country") {
        var option0 = new Option("일치, 불일치", "strbool");
        //country_code_identifier = "countryBool";
        $("#pop_op_type_"+rownum).append(option0);
    }
    else{
        var option0 = new Option( "값 포함", "in" );
        $("#pop_op_type_"+rownum).append(option0);
        //country_code_identifier = "";
    }

    pop_op_type_changed('pop_op_type_'+rownum,'pop_op_'+rownum)

}

function add_inputdiv(){
    clear_dna_sector();

    if (input_sub_list.length > 3){
        alert("DNA 요소는 최대 4개 까지만 가능 합니다.");
        return;
    }

    rownum = Math.max.apply(null,input_sub_list)+1;
    div_id = "pop_input_sub"+rownum;

    inputDiv = "<div name='pop_input_sub' id='"+div_id+"' class=\"popup-input-sub\" style=\"display:contents;\">\n" +
        "<br>" +
        "                            <table>\n" +
        "                                <tr>\n" +
        "                                    <td width=\"100px\">\n" +
        "                                        <input type=\"button\" value=\"-(삭제)\" style=\"width:70px;\" onclick='remove_inputdiv("+ rownum +")')>\n" +
        "                                    </td>\n" +
        "                                    <td>\n" +
        "                                        <select id=\"pop_link_e_"+rownum+"\" name=\"pop_link_e\" onchange=\"pop_link_e_changed('pop_link_e_"+rownum+"','pop_st_data_"+rownum+"')\">\n" +
        "                                        </select>\n" +
        "                                    </td>\n" +
        "                                    <td>\n" +
        "                                        <select id=\"pop_st_data_"+rownum+"\" name=\"pop_st_data\" onchange=\"pop_st_data_changed('pop_st_data_"+rownum+"')\">\n" +
        "                                        </select>\n" +
        "                                    </td>\n" +
        "                                    <td>\n" +
        "                                        <select id=\"pop_op_type_"+rownum+"\" name=\"pop_op_type\" onchange=\"pop_op_type_changed('pop_op_type_"+rownum+"','pop_op_"+rownum+"')\">\n" +
        "                                            <option value=\"bool\">&gt;,&lt;,=</option>\n" +
        "                                            <option value=\"range\">A ~ B (Range)</option>\n" +
        "                                            <option value=\"in\">In</option>\n" +
        "                                        </select>\n" +
        "                                    </td>\n" +
        "                                    <td>\n" +
        "                                        <select id=\"pop_op_"+rownum+"\" name=\"pop_op\" >\n" +
        "                                            <option value=\">\">&gt;</option>\n" +
        "                                            <option value=\"=\">=</option>\n" +
        "                                        </select>\n" +
        "                                    </td>\n" +
        "                                    <td style='width:75px; font-size: 9px !important; word-wrap:break-word;' id=\"link_element_column_text_for_row_"+rownum+"\"><p>Link요소<p></td>\n" +
        "                                    <td>\n" +
        "                                        <table id=\"pop_value_table_"+rownum+"\" style=\"width:120px\">\n" +
        "                                            <tr>\n" +
        "                                                <td><input name='pop_value' type=\"text\" ></td><td><label style=\"width:50px;font-size:25px;vertical-align:baseline;\">&gt;</label></td><td>X</td>\n" +
        "                                            </tr>\n" +
        "                                            <tr>\n" +
        "                                                <td><input name='pop_value' type=\"text\" ></td><td><label style=\"width:50px;font-size:25px;vertical-align:baseline;\">&lt;= X</label></td><td>X</td>\n" +
        "                                            </tr>\n" +
        "                                        </table>\n" +
        "                                    </td>\n" +
        "                                </tr>\n" +
        "                            </table>\n" +
        "                        </div>";

    $("#divAddInputArea").append(inputDiv);
    pop_link_e_init('pop_link_e_'+rownum);
    pop_link_e_changed('pop_link_e_'+rownum, 'pop_st_data_'+rownum);
    pop_op_type_changed( 'pop_op_type_'+rownum, 'pop_op_'+rownum);

    input_sub_list.push(rownum);
}

function remove_inputdiv(id_no){
    $("#pop_input_sub"+id_no).remove();
    input_sub_list.pop(id_no);
    clear_dna_sector();
}

function clear_dna_sector(){
    $("#tbl_dna_sector").empty();
    dna_sector_confirmed = false;
}

function make_dna_sector(){
    clear_dna_sector();

    if( !validate_input_value())
        return;

    desc_list = [];
    desc_id_list = [];

    id = 0;
    for( var i = 0; i < input_sub_list.length; i ++) {
        op_type = $('#pop_op_type_' + input_sub_list[i]).val();
        sub_desc = [];
        sub_id = [];

        stdata = $("#pop_st_data_"+i).val();
        org_column = $('#pop_link_e_' + input_sub_list[i] + " option:selected").text()
        if(stdata != "" && stdata != "in")
            org_column += " 의 '"+$("#pop_st_data_"+i+" option:selected").text()+ "'상관관계값";

        //같거나 다르다로 나뉘는 단순 비교 항목 - 이 경우는 true, false 두가지 DNA 섹터를 생성 합니다.
        if(op_type == 'bool'){

            input_value = $("#pop_value_table_"+i).find('input')[0].value;

            //true
            desc = "[ {0} {1} {2}]".format(
                org_column,
                $('#pop_op_' + input_sub_list[i]).val(),
                input_value
            );
            sub_desc.push(desc);
            sub_id.push(id++);

            //false
            _op_op_val = OppositionFunction($('#pop_op_' + input_sub_list[i]).val());
            desc = "[ {0} {1} {2}]".format(
                org_column,
                _op_op_val,
                input_value
            );
            sub_desc.push(desc);
            sub_id.push(id++);

        }
        else if (op_type == 'strbool'){
            input_value = $("#pop_value_table_"+i).find('input')[0].value;

            //true
            desc = "[ {0} {1} {2}]".format(
                org_column,
                $('#pop_op_' + input_sub_list[i]).val(),
                input_value
            );
            sub_desc.push(desc);
            sub_id.push(id++);

            //false
            _op_op_val = OppositionFunction($('#pop_op_' + input_sub_list[i]).val());
            desc = "[ {0} {1} {2}]".format(
                org_column,
                _op_op_val,
                input_value
            );
            sub_desc.push(desc);
            sub_id.push(id++);
        }
        //Range 비교 (Range 수만큼 생성)
        else if(op_type == 'range'){
            input_element = $("#pop_value_table_"+i).find('input');
            for( var k=0; k < input_element.length; k++){
                desc = "{0} {1} {2}";
                if( k == 0 ){   //Range 비교 첫번째 요소는 x < [ ]
                    desc = "[{0} < {1}] ".format(org_column,input_element[k].value);
                }
                else if ( k == input_element.length-1){ //마지막 요소는  [] < X
                    desc = "[{0} > {1}]".format(org_column, input_element[k].value);
                }
                else{   //중간 요소는 입력필드 2개씩 쌍으로 사용한다.
                    desc = "[{1} <= {0} <= {2}]".format(org_column, input_element[k].value, input_element[k+1].value);
                    k++;
                }

                sub_desc.push(desc);
                sub_id.push(id++);
            }
        }
        else {
            input_value = $("#pop_value_table_"+i).find('input')[0].value;

            //true
            desc = "[ ({0}) {1} {2}]".format(
                input_value,
                $('#pop_op_' + input_sub_list[i]).val(),
                org_column
            );
            sub_desc.push(desc);
            sub_id.push(id++);

            //false
            _op_op_val = OppositionFunction($('#pop_op_' + input_sub_list[i]).val());
            desc = "[ ({0}) {1} {2}]".format(
                input_value,
                _op_op_val,
                org_column
            );
            sub_desc.push(desc);
            sub_id.push(id++);
        }

        desc_list.push(sub_desc);
        desc_id_list.push(sub_id);

    }

    var tableHead = "<tr style=\"margin-bottom:5px !important;\">\n " +
                                    "<th style='text-align: center;'>DNA섹터명</th>\n" +
                                    "<th style='text-align: center;'>산술식</th>\n" +
                                    "<th style='text-align: center;'>중요DNA</th>\n" +
                                    "<th style='text-align: center;'>WhiteList</th>\n" +
                                    "<th style='text-align: center;'>설명</th>\n" +
                    "</tr>";
    $("#tbl_dna_sector").append(tableHead);
    //DNA 각 조건을 조합하여 각각의 DNA 섹터를 재귀호출 하여 생성 한다.
    complexed_desc = [];
    for( var i =0; i < desc_list.length; i++) {
        if( i == 0) {
            complexed_desc = createDnaSectorRecursive(desc_list[i], desc_list[i + 1]);
        }
        else{
            complexed_desc = createDnaSectorRecursive(complexed_desc, desc_list[i + 1]);
        }
    }

    complexed_ids = [];
    for( var i =0; i < desc_id_list.length; i++) {
        if( i == 0) {
            complexed_ids = createDnaSectorIdRecursive(desc_id_list[i], desc_id_list[i + 1]);
        }
        else{
            complexed_ids = createDnaSectorIdRecursive(complexed_ids, desc_id_list[i + 1]);
        }
    }

    //desc_list의 마지막 요소를 불러와서 화면에 그려준다.
    for( var i =0; i < complexed_desc.length; i ++){
        sector_row = getSectorRow(complexed_ids[i], "", complexed_desc[i], false, "");
        $("#tbl_dna_sector").append(sector_row);
    }

    dna_sector_confirmed = true;
}

function createDnaSectorRecursive(curList, nextList){
    result = [];
    if(nextList == null){
        return curList;
    }else {
        for(var i = 0; i < curList.length; i ++){
            for( var k = 0; k < nextList.length; k++){
                result.push(curList[i] + "\r " + nextList[k]);
            }
        }
    }

    return result;

}

function createDnaSectorIdRecursive(curList, nextList){
    result = [];
    if(nextList == null){
        return curList;
    }else {
        for(var i = 0; i < curList.length; i ++){
            for( var k = 0; k < nextList.length; k++){
                result.push(curList[i] + "_" + nextList[k]);
            }
        }
    }

    return result;

}

function getSectorRow(row_id, name, desc, ischecked, comment){

    checked = (ischecked ? "checked" : "");
    sector_row =
            "       <tr>\n" +
            "           <td style=\"width:385px\">\n" +
            "               <label style=\"width:0px\"></label>\n" +
            "               <input id='sector_name_"+row_id+"' name='sector_name' type=\"text\" value='"+name+"' style='width:300px;'>\n" +
            "           </td>\n" +
            "           <td style=\"width:550px\">\n" +
            "               <label name='sector_desc' style=\"text-align:center; width:550px;color:deepskyblue;margin-bottom:0px\">"+desc+"</label>\n" +
            "           </td>\n" +
            "           <td style=\"vertical-align: center\" style='width:110px;'>\n" +
            "               <label style=\"width:110px;margin-bottom:0px\"><input id='sector_chk_"+ row_id+"' name=\"radio_important\" type=\"checkbox\" "+checked+">중요 DNA</label>\n" +
            "           </td>\n" +
            "           <td style=\"vertical-align: center\" style='width:50px;'>\n" +
            "               <label style=\"width:50px;margin-bottom:0px\"><input id='whitelist_chk_"+ row_id+"' name=\"radio_whitelist\" type=\"checkbox\" "+checked+"></label>\n" +
            "           </td>\n" +
            "           <td style='width:400px;text-align:center'>" +
            "               <label style=\"width:0px\"></label><input id='sector_comment_"+row_id+"' name='sector_comment' type=\"text\" style='width:360px' value='"+comment+"'>\n" +
            "           </td>\n" +
            "       </tr>".format(name, desc, checked);

    return sector_row;

}


String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
}

function validate_input_value(){
    if( $("#pop_name").val().trim().length == 0 ) {
        $("#pop_name").css('border-color', "red");
        return false;
    }
    else{
        $("#pop_name").css('border-color', "#e0e0e0");
    }

    for( var i = 0; i < input_sub_list.length; i ++) {
        var st_data = $("#pop_st_data_"+i).val();
        if(st_data < 0){
            $("#pop_st_data_"+i).css('border-color', "red");
            return false;
        }
        else{
            $("#pop_st_data_"+i).css('border-color', "#e0e0e0");
        }

        op_type = $('#pop_op_type_' + input_sub_list[i]).val();
        if(op_type == 'bool') {//단순 비교식
            op = $('#pop_op_' + input_sub_list[i]).val();
            input_value = $("#pop_value_table_"+i).find('input')[0].value;

            if(input_value.trim().length == 0){
                $("#pop_value_table_"+i).find('input').css('border-color', "red");
                return false;
            }
            else if(op_type != "=" || op_type == "!="){
                //== 비교가 아닌 부등호의 경우 숫자만 입력 가능하다


                if( !isInt(input_value)) {
                    $("#pop_value_table_" + i).find('input').css('border-color', "red");
                    return false;
                }
            }

            $("#pop_value_table_"+i).find('input').css('border-color', "#e0e0e0");
        }
        else if (op_type == 'strbool') {
            op = $('#pop_op_' + input_sub_list[i]).val();
            input_value = $("#pop_value_table_"+i).find('input')[0].value;

            if(input_value.trim().length == 0){
                $("#pop_value_table_"+i).find('input').css('border-color', "red");
                return false;
            }
        }
        else if (op_type == "range"){
            input_element = $("#pop_value_table_"+i).find('input');
            for( var k=0; k < input_element.length; k++){
                var input_value = input_element[k].value
                if(input_value.trim().length == 0) {
                    $(input_element[k]).css('border-color', "red");
                    return false;
                }
                else if(!isInt(input_value)) {
                    $(input_element[k]).css('border-color', "red");
                    return false;
                }
                else{
                    if( k > 0 && parseFloat(input_element[k-1].value) >= parseFloat(input_element[k].value)) {
                        $(input_element[k]).css('border-color', "red");
                        return false;
                    }
                }
                $(input_element[k]).css('border-color', "#e0e0e0");
            }
        }
        else{   //in 비교
            op = $('#pop_op_' + input_sub_list[i]).val();
            input_value = $("#pop_value_table_"+i).find('input')[0].value;

            if(input_value.trim().length == 0){
                $("#pop_value_table_"+i).find('input').css('border-color', "red");
                return false;
            }

            var valueList = input_value.split(",");
            for(var k = 0; k < valueList.length; k ++) {
                _row = valueList[k];
                if (_row.trim().length == 0) {
                    $("#pop_value_table_" + i).find('input').css('border-color', "red");
                    return false;
                }
            }

            $("#pop_value_table_"+i).find('input').css('border-color', "#e0e0e0");
        }
    }

    return true;
}

function isInt(n) {
    return $.isNumeric(n);
   //return n % 1 === 0;
}

function validate_dna_sector(){
    if(!dna_sector_confirmed){
        alert("DNA 섹터를 확정 해 주세요");
        return false;
    }
    
    input_elements = $("#tbl_dna_sector").find("input[type='text'][name='sector_name']");
    for(var i=0; i < input_elements.length; i ++){
        if( input_elements[i].value.trim().length == 0) {
            $(input_elements[i]).css('border-color', 'red');
            return false;
        }
        else{
            $(input_elements[i]).css('border-color','#e0e0e0');
        }
    }

    return true;
}

function AddSubmit(){
    if( validate_input_value() == false || validate_dna_sector() == false)
        return;

    dna_config = MakeSubmitData();

    jsondata = JSON.stringify(dna_config);
    var postData = new Object();
    postData.dna_name = $("#pop_name").val();
    postData.dna_config = jsondata;

    var request = $.ajax({
        url:"/dna/manage",
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

function EditSubmit(){
    if( validate_input_value() == false || validate_dna_sector() == false)
        return;

    dna_config = MakeSubmitData();

    jsondata = JSON.stringify(dna_config);
    var postData = new Object();
    postData.dna_name = $("#pop_name").val();
    postData.dna_config = jsondata;

    var request = $.ajax({
        url:"/dna/manage/" + $("#pop_seq").val(),
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

function MakeSubmitData(){
    operate_list = [];

    range_id = 0;

    for(var i=0; i < input_sub_list.length; i ++){

        linkvalue = $('#pop_link_e_' + input_sub_list[i]).val();
        stdata = $('#pop_st_data_' + input_sub_list[i]).val();
        optype = $("#pop_op_type_" + input_sub_list[i] ).val();
        op = $("#pop_op_" + input_sub_list[i] ).val();
        if(op === "Equal"){
            op = "===";
        } else if (op === "Unequal") {
            op = "!==";
        }
        value_range =[];


        if(optype == "bool" ){
            input_value = $("#pop_value_table_"+i).find('input')[0].value;
            var value_item =
                {
                    "range_id" : range_id++,
                    "value" : input_value,
                    "operate" : op,
                    "bool" : "true"
                };
            value_range.push(value_item);

            input_value = $("#pop_value_table_"+i).find('input')[0].value;
            var value_item =
                {
                    "range_id" : range_id++,
                    "value" : input_value,
                    "operate" : op,
                    "bool" : "false"
                };
            value_range.push(value_item);
        } else if (optype == "strbool")   {
             input_value = $("#pop_value_table_"+i).find('input')[0].value;
            var value_item =
                {
                    "range_id" : range_id++,
                    "value" : input_value,
                    "operate" : op,
                    "bool" : "true"
                };
            value_range.push(value_item);

            input_value = $("#pop_value_table_"+i).find('input')[0].value;
            var value_item =
                {
                    "range_id" : range_id++,
                    "value" : input_value,
                    "operate" : op,
                    "bool" : "false"
                };
            value_range.push(value_item);
        }
        else if(optype == "in"){
            input_value = $("#pop_value_table_"+i).find('input')[0].value;
            stdata = "";
            var value_item =
                {
                    "range_id" : range_id++,
                    "value" : input_value.split(","),
                    "operate" : op,
                    "bool" : "true"
                };
            value_range.push(value_item);

            input_value = $("#pop_value_table_"+i).find('input')[0].value;
            var value_item =
                {
                    "range_id" : range_id++,
                    "value" : input_value.split(","),
                    "operate" : op,
                    "bool" : "false"
                };
            value_range.push(value_item);
        }
        else{
            input_element = $("#pop_value_table_"+i).find('input');
            var value_item = {};

            for( var k = 0; k < input_element.length; k++){
                if( k == 0 ){   //Range 비교 첫번째 요소와 마지막 요소는 단일 값을 갖는다.
                    value_item = {
                        "range_id" : range_id++,
                        "max" : input_element[k].value
                    }
                }
                else if( k == input_element.length-1){
                    value_item = {
                        "range_id" : range_id++,
                        "min" : input_element[k].value
                    }
                }
                else{   //중간 요소는 입력필드 2개씩 쌍으로 사용한다.
                    value_item = {
                        "range_id" : range_id++,
                        "min" : input_element[k].value,
                        "max" : input_element[k+1].value
                    }
                    k++;
                }
                value_range.push(value_item);
            }
        }
        if (optype == "strbool"){
            item = {
                "link_id" :  linkvalue.substring(1,linkvalue.length),
                "link_type" : linkvalue[0],
                "st_data" : stdata,
                "operate_type" : optype,
                "value_range" : value_range
            };
        } else {
            item = {
                "link_id" :  linkvalue.substring(1,linkvalue.length),
                "link_type" : linkvalue[0],
                "st_data" : stdata,
                "operate_type" : optype,
                "value_range" : value_range
            };
        }


        operate_list.push(item);

    }

    name_element_list = $("[name=sector_name]");
    dna_name_list = [];

    for(var i =0; i < name_element_list.length; i ++){
        var row_id = name_element_list[i].id.replace("sector_name_","");
        ids = row_id. split("_");
        isImportantDNA = $("#sector_chk_"+row_id)[0].checked;
        isWhiteListApplied = $("#whitelist_chk_"+row_id)[0].checked;
        sector_comment = $("#sector_comment_"+row_id).val();

        dna_name_list.push(
            {
                "dna_name" : name_element_list[i].value,
                "range_ids" : ids,
                "isImportantDNA" : isImportantDNA,
                "isWhiteListApplied" : isWhiteListApplied,
                "desc" : complexed_desc[i],
                "comment" : sector_comment
            }
        )
    }

    dna_config = {
        "dna_operate_list" : operate_list,
        "dna_name_list" : dna_name_list
    };

    return dna_config;
}

function showEditDialog(){
    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('수정 할 아이템을 선택 해 주세요');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value

    initInputPopup();
    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    $('#pop_typea_tables').val(row.src_type);

    $('#pop_seq').val(row.id);
    $('#pop_name').val(row.dna_name);

    //Parse Operate Function
    opData = JSON.parse(row.operate_function);
    
    //링크 요소 입력 부분 초기화
    for (var k = 0; k < opData.dna_operate_list.length; k ++)
    {
        //input div 영역을 추가 한다.
        if(k > 0){
            add_inputdiv();
        }
        op_row = opData.dna_operate_list[k];
        var link_id = op_row.link_type + op_row.link_id;
        $("#pop_link_e_"+k).val(link_id);
        pop_link_e_changed('pop_link_e_'+k, 'pop_st_data_'+k);

        if ( op_row.operate_type != "in")
            $("#pop_st_data_"+k).val(op_row.st_data);
        else
            $("#pop_st_data_"+k).val("in");
        pop_st_data_changed("pop_st_data_"+k);
        $("#pop_op_type_"+k).val(op_row.operate_type);
        pop_op_type_changed('pop_op_type_'+k,'pop_op_'+k);

        if (op_row.operate_type == "strbool")
        {
            //$('pop_op_'+k).val('Equal');
            pop_op_changed_country('pop_op_'+k, 'pop_value_table_' + k);
            $("#pop_op_"+k).val(op_row.value_range[0].operate);
            pop_op_changed_country('pop_op_'+k, 'pop_value_table_' + k);
            $("#pop_input_simple_"+k).val(op_row.value_range[0].value);
        } else if(op_row.operate_type == "bool" ){
            pop_op_changed_simple('pop_op_'+k, 'pop_value_table_' + k);
            $("#pop_op_"+k).val(op_row.value_range[0].operate);
            pop_op_changed_simple('pop_op_'+k, 'pop_value_table_' + k);
            $("#pop_input_simple_"+k).val(op_row.value_range[0].value);



        }
        else if(op_row.operate_type == "in"){
            pop_op_changed_in('pop_op_'+k, 'pop_value_table_' + k);
            $("#pop_op_"+k).val(op_row.value_range[0].operate);
            value =
            $("#pop_input_simple_"+k).val(op_row.value_range[0].value.join());
        }
        else{
            $("#pop_op_"+k).val(op_row.value_range.length);
            pop_op_changed_range('pop_op_'+k, 'pop_value_table_' + k);

            input_counter = 0;
            for(var i = 0; i < op_row.value_range.length; i ++){
                if( i == 0){
                    $("#pop_value_table_"+k).find('input')[input_counter].value = op_row.value_range[i].max;
                }
                else if ( i == op_row.value_range.length-1){
                    $("#pop_value_table_"+k).find('input')[input_counter].value = op_row.value_range[i].min;
                }
                else{
                    $("#pop_value_table_"+k).find('input')[input_counter].value = op_row.value_range[i].min;
                    input_counter++;
                    $("#pop_value_table_"+k).find('input')[input_counter].value = op_row.value_range[i].max;
                }
                input_counter++;
            }
        }
    }

    //DNA 섹터 부분 초기화
    make_dna_sector();
    for( var i =0; i < opData.dna_name_list.length; i ++){
        $("[name='sector_name']")[i].value = opData.dna_name_list[i].dna_name;
        $("[name='sector_comment']")[i].value = opData.dna_name_list[i].comment;

        if( opData.dna_name_list[i].isImportantDNA)
            $("[name='radio_important']")[i].checked = true;

        if( opData.dna_name_list[i].isWhiteListApplied)
            $("[name='radio_whitelist']")[i].checked = true;
    }


    $('#btnAdd_Submit').hide();
    $('#btnEdit_Submit').show();
    $('#modal-popup').modal();
}

function deleteItem(seq){
    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('삭제 할 아이템을 선택 해 주세요');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value
    seq = $('#demo-foo-filtering').DataTable().data()[rownum].id;

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    if( result) {
        url = "/dna/manage/"+seq;

        var request = $.ajax({
            url: url,
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

function OppositionFunction(op){

    switch (op){
        case "<" :
            return ">=";
        case "<=" :
            return ">";
        case ">" :
            return "<=";
        case ">=" :
            return "<";
        case "=" :
            return "!=";
        case "!=" :
            return "=";
        case "in" :
            return "not in";
        default:
            return "";
    }
}