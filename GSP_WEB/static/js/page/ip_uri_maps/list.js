function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        $('.table-sc01').loading();
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/ip-uri-maps/getlist",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.keywordType = $("#keywordType").val();
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
                    $('.table-sc01').loading('stop');
                    $('#divTotal').text("총 "+json.recordsFiltered + "건");
              },
            error: function(xhr, error, thrown) {
                $('.table-sc01').loading('stop');
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
                    data : "display_time",
                    label: "타임스탬프"
                },
                {
                    data : "_source.dst_ip",
                    label: "IP 주소"
                },{
                    data : "_source.uri",
                    label: "설명"
                }
            ],
            columnDefs : [
                {
                    "targets" : 2,
                    "width" : "55%",
                    "render" : function(data,type, row,meta){
                        var btnHtml = '<div style="max-width:1000px;word-wrap:break-word">'+ row._source.uri+'</div>';
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
};

function DatatableReload() {
    $('.table-sc01').loading();
    $('#demo-foo-filtering').DataTable().ajax.reload(function (data) {
        $('#divTotal').text("총 " + data.recordsFiltered.toLocaleString() + "건");
        $('.table-sc01').loading('stop');
    })
};