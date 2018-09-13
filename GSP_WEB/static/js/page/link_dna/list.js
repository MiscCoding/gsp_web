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
    var tr = '<tr><th>전송량 </th>';
    tr += '<td>{0}</td></tr>'.format(getReadableFileSizeString(d._source.bytes));
    tr += '<tr><th>패킷수 </th>';
    tr += '<td>{0}</td></tr>'.format( nullableStringFormat(d._source.pkts));
    tr += '<tr><th>세션유지시간 </th>';
    tr += '<td>' + nullableStringFormat(d._source.differ_time) + ' sec</td></tr>';
    tr += '<tr><th>세션수 </th>';
    tr += '<td>' + nullableStringFormat(d._source.session_cnt) + '</td></tr>';
    tr += '<tr><th>TCP Flag </th>';
    tr += '<td>' + "URG: {0}%, {1} / ACK: {2}%, {3} / PSH: {4}%, {5} / RST: {6}%, {7} / SYN: {8}%, {9} / FIN: {10}%, {11}"
            .format(nullableStringFormat(d._source.tcp_flags_URG_P)
                , nullableStringFormat(d._source.tcp_flags_URG)
                , nullableStringFormat(d._source.tcp_flags_ACK_P)
                , nullableStringFormat(d._source.tcp_flags_ACK)
                , nullableStringFormat(d._source.tcp_flags_PSH_P)
                , nullableStringFormat(d._source.tcp_flags_PSH)
                , nullableStringFormat(d._source.tcp_flags_RST_P)
                , nullableStringFormat(d._source.tcp_flags_RST)
                , nullableStringFormat(d._source.tcp_flags_SYN_P)
                , nullableStringFormat(d._source.tcp_flags_SYN)
                , nullableStringFormat(d._source.tcp_flags_FIN_P)
                , nullableStringFormat(d._source.tcp_flags_FIN)
            )
        + '</td></tr>';
    tr += '<tr><th>지리적 거리 </th>';
    tr += '<td>' + nullableStringFormat(d._source.geoip_distance) + ' km</td></tr>';
    tr += '<tr><th>패킷 탐지명</th>';
    tr += '<td>' + nullToDesc(d._source.alert_signature) + '</td></th>';
    tr += '<tr><th>파일명</th>';
    tr += '<td id="row' + rownum + '_fileName">불러오는중..</td></tr>';
    tr += '<tr id="tr' + rownum + '_thrd" style="display:none">';
    tr += '<th id="th' + rownum + '_thrd"></th>';
    tr += '<td id="row' + rownum + '_thrd"></td></tr>';
    if(d._source.syslog_name != null){
        tr += '<tr><th>Syslog명</th><td>'+ d._source.syslog_name +'</td></tr>';
        tr += '<tr><th>Syslog Message</th><td>'+ d._source.msg +'</td></tr>';
            }

    html = table + tr + "</table>";

    var _data = {
        'start_time': d._source.session_min_time,
        'end_time': d._source.session_max_time,
        "src_ip" : d._source.src_ip,
        "src_port" : d._source.src_port,
        "dst_ip" : d._source.dst_ip,
        "dst_port" : d._source.dst_port
    };

    $.ajax({
        url: "/link-dna/getdetail",
        data: _data,
        dataType: "json",
        success: function (data) {

            if(data.analysis_results != null && data.analysis_results.file_name != null && data.analysis_results.file_name != "") {
                row_file = "파일명:{0}, uri:{1}, 결과:{2}".format(
                    data.analysis_results.file_name, data.analysis_results.uri, data.analysis_results.security_level
                );
                $("#row"+rownum+"_fileName").text(row_file);
            }
            else{
                $("#row"+rownum+"_fileName").text(nullToDesc(null));
            }

        }
    });

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
                url: "/link-dna/getlist-es",
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
                    label: "타임스탬프"
                }, {
                    data: "_source.protocol",
                    label: "프로토콜"
                }, {
                    data: "_source.src_ip",
                    label: "Source IP"
                }, {
                    data: "_source.src_port",
                    label: "출발 Port"
                }, {
                    data: "_source.dst_ip",
                    label: "목적 IP"
                }, {
                    data: "_source.dst_port",
                    label: "목적 IP"
                }, {
                    data: "_source.data_type",
                    label: "데이터 소스"
                }, {
                    data: "_source",
                    label: "프로파일"
                }
            ],
            columnDefs : [ {
                    "targets": 3,
                    "render" : function (data, type, row, meta){
                        //row._id
                        var html = row._source.src_ip
                        if( row._source.src_country_code != "")
                            html += " (" + row._source.src_country_code + ")";
                        url = 'http://whois.kisa.or.kr/openapi/whois.jsp?query={0}&key=2018032013435689368141&answer=xml';
                        //window.open(url, 'ServerCon', "width=1280", "height=720");
                        return '<a style="text-decoration-line: underline" onclick="openWhoisWindow(\'' + row._source.src_ip + '\');">'+ html+'</a>'
                        //return html;
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

                        url = 'http://whois.kisa.or.kr/openapi/whois.jsp?query={0}&key=2018032013435689368141&answer=xml';
                        //window.open(url, 'ServerCon', "width=1280", "height=720");
                        return '<a style="text-decoration-line: underline" onclick="openWhoisWindow(\'' + row._source.dst_ip + '\');">'+ html+'</a>'
                        //return html;
                    }
                },{
                    "targets": 6,
                    "render" : function (data, type, row, meta){
                        //row._id
                        if( row._source.dst_port != null)
                            return row._source.dst_port;
                        else
                            return "-";
                    }
                },{
                    "targets": -1,
                    "render" : function (data, type, row, meta){
                        return nullToDesc(row._source.profile);
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
                "src_ip" : rowData._source.src_ip,
                "src_port" : rowData._source.src_port,
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
                    var td_7 = '<td>' + row.btyes + '</td>';
                    var td_8 = '<td>' + row.packets + '</td>';
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

function getProfile(){
    //empty value
    seq = $("#search_profile").val();
    if( seq == '')
        return false;

    $('#formSearch input[type="text"]').val("");
    $('#formSearch select[id!="search_profile"]').prop('selectedIndex', 0);

    $.ajax({
        url: "/rules/profile/"+seq,
        method:"GET",
        dataType: "json",
        success: function (data) {
            json = JSON.parse(data.pattern_ui);
            $("#search_profile_name").val(data.name);
            $("#search_profile_description").val(data.description);

            var _keys = Object.keys(json);
            for( i =0 ; i < _keys.length; i++)
            {
                if(_keys[i] == "perpage")
                    continue;
                $("#"+_keys[i]).val(json[_keys[i]]);
            };

            return false;
        }
    });

    return false;
}

function saveProfile (){
    var _form  = $('#formAddProfile')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var pattern_ui = makePostData();
        delete  pattern_ui['search_profile'];

        var json = JSON.stringify(pattern_ui);
        var postData = Object();
        postData.name = $("#search_profile_name").val();
        postData.description = $("#search_profile_description").val();
        postData.pattern_ui = json;

        var request = $.ajax({
            url:"/rules/profile",
            type:"POST",
            data:postData,
            success: function(data, status){
                getProfileList();
                $('#modal-AddProfile').modal('toggle');
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
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

function SearchServerCon(){
    url = "/link-dna/con-server-list?start_time={0}&end_time={1}&con_svr_from={2}&con_svr_to={3}".format(
        $("#dateFrom").val(), $("#dateTo").val(),$("#search_svr_con_count_value").val()
        ,$("#search_svr_con_count_value2").val());
    window.open(url, 'ServerCon', "width=1280", "height=720");
}

function SearchClientCon(){
    url = "/link-dna/con-client-list?start_time={0}&end_time={1}&con_cli_from={2}&con_cli_to={3}".format(
        $("#dateFrom").val(), $("#dateTo").val(),$("#search_cli_con_count_value").val()
        ,$("#search_cli_con_count_value2").val());
    window.open(url, 'ServerCon', "width=1280", "height=720");
}

function makePostData(){
    var postData = Object();
    postData.search_data_type = $("#search_data_type").val();
    postData.search_src_ip_value = $("#search_src_ip_value").val();
    postData.search_src_ip_opt = $("#search_src_ip_opt").val();
    postData.search_dst_ip_value = $("#search_dst_ip_value").val();
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
    postData.search_profile = $("#search_profile").val();
    postData.search_bytes_opt = $("#search_bytes_opt").val();
    postData.search_bytes_value = $("#search_bytes_value").val();
    postData.search_pkts_opt = $("#search_pkts_opt").val();
    postData.search_pkts_value = $("#search_pkts_value").val();
    postData.search_differ_time_opt = $("#search_differ_time_opt").val();
    postData.search_differ_time_value = $("#search_differ_time_value").val();
    postData.search_session_cnt_opt = $("#search_session_cnt_opt").val();
    postData.search_session_cnt_value = $("#search_session_cnt_value").val();
    postData.search_tcp_flag_URG_opt = $("#search_tcp_flag_URG_opt").val();
    postData.search_tcp_flag_URG_value = $("#search_tcp_flag_URG_value").val();
    postData.search_tcp_flag_ACK_opt = $("#search_tcp_flag_ACK_opt").val();
    postData.search_tcp_flag_ACK_value = $("#search_tcp_flag_ACK_value").val();
    postData.search_tcp_flag_PSH_opt = $("#search_tcp_flag_PSH_opt").val();
    postData.search_tcp_flag_PSH_value = $("#search_tcp_flag_PSH_value").val();
    postData.search_tcp_flag_RST_opt = $("#search_tcp_flag_RST_opt").val();
    postData.search_tcp_flag_RST_value = $("#search_tcp_flag_RST_value").val();
    postData.search_tcp_flag_SYN_opt = $("#search_tcp_flag_SYN_opt").val();
    postData.search_tcp_flag_SYN_value = $("#search_tcp_flag_SYN_value").val();
    postData.search_tcp_flag_FIN_opt = $("#search_tcp_flag_FIN_opt").val();
    postData.search_tcp_flag_FIN_value = $("#search_tcp_flag_FIN_value").val();
    postData.search_tcp_flag_URG_P_opt =   $("#search_tcp_flag_URG_P_opt").val();
    postData.search_tcp_flag_URG_P_value = $("#search_tcp_flag_URG_P_value").val();
    postData.search_tcp_flag_ACK_P_opt =   $("#search_tcp_flag_ACK_P_opt").val();
    postData.search_tcp_flag_ACK_P_value = $("#search_tcp_flag_ACK_P_value").val();
    postData.search_tcp_flag_PSH_P_opt =   $("#search_tcp_flag_PSH_P_opt").val();
    postData.search_tcp_flag_PSH_P_value = $("#search_tcp_flag_PSH_P_value").val();
    postData.search_tcp_flag_RST_P_opt =   $("#search_tcp_flag_RST_P_opt").val();
    postData.search_tcp_flag_RST_P_value = $("#search_tcp_flag_RST_P_value").val();
    postData.search_tcp_flag_SYN_P_opt =   $("#search_tcp_flag_SYN_P_opt").val();
    postData.search_tcp_flag_SYN_P_value = $("#search_tcp_flag_SYN_P_value").val();
    postData.search_tcp_flag_FIN_P_opt =   $("#search_tcp_flag_FIN_P_opt").val();
    postData.search_tcp_flag_FIN_P_value = $("#search_tcp_flag_FIN_P_value").val();
    postData.search_geoip_distance_opt = $("#search_geoip_distance_opt").val();
    postData.search_geoip_distance_value = $("#search_geoip_distance_value").val();
    postData.search_src_country_value = $("#search_src_country_value").val();
    postData.search_dst_country_value = $("#search_dst_country_value").val();
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

function openWhoisWindow(ip){
    url = 'http://whois.kisa.or.kr/openapi/whois.jsp?query={0}&key=2018032013435689368141&answer=xml'.format(ip);
    window.open(url, 'Whois', "width=1280", "height=720");
}