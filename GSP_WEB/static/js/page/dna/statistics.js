

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        //$('.table-sc01').loading();
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/dna/statistics/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.keywordType = $("#keywordType").val();
                        d.search_keyword = $("#search_keyword").val();
                    }
                },
                'rowsGroup' : [0,2],
                dataFilter: function(data){
                var json = jQuery.parseJSON( data );
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                json.data = json.list;

                return JSON.stringify( json ); // return JSON string
            },
            "initComplete": function(settings, json){
                    $('.table-sc01').loading('stop');
                    $('#divTotal').text("총 "+json.dna_name_count + "건");
                    //dtTable.rowsgroup.update();
              },
            error: function(xhr, error, thrown) {
                $('.table-sc01').loading('stop');
                alert(error);
                error(xhr, error, thrown);
            },
            dom: 'Bfrtip',
            "pagingType": "full_numbers",
            fixedHeader: true,
            serverSide: true,
            pageLength: 100,
            bLengthChange: false,
            processing: true,
            searching: false,
            sort: false,
            paging: true,
            bPaginate: true,
            info: false,
            deferRender: true,
            responsive: true,
            "scrollY" : "800px",
            //select: 'single',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    data : "dna",
                    label: "DNA 명"
                },
                {
                    data : "sector",
                    label: "DNA 섹터"
                },
                {
                    data : "totalLinkCount",
                    label: "분석 대상"
                },{
                    data : "dna_count",
                    label: "DNA확정"
                },{
                    data : "sector_count_whitelist",
                    label: "검출결과"
                },{
                    data : "sector_percent",
                    label: "점유율"
                },{
                    data : "isimportant",
                    label: "중요 DNA"
                },{
                    data : "desc",
                    label: "설명"
                }
            ],
            columnDefs : [
                {
                    "targets" : 1,
//                    "render" : function(data,type, row, meta){
//                        href = "/dna/analysis_result?dna={0}&sector={1}".format(row.dna_id, row.sector);
//                        var html = "<a href='{0}'>{1}</a>".format(href,data);
//                        return html
//                    }
                }
                ,
                {
                    "targets" : 2,
                    "render" : function(data,type, row,meta){
                        return row.totalLinkCount.toLocaleString();
                    }
                },
                {
                    "targets" : 3,
                    "render" : function(data,type, row,meta){
                        return row.dna_count.toLocaleString();
                    }
                },
                {
                    "targets" : 4,
                    "render" : function(data,type, row,meta){
                        var per = row.sector_count * 100 / row.dna_count ;
                        var text = "{0}".format(row.sector_count.toLocaleString());
                        var textWhiteListCount = "{0}".format(row.sector_count_whitelist.toLocaleString());
                        var isWhiteListApplied = "{0}".format(row.isWhiteListApplied.toLocaleString());
                        var whiteListTrue = "true";
                        var whiteListFalse = "false";
                        var showWhiteListFalse = "true";
                        var textTotalListCount = "{0}".format(row.sector_count.toLocaleString());


                        href1 = "/dna/analysis_result?dna={0}&sector={1}&whitelist={2}".format(row.dna_id, row.sector, whiteListFalse);
                        href2 = "/dna/analysis_result?dna={0}&sector={1}&whitelist={2}&showWhiteListFalse={3}".format(row.dna_id, row.sector, whiteListTrue, showWhiteListFalse);
//                        if(row.sector_count_whitelist > 0){
//                            var html = "<a href='{0}'>{1}  / <a href='{2}'>{3}</a>".format(href1,textTotalListCount, href2, textWhiteListCount);
//                        } else {
//                            var html = "<a href='{0}'>{1}</a>".format(href1, textTotalListCount);
//                        }
                        if(isWhiteListApplied === "true"){
                            var html = "<a href='{0}'>{1}</a> / <a href='{2}'>{3}</a>".format(href1,textTotalListCount, href2, textWhiteListCount);
                        } else {
                            var html = "<a href='{0}'>{1}</a> / 0".format(href1,textTotalListCount);
                        }
                        return html;
                    }
                },
                {
                    "targets" : 5,
                    "render" : function(data,type, row,meta){
                        //var per = row.sector_count * 100 / row.dna_count ;
                        var text = "{0}%".format(data.toLocaleString(undefined, {maximumFractionDigits:2}));

                        return text;
                    }
                },
                {
                    "targets" : 6,
                    "render" : function(data,type, row,meta){
                        if(row.isimportant){
                            return "O";
                        }
                        else{
                            return "X";
                        }
                    }
                },
                {
                    "targets" : -1,
                    "render" : function(data,type, row,meta){
                        var comment = ( row.comment.trim().length == 0 ? "-" : row.comment );
                        var desc = row.desc.replace(/\r/gi, "<br>").replace(/'/gi, "").replace( /\[/gi, "").replace( /\]/gi, "");
                        html = "<span data-toggle='tooltip' data-placement='left' title='" + desc + "'>" + comment + "</span>";
                        return html;
                    }
                }
                ],
            rowsGroup : [0,2,3]
        }).on('draw.dt', function(){
            //dtTable.rowsgroup.update();
            $('[data-toggle="tooltip"]').tooltip({html: true});
        });

        $.fn.dataTable.ext.errMode = 'none';

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

        },
        draw : function(){
            //MergeGridCells();
        },

    };
}();

var handleDataTableDefault = function() {
    GetList();
    //MergeGridCells();
};

function DatatableReload() {
    //$('.table-sc01').loading();

    GetList();
    return;
    $('#demo-foo-filtering').DataTable().ajax.reload(function (data) {
        $('#divTotal').text("총 " + data.recordsFiltered.toLocaleString() + "건");
        $('.table-sc01').loading('stop');
    })
};

function MergeGridCells() {

    var dimension_cells = new Array();
    var dimension_col = new Array();

    var i = 1;
    // First, scan first row of headers for the "Dimensions" column.
    $("#demo-foo-filtering").find('th').each(function () {
        if ($(this).text() == 'Timestamp') {
            dimension_col.push(i);
        }
        i++;
    });

    for( var k =0; k < dimension_col.length; k++) {

        if (dimension_col.indexOf(k) < 0)
            continue;


    }

    // first_instance holds the first instance of identical td
    var first_instance = null;
    var rowspan = 1;

    // iterate through rows
    $("#demo-foo-filtering").find('tr').each(function (idx) {

        // find the td of the correct column (determined by the dimension_col set above)
        var dimension_td = $(this).find('td:nth-child(1)');

        if (first_instance == null) {
            // must be the first row
            first_instance = dimension_td;
        } else if (dimension_td.text() == first_instance.text()) {
            // the current td is identical to the previous
            // remove the current td
            dimension_td.remove();
            ++rowspan;
            // increment the rowspan attribute of the first instance
            first_instance.attr('rowspan', rowspan);
        } else {
            // this cell is different from the last
            first_instance = dimension_td;
            rowspan = 1;
        }

    });

    var first_instance = null;
    var rowspan = 1;

    // iterate through rows
    $("#demo-foo-filtering").find('tr').each(function (idx) {

        // find the td of the correct column (determined by the dimension_col set above)
        var dimension_td = $(this).find('td:nth-child(2)');

        if (first_instance == null) {
            // must be the first row
            first_instance = dimension_td;
        } else if (dimension_td.text() == first_instance.text()) {
            // the current td is identical to the previous
            // remove the current td
            dimension_td.remove();
            ++rowspan;
            // increment the rowspan attribute of the first instance
            first_instance.attr('rowspan', rowspan);
        } else {
            // this cell is different from the last
            first_instance = dimension_td;
            rowspan = 1;
        }

    });

}