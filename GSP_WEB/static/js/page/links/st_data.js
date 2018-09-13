elementList = null;

function DrawChart(chartDiv, seriesData){
    /* Add a basic data series with six labels and values */

    var data = {
        //labels: ['1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6'],
        series: [
            {
                data: seriesData
            }
        ]
    };

    // var data = {
    //     labels: ['1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6'],
    //     series: [
    //         {
    //             data: ['1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6','1', '2', '3', '4', '5', '6']
    //         }
    //     ]
    // };

    /* Set some base options (settings will override the default settings in Chartist.js *see default settings*). We are adding a basic label interpolation function for the xAxis labels. */
    var options = {
        axisX: {
            showLabel: false,
            labelInterpolationFnc: function(value) {
                return 'Calendar Week ' + value;
            }
        }
    };

    /* Now we can specify multiple responsive settings that will override the base settings based on order and if the media queries match. In this example we are changing the visibility of dots and lines as well as use different label interpolations for space reasons. */
    var responsiveOptions = [
        ['screen and (min-width: 350px) and (max-width: 350px)', {
            showPoint: false,
            axisX: {
                labelInterpolationFnc: function(value) {
                    return 'Week ' + value;
                }
            }
        }],
        ['screen and (max-width: 350px)', {
            showLine: false,
            axisX: {
                labelInterpolationFnc: function(value) {
                    return 'W' + value;
                }
            }
        }]
    ];

    /* Initialize the chart with the above settings */
    new Chartist.Line('#'+chartDiv, data, options, responsiveOptions);
}

function handleShowAdd(){
    $('#pop_name').val("");
    $("#pop_file_name").val("선택된 파일 없음");

    $('#btnAdd_Submit').show();
    $('#btnEdit_Submit').hide();
    $('#modal-popup').modal();
}

var TableManageDefault = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleDataTableDefault();

        },
        draw : function(){

        },

    };
}();

var handleDataTableDefault = function() {
    GetList();
    //MergeGridCells();
};

function GetList(){


    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/links/st_data/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_keyword = $("#search_keyword").val();
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
                    data:null
                },
                {
                    data : "name",
                    label: "표준 데이터명"
                },{
                    data : "list_data",
                    label: "데이터"
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

                    "targets": 2,
                    "render" :function (data, type, row, meta){
                        var html = "<div id='list_data_"+meta.row+"'></div>"

                        return html;
                    }
                }
            ],
            "drawCallback" : function(setting,data){
                dtTable.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                    var data = this.data();

                    var _id = "list_data_" + rowIdx;
                    try {
                        if ($("#" + _id) != null)
                            DrawChart(_id, jQuery.parseJSON(data.list_data));
                    }
                    catch (exception) {
                    }

                    setTimeout(function(){
                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                    }, 350);

                });
            }
        });

        // $('#dtData').footable();
        // $("#dtTableToolbar").insertBefore( "#demo-foo-filtering_paginate" );

    }
}

function download(){
    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('다운로드 할 아이템을 선택 해 주세요');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value
    seq = $('#demo-foo-filtering').DataTable().data()[rownum].id;

    var link = document.createElement("a");
    link.download = name;
    link.href = "/links/st_data/download/"+seq;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}

function AddSubmit(){

    var _form  = $('#formUpload');
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        if( !isFileValidate())
        {
            alert("업로드할 파일을 선택 해 주세요");
            return false;
        }

        var formData = new FormData($("#formUpload")[0]);
        formData.append("name", $("#pop_name").val());
        formData.append("target_type", $("#pop_link").val()[0]);
        formData.append("target_seq", $("#pop_link").val().substr(1));
        formData.append("file", $("#pop_file")[0].files[0]);

        var request = $.ajax({
            url:"/links/st_data",
            type:"POST",
            data:formData,
            processData:false,
            contentType: false,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
                $('.filebox .upload-hidden').val(null);

            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
                 $('.filebox .upload-hidden').val(null);
            }
        });
    }

    return false;

}

function EditSubmit(){

    var _form  = $('#formUpload')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var formData = new FormData($("#formUpload")[0]);
        formData.append("name", $("#pop_name").val());
        formData.append("target_type", $("#pop_link").val()[0]);
        formData.append("target_seq", $("#pop_link").val().substr(1));
        formData.append("file", $("#pop_file")[0].files[0]);

        var request = $.ajax({
            url:"/links/st_data/"+$("#pop_seq").val(),
            type:"PUT",
            data:formData,
            processData:false,
            contentType: false,
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
    $('#pop_seq').val(row.id);
    $('#pop_name').val(row.name);
    $("#pop_link").val(row.target_link_type+ row.target_link_seq);
    $("#pop_file_name").val("선택된 파일 없음");
    $('#btnAdd_Submit').hide();
    $('#btnEdit_Submit').show();
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
        url = "/links/st_data/"+seq;
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

function DatatableReload(){
    $('#demo-foo-filtering').DataTable().ajax.reload(function(data){
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
        dtTable.page.len($("#perpage").val()).draw();
    });
}

function LoadLinkElement(){

    var request = $.ajax({
            url:"/links/element-list",
            type:"GET",
            success: function(data, status){
                _elementList = jQuery.parseJSON(data);
                elementList = new Array();
                for(i = 0; i < _elementList.TypeA.length; i++){
                    if(_elementList.TypeA[i].dst_data_type =="single" || _elementList.TypeA[i].dst_data_type =="map")
                        continue;
                    var dict = {};
                    dict["id"] = "a" + _elementList.TypeA[i].id;
                    dict["name"] = _elementList.TypeA[i].dst_columns_name;
                    dict["dst_data_type"] = _elementList.TypeA[i].dst_data_type;
                    dict["dst_data_size"] = _elementList.TypeA[i].dst_data_size;
                    elementList.push(dict);
                }
                for(i = 0; i < _elementList.TypeB.length; i++){
                    if(_elementList.TypeB[i].dst_data_type =="single" || _elementList.TypeB[i].dst_data_type =="map")
                        continue;
                    var dict = {};
                    dict["id"] = "b" + _elementList.TypeB[i].id;
                    dict["name"] = _elementList.TypeB[i].dst_columns_name;
                    dict["dst_data_type"] = _elementList.TypeB[i].dst_data_type;
                    dict["dst_data_size"] = _elementList.TypeB[i].dst_data_size;
                    elementList.push(dict);
                }

                $("#pop_link").empty();
                $("#pop_link").append("<option value='0'></option>")

                for(var i =0; i < elementList.length; i ++){
                    var option = document.createElement("option");
                    option.text = elementList[i].name;
                    option.value = elementList[i].id;
                    $("#pop_link").append(option);

                }

            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });

}

function isFileValidate(){
    if ($("#pop_file").val() == '' )
        return false;
    else
        return true;
}

function pop_link_changed(){
    selectedVal = $("#pop_link").val();
    if( selectedVal == "")
        $("#pop_div_desc").hide();
    else{
        $("#pop_div_desc").show();
        selectedElement = null;
        elementList.forEach(function(obj){
           if(obj.id == selectedVal)
               selectedElement = obj;
        });

        str_DataType = "";
        str_DataLength = "";

        if(selectedElement.dst_data_type == "list" && selectedElement.dst_data_size == null){
            str_DataType = "시계열 데이터";
            str_DataLength = "7 or 24 or 144"
        }
        else{
            str_DataType = "1차원 배열 데이터";
            str_DataLength = selectedElement.dst_data_size;
        }

        $("#pop_span_desc").text("{0} : {1}".format(str_DataType, str_DataLength));
    }
}