var dtTable

function DatatableReload(){
    $('#divSearch').loading();

    var _form = $("#formSearch");
    _form.parsley().validate();

    if( !_form.parsley().validationResult) {
        $("#divSearch").loading('stop');
        return false;
    }

    dtTable.ajax.reload(function(){
        $("#divSearch").loading('stop');
        $('#tblDetail').empty();
    });


    reloadData();
}

function detailFormat ( d , rownum) {
    // `d` is the original data object for the row

    var table = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;min-width:800px">';
    var tr = '<tr><th>패킷수 </th>';
    tr += '<td>{0}</td></tr>'.format( nullableStringFormat(d._source.in_pkts));
    tr += '<tr><th>패킷량 </th>';
    tr += '<td>{0}</td></tr>'.format( getReadableFileSizeString(d._source.in_bytes));
    tr += '<tr><th>TCP Flag </th>';
    tr += '<td>' + "URG: {0} / ACK: {1} / PSH: {2} / RST: {3} / SYN: {4} / FIN: {5}"
            .format(nullableStringFormat(d._source.tcp_flags_URG)
                , nullableStringFormat(d._source.tcp_flags_ACK)
                , nullableStringFormat(d._source.tcp_flags_PSH)
                , nullableStringFormat(d._source.tcp_flags_RST)
                , nullableStringFormat(d._source.tcp_flags_SYN)
                , nullableStringFormat(d._source.tcp_flags_FIN)
            )
        + '</td></tr>';
    tr += '<tr><th>지리적 거리 </th>';
    tr += '<td>' + nullableStringFormat(d._source.geoip_distance) + ' km</td></tr>';
    // tr += '<tr><th>uri</th>';
    // tr += '<td>' + data['analysis_results']['uri'] + '</td></th>';
    // tr += '<tr><th>MD5(SHA)</th>';
    // tr += '<td>' + data['analysis_results']['md5'] + '</td></th>';
    // tr += '<tr><th>분석 결과</th>';
    // tr += '<td>' + data['analysis_results']['security_level'] + '</td></th>';
    if(d._source.syslog_name != null){
        tr += '<tr><th>Syslog명</th><td>'+ d._source.syslog_name +'</td></tr>';
        tr += '<tr><th>Syslog Message</th><td>'+ d._source.msg +'</td></tr>';
            }

    html = table + tr + "</table>";

    return html;

}

var handleDataTableDefault = function() {
    $('#divSearch').loading();

    if ($('#dtTable').length !== 0) {
        dtTable = $('#dtTable').DataTable({
            "drawCallback": function( settings ) {
                $("#dtTable thead").remove();
                },
            ajax: {
                url: "/5tuple/getlist-es",
                "type": 'POST',
                "data": function (d) {
                    postData = makePostData();
                    for (var _data in postData) {
                        d[_data] = postData[_data];
                    }
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
            "initComplete": function(settings, json){
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
            "autoWidth": true,
            deferRender: true,
            responsive: true,
            select: 'true',
            "sPaginationType": "full_numbers",
            columns: [
                {
                    "className":      'details-control',
                    "orderable":      false,
                    "data":           null,
                    "defaultContent": ''
                },
                {
                    data: "display_time",
                    label: "타임스탬프",
                    render : function(data, type, row){
                        return formatDate(data);
                    }
                }, {
                    data: "_source.protocol",
                    label: "프로토콜"
                }, {
                    data: "_source.src_ip",
                    label: "출발 IP"
                }, {
                    data: "_source.src_port",
                    label: "출발 Port"
                }, {
                    data: "_source.dst_ip",
                    label: "목적 IP"
                }, {
                    data: "_source.dst_port",
                    label: "목적 Port"
                }, {
                    data: "_source.data_type",
                    label: "데이터 소스"
                }
            ],
            columnDefs : [ {
                    "targets":1,
                    "render" : function (data, type, row, meta){
                        row._id;
                        var date = new Date(row._source.session_min_time);
                        return date.tostring();
                    }
                },{
                    "targets": 3,
                    "render" : function (data, type, row, meta){
                        //row._id
                        var html = row._source.src_ip
                        if( row._source.src_country_code != "")
                            html += " (" + row._source.src_country_code + ")";
                        return html;
                    }
                },{
                    "targets": 4,
                    "render" : function (data, type, row, meta){
                        //row._id

                        if( row._source.src_port != null)
                            return row._source.src_port;
                        else
                            return "-";
                    }
                },{
                    "targets": 5,
                    "render" : function (data, type, row, meta){
                        //row._id
                        var html = row._source.dst_ip
                        if( row._source.dst_country_code != "")
                            html += " (" + row._source.dst_country_code + ")";
                        return html;
                    }
                },{
                    "targets": 6,
                    "render" : function (data, type, row, meta){
                        if( row._source.dst_port != null)
                            return row._source.dst_port;
                        else
                            return "-";
                    }
                }]
        });

        $('#dtTable tbody').on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = dtTable.row( tr );

            if ( row.child.isShown() ) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                // Open this row
                rownum = row[0][0];
                row.child( detailFormat(row.data(), rownum) ).show();
                tr.addClass('shown');
            }
        } );

        //dtTable.columns.adjust().draw();

        dtTable.on('select', function (e, dt, type, indexes) {
            var rowData = dtTable.row(indexes).data();
            var _data = {
                'search_time': rowData._source.min_timestamp,
                "src_ip" : rowData._source.svr_ip,
                "src_port" : rowData._source.svr_port,
                "dst_ip" : rowData._source.dst_ip,
                "dst_port" : rowData._source.dst_port
            };


        });

        //$("#dtTableToolbar").insertBefore( "#dtTable_paginate" );
    }

};

var curpage = 1;
function getLogData(){
    $.ajax({
        url: "/link-dna/getlist",
        type: "POST",
        data : {
            "curpage" : curpage,
            "perpage" : $("#perpage").val(),
            "start_dt" : $("#datepicker").val(),
            "end_dt" : $("#datepicker2").val()
        },
        dataType: "json",
        success:function(data){
                for(i = 0; i < data.data.length; i ++){
                    row =  JSON.parse(data.data[i]);
                    var sessionTimeMin = formatDate(new Date(row.session_time_min).toUTCString());
                    var td_0 = '<tr><td>' + row.start_time+ '</td>';
                    var td_1 = '<td>' + row.src_ip + '</td>';
                    var td_2 = '<td>' + row.src_port + '</td>';
                    var td_3 = '<td>' + row.dst_ip + '</td>';
                    var td_4 = '<td>' + row.dst_port + '</td>';
                    var td_5 = '<td>' + sessionTimeMin + '</td>';
                    var td_6 = '<td>' + row.protocol + '</td>';
                    var td_7 = '<td>' + row.s2c_btyes + '</td>';
                    var td_8 = '<td>' + row.s2c_packets + '</td>';
                    var td_9 = '<td>' + row.tcp_flags_ACK + '</td>';
                    var td_10 = '<td>' + row.tcp_flags_FIN + '</td>';
                    var td_11 = '<td>' + row.tcp_flags_PSH + '</td>';
                    var td_12 = '<td>' + row.tcp_flags_RST + '</td>';
                    var td_13 = '<td>' + row.tcp_flags_SYN + '</td>';
                    var td_14 = '<td>' + row.tcp_flags_URG + '</td></tr>';

                    trTag = td_0  + td_1 + td_2 + td_3 + td_4 + td_5 + td_6 + td_7 + td_8 + td_9 + td_10 + td_11 + td_12 + td_13 + td_14;
                    $('#tdTbody').append(trTag);
                }
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

String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    str = str.replace(reg, arguments[i]);
  }
  return str;
}

function nullToEmpty(value) {
  var str = value;
  if (value == null)
      return ""
  else
      return str;
}

function nullToDesc(value) {
  var str = value;
  if (value == null)
      return "해당 없음"
  else
      return str;
}

function showAddDialog(){
    $('#modal-AddProfile').modal();
    $('#search_profile_name').val('');
    $('#search_profile_description').val('');
    $('#formAddProfile').parsley().reset();
    return false;
}

function getProfileList(){
    var postData = Object();
    postData.perpage = 50;
    postData.draw = 0;
    postData.start = 0;
    postData.search_source = '';
    postData.search_keyword = '';

    var request = $.ajax({
        url:"/rules/profile/list",
        type:"POST",
        data:postData,
        success: function(data, status){
            $("#search_profile").empty();
            empty_row = '<option value="">프로파일 선택</option>';
            $("#search_profile").append(empty_row);
            for(i = 0; i < data.data.length; i++){
                var row = '<option value="'+ data.data[i].seq+'">'+data.data[i].name+'</option>';
                $("#search_profile").append(row);
            }
        },
        error: function(err, status, err2){
            alert(err.responseJSON.message);
        }
    });
}

function makePostData(){
    var postData = Object();
    postData.search_data_type = $("#search_data_type").val();
    postData.search_src_ip = $("#search_src_ip").val();
    postData.search_src_ip_opt = $("#search_src_ip_opt").val();
    postData.search_dst_ip = $("#search_dst_ip").val();
    postData.search_dst_ip_opt = $("#search_dst_ip_opt").val();
    postData.search_src_port_opt = $("#search_src_port_opt").val();
    postData.search_src_port_value = $("#search_src_port_value").val();
    postData.search_dst_port_opt = $("#search_dst_port_opt").val();
    postData.search_dst_port_value = $("#search_dst_port_value").val();
    postData.search_protocol_opt = $("#search_protocol_opt").val();
    postData.search_protocol_value = $("#search_protocol_value").val();
    postData.timeFrom = $("#dateFrom").val();
    postData.timeTo = $("#dateTo").val();
    postData.perpage = $("#perpage").val();
    postData.search_packet_opt = $("#search_packet_opt").val();
    postData.search_packet_value = $("#search_packet_value").val();
    postData.search_bytes_value = $("#search_bytes_value ").val();
    postData.search_bytes_opt = $("#search_bytes_opt").val();
    postData.search_flag_urg_opt = $("#search_flag_urg_opt").val();
    postData.search_flag_urg_value = $("#search_flag_urg_value").val();
    postData.search_flag_ack_opt = $("#search_flag_ack_opt").val();
    postData.search_flag_ack_value = $("#search_flag_ack_value").val();
    postData.search_flag_psh_opt = $("#search_flag_psh_opt").val();
    postData.search_flag_psh_value = $("#search_flag_psh_value").val();
    postData.search_flag_rst_opt = $("#search_flag_rst_opt").val();
    postData.search_flag_rst_value = $("#search_flag_rst_value").val();
    postData.search_flag_syn_opt = $("#search_flag_syn_opt").val();
    postData.search_flag_syn_value = $("#search_flag_syn_value").val();
    postData.search_flag_fin_opt = $("#search_flag_fin_opt").val();
    postData.search_flag_fin_value = $("#search_flag_fin_value").val();
    postData.search_geo_distance_opt = $("#search_geo_distance_opt").val();
    postData.search_geo_distance_value = $("#search_geo_distance_value").val();
    postData.search_src_country = $("#search_src_country").val();
    postData.search_dst_country = $("#search_dst_country").val();
    postData.search_syslog_name_opt = $("#search_syslog_name_opt").val();
    postData.search_syslog_name_value = $("#search_syslog_name_value").val();
    postData.search_msg_opt = $("#search_msg_opt").val();
    postData.search_msg_value = $("#search_msg_value").val();

    return postData;
}

function getReadableFileSizeString(fileSizeInBytes) {
    if(fileSizeInBytes == null)
        return "-";
    var i = -1;
    var byteUnits = [' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
    do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
    } while (fileSizeInBytes > 1024);

    return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
};

function getDetailPercentage(child, parent){
    if(child == 0)
        child = 1;
    if(parent == 0)
        parent = 1;

    return ((child*100/parent).toFixed(2));
}

function nullableStringFormat(obj){
    if( obj != null)
        return obj.toLocaleString(undefined, {maximumFractionDigits:2});
    else
        return "-";

}