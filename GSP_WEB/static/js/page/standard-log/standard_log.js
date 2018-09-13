// var handleDataTableDefault = function() {
//
//     var url = "/standard-log/getlist";
//
//     jQuery.ajax({
//         type: "GET",
//         url: url,
//         dataType: "JSON", // 옵션이므로 JSON으로 받을게 아니면 안써도 됨
//
//         success: function (data) {
//
//             trTag = "<tr><td>"+data.cre_dt+"</td><td>"+data.id+"</td><td>"+data.ip+"</td><td><img src=\"/static/img/normal-n.png\" alt=\"정보\" />"+td.importance+"</td><td class=\"text-le\">"+data.description+"</td></tr>";
//             $('$tdTbody').append();
//         },
//
//         complete: function (data) {
//
//         },
//
//         error: function (xhr, status, error) {
//             alert("에러발생");
//         }
//     });
//
// }

var handleDataTableDefault = function() {
    getLogData();
}

var curpage = 1;
function getLogData(){
    $.ajax({
        url: "/standard-log/getlist",
        type: "POST",
        data : {
            "curpage" : curpage,
            "perpage" : $("#perpage").val()
        },
        dataType: "json",
        success:function(data){
                for(i = 0; i < data.data.length; i ++){
                    row = data.data[i]
                    var td_cre_dt = '<tr><td>' + row.cre_dt + '</td>';
                    var td_id = '<td>' + row.id + '</td>';
                    var td_ip = '<td>' + row.ip + '</td>';
                    var td_importance = '';
                    if( row.importance == '1')
                        td_importance =  '<td><img src="/static/img/normal-n.png" alt="정보" />정보</td>';
                    else
                        td_importance =  '<td><img src="/static/img/normal-w.png" alt="정보" />경고</td>';
                    var td_description = '<td class="text-le">' + row.description + '</td></tr>';

                    trTag = td_cre_dt  + td_id + td_ip + td_importance + td_description;
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