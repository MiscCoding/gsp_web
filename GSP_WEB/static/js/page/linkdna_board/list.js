var curpage = 1;

function DatatableReload(){

    dtTable.ajax.reload(function(){

    });

}

var handleDataTableDefault = function() {

    $.ajax({
        url: "/linkdnaboard/grouplist",
        dataType: "json",
        success: function (colData) {

            if ($('#dtTable').length !== 0) {
                dtTable = $('#dtTable').DataTable({
                    "drawCallback": function (settings) {

                    },
                    ajax: {
                        url: "/linkdnaboard/list",
                        "type": 'POST',
                        "data": function (d) {
                            d['curpage'] = curpage;
                            d['perpage'] = $("#perpage").val();
                            d['search_src_ip'] = $("#search_src_ip").val();
                            d['search_dst_ip'] = $("#search_dst_ip").val();
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
                        $('#tblDetail').empty();
                    },
                    error: function (xhr, error, thrown) {
                        alert(error);
                        $("#divSearch").loading('stop');
                        error(xhr, error, thrown);
                    },
                    dom: 'Bfrtip',
                    "pagingType": "full_numbers",
                    serverSide: true,
                    pageLength: 20,
                    bLengthChange: false,
                    processing: true,
                    searching: false,
                    sort: false,
                    paging: true,
                    info: false,
                    deferRender: true,
                    select: 'true',
                    "scrollX": true,
                    "jQueryUI": true,
                    "sPaginationType": "full_numbers",
                    columns: colData
                });

            };

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
            handleDataTableDefault();
        }
    };
}();