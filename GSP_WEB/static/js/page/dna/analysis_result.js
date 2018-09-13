var curpage = 1;
var columnList = [];
var columnDef = {};
var dnaList;

function downloadExcel(){

    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
        search_src_ip : $("#search_src_ip").val(),
        search_dst_ip : $("#search_dst_ip").val(),
        search_dna : $('#searchDna').val(),
        search_dna_name : $('#searchDna option:selected').text(),
        search_sector : $('#searchSector').val()
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
    form.setAttribute('action', "/dna/analysis_result/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

function getDnaList(dna, sector, whiteList, showWhiteListFalse){

    $.ajax({
        url: "/dna/get-list",
        "type": 'GET',
        success: function (data) {
        dataType: "json",
            dnaList = [];
            dnaList = data.data;

            $("#searchDna").empty();
            var option = new Option("DNA 전체", "");
            $("#searchDna").append(option);

            for(var i=0; i < dnaList.length; i++){
                var option = new Option(dnaList[i].dna_name, dnaList[i].id);
                $("#searchDna").append(option);
            }

            if(dna != null && sector != null){
                $("#searchDna").val(dna);
                searchDnaChanged();
                $("#searchSector").val(sector);
            }

            handleDataTableDefault(whiteList, showWhiteListFalse);
        }
    });
}

function searchDnaChanged(){
    dna = $("#searchDna").val();
    $("#searchSector").empty();
    var option = new Option("Sector 전체", "");
    $("#searchSector").append(option);

    for(var i=0; i < dnaList.length; i++) {
        if ( dna == dnaList[i].id) {
            for(var j=0; j < dnaList[i].sector_list.length; j++  ) {
                option = new Option(dnaList[i].sector_list[j].name, dnaList[i].sector_list[j].name);
                $("#searchSector").append(option);
            }
        }
    }
}

function DatatableReload(){

    dtTable.ajax.reload(function(data){
        dtTable.page.len($("#perpage").val()).draw();
        $('#divTotal').text("총 "+data.recordsFiltered.toLocaleString() + "건");
    });

}

function getColdef(_columnList){
    colDef = [];

    rownum = {
        "targets" : 0,
        "width" : "80px"
    }
    colDef.push(rownum);

    linkDef = {
        "targets" : 1,
        "width" : "400px",
        "render" : function(data, type, row, meta){
            html = "<a href='/links/analysis_result?src_ip={0}&dst_ip={1}'>{2}</a>"
                .format(row['_source']['src_ip'],row['_source']['dst_ip'],data.replace("_"," → "));
            return html;
        }
    }
    colDef.push(linkDef);

    for( var i = 2; i < _columnList.length; i ++){
        var div_id = String(_columnList[i].title);

        var colNames = columnList[i-1].data.split('.');
        var desc = '';

        var _def =
         {
            "targets": i,
             "width" : "400px",
             "render": function (data, type, row, meta) {

                var dna_name = columnList[meta.col].data.split('.')[1];

                 for( var j = 0; j < dnaList.length; j++){
                     if ( dnaList[j].dna_name == dna_name){
                         for( var k =0; k < dnaList[j].sector_list.length; k++){
                             if( dnaList[j].sector_list[k].name == data){
                                 desc = dnaList[j].sector_list[k].comment;
                                 desc = desc.replace(/'/gi,"");
                                 desc = desc.replace(/\r/gi,"<br>");
                             }
                         }
                     }
                 }

                 html = "<span data-toggle='tooltip' data-placement='right' title='"+desc+"'>"+data+"</span>";

                 return html;
                 //return btnHtml;
             }
        }

        colDef.push(_def);
    }

    columnDef = colDef;

    return colDef;
}

var handleDataTableDefault = function(whiteList, showWhiteListFalse) {

    $.ajax({
        url: "/dna/analysis_result/columnlist",
        dataType: "json",
        success: function (colData) {
            columnList = colData;
            getColdef(columnList);

            if ($('#dtTable').length !== 0) {
                dtTable = $('#dtTable').DataTable({
                    "drawCallback": function (settings) {
                        $('.pagination').css('display', 'table');
                        $('[data-toggle="tooltip"]').tooltip({html: true});
                    },
                    ajax: {
                        url: "/dna/analysis_result/list",
                        "type": 'POST',
                        "data": function (d) {
                            d['curpage'] = curpage;
                            d['perpage'] = $("#perpage").val();
                            d['search_type'] = $("#keywordType").val();
                            d['search_src_ip'] = $("#search_src_ip").val();
                            d['search_dst_ip'] = $("#search_dst_ip").val();
                            d['search_dna'] = $('#searchDna').val();
                            d['search_dna_name'] = $('#searchDna option:selected').text();
                            d['search_sector'] = $('#searchSector').val();
                            d['whiteList'] = whiteList;
                            d['showWhiteListFalse'] = showWhiteListFalse;
                            $('#tblDetail').empty();
                        }
                    },
                    dataFilter: function (data) {
                        var json = jQuery.parseJSON(data);
                        json.recordsTotal = json.total;
                        json.recordsFiltered = json.total;
                        json.data = json.list;

                        return JSON.stringify(json); // return JSON string
                    },
                    "initComplete": function (settings, json) {
                        $("#divSearch").loading('stop');
                        $('#divTotal').text("총 "+json.recordsFiltered.toLocaleString() + "건");
                        $('#tblDetail').empty();

                    },
                    error: function (xhr, error, thrown) {
                        alert(error);
                        $("#divSearch").loading('stop');
                        error(xhr, error, thrown);
                    },
                    dom: 'Bfrtip',
                    "pagingType": "full_numbers",
                    fixedHeader: true,
                    "scrollY" : "800px", //height adjustment according to the new UI requirement.
                    autoWidth : true,
                    serverSide: true,
                    pageLength: $("#perpage").val(),
                    bLengthChange: true,
                    processing: true,
                    searching: false,
                    "scrollX": true,
                    sort: false,
                    paging: true,
                    info: false,
                    deferRender: true,
                    select: 'true',
                    "jQueryUI": true,
                    "sPaginationType": "full_numbers",
                    columns: colData,
                    columnDefs : columnDef
                });

            };

            $.fn.dataTable.ext.errMode = 'none';
            $('#dtTable_paginate').attr('class', 'pagination pagination-split footable-pagination m-t-10 m-b-0');
            $('#dtTable_paginate').css('margin', '0 auto');

        }
    });

}

var TableManageDefault = function () {
	"use strict";
    return {
        //main function
        init: function () {
            //getDnaList();
            //handleDataTableDefault(); <-- 이 함수는 getDnaList의 ajax success 이후에 호출됨
        }
    };
}();