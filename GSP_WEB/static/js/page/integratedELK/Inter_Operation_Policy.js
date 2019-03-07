function isFileValidate(){
    if ($("#pop_file").val() == '' )
        return false;
    else
        return true;
}

function makeEmptyRegisterEditDialogBox(){
        $("#pop_Type").val("");
        $("#pop_IPS_Policy").val("");
        $("#pop_IPS_Policy_No").val("");
        $("#pop_Mal_IP").val("");
        $("#pop_Target_IP").val("");
        $("#pop_Mal_IP_Type").val("");
        $("#pop_Regular_Exp_Name").val("");
        $("#sec_log_chkbox").prop("checked", false);
        $("#ti_log_chkbox").prop("checked", false);
        $("#pop_seq").val("");
}


function handleWhiteListDays (){

        $body.addClass("loading");

        var postData = new Object();
        postData.whitelistvalue = $('#whiteList_maintain_period').val();

        var request = $.ajax({
            url:"/ELK/IPS_management/whitelistPeriodSet",
            type:"PUT",
            data:postData,
            success: function(data, status){
                alert("White list store days has been set.");
                $body.removeClass("loading");
            },
            error: function(err, status, err2){
                $body.removeClass("loading");
                 alert(err.responseJSON.message);

            }
        });
}

function downloadExcel(){

    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        perpage : $("#perpage").val(),
        //search_type : $("#search_type").val(),
        //search_security_level : $("#search_security_level").val(),
        //search_keyword_type : $("#search_keyword_type").val(),
        search_keyword : $("#search_keyword").val(),
        search_keyword_type : $("#search_keyword_type").val()
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
    form.setAttribute('action', "/ELK/Inter_Operation_Policy/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}


function downloadExcelSample(){

    data = {
        sample: "yes"

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
    form.setAttribute('action', "/ELK/Inter_Operation_Policy/sample-excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}


function fileSubmit(){


        if( !isFileValidate())
        {
            alert("업로드할 파일을 선택 해 주세요");
            return false;
        }

        var formData = new FormData($("#formUpload")[0]);
        $body.addClass("loading");

        formData.append("file", $("#pop_file")[0].files[0]);
        $('#modal-popup-file').modal('toggle');
        var request = $.ajax({
            url:"/ELK/Inter_Operation_Policy/uploadlist",
            type:"POST",
            data:formData,
            processData:false,
            contentType: false,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();

                $('#pop_file_name').val("");
                $('.filebox .upload-hidden').val("");
                $body.removeClass("loading");

            },
            error: function(err, status, err2){
                 $('#demo-foo-filtering').DataTable().ajax.reload();
                 $('#pop_file_name').val("");
                 $('.filebox .upload-hidden').val("");
//                 $('#modal-popup-file').modal('toggle');
                 alert(err.responseJSON.message);
                 $body.removeClass("loading");
            }
        });
//    }

//    return false;

}

function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( $("#pop_IPS_Policy").val() !== '' && $("#pop_IPS_Policy_No").val() !== '') {

        var postData = new Object();
        postData.Type = $("#pop_Type").val();
        postData.IPS_Policy = $("#pop_IPS_Policy").val();
        postData.IPS_Policy_No= $("#pop_IPS_Policy_No").val();
        postData.SRC_IP_Type = $("#pop_Mal_IP").val();
        postData.DST_IP_Type = $("#pop_Target_IP").val();
        postData.Mal_IP_Type = $("#pop_Mal_IP_Type").val();
        postData.Regular_Exp_Name = $("#pop_Regular_Exp_Name").val();
        postData.Security_Log_Use = $("#sec_log_chkbox").prop('checked');
        postData.TI_Log_Use = $("#ti_log_chkbox").prop('checked');
//        postData.IP_Address = $("#pop_pattern").val();
//        postData.Password = $("#pop_IPS_password").val();
//        postData.Description = $("#pop_etc").val();
//        postData.desc = $('#pop_desc_drop').val();


        var request = $.ajax({
            url:"/ELK/inter-operation-policy-list",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
                DatatableReload();
                makeEmptyRegisterEditDialogBox();
            },
            error: function(err, status, err2, temp){
                 alert(err.responseJSON.message);
                 makeEmptyRegisterEditDialogBox();
            }
        });
    }

    return false;
}

function handleEditSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if($("#pop_IPS_Policy").val() !== '' && $("#pop_IPS_Policy_No").val() !== '') {

        var postData = new Object();
        postData.seq = $("#pop_seq").val();

        postData.Type = $("#pop_Type").val();
        postData.IPS_Policy = $("#pop_IPS_Policy").val();
        postData.IPS_Policy_No= $("#pop_IPS_Policy_No").val();
        postData.SRC_IP_Type = $("#pop_Mal_IP").val();
        postData.DST_IP_Type = $("#pop_Target_IP").val();
        postData.Mal_IP_Type = $("#pop_Mal_IP_Type").val();
        postData.Regular_Exp_Name = $("#pop_Regular_Exp_Name").val();
        postData.Security_Log_Use = $("#sec_log_chkbox").prop('checked');
        postData.TI_Log_Use = $("#ti_log_chkbox").prop('checked');

//        postData.Customer_Category = $("#pop_ELK_Category").val();
//        postData.Customer_Name = $("#pop_Customer_Name").val();
//        postData.IP_Address = $("#pop_IP_Address").val();
//        postData.Branch = $("#pop_Branch").val();
//        postData.IP_Address = $("#pop_pattern").val();
//        postData.Password = $("#pop_IPS_password").val();
//        postData.Description = $("#pop_etc").val();
//        postData.desc = $('#pop_desc_drop').val();


        var request = $.ajax({
            url:"/ELK/Inter_Operation_Policy/"+ postData.seq,
            type:"PUT",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
                makeEmptyRegisterEditDialogBox();
            },
            error: function(err, status, err2){
                 alert(err.responseJSON.message);
                 makeEmptyRegisterEditDialogBox();
            }
        });
    }

    return false;
}

function showEditDialog(id){
    makeEmptyRegisterEditDialogBox();
    if($('input[name=editFeature]input:checked').length == 0){
        alert('수정할 아이템을 선택하세요!');
        return
    }

    var rownum = $('input[name=editFeature]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
     $('#pop_seq').val(row.seq);
     $('#pop_Type').val(row.Type);
     $("#pop_IPS_Policy").val(row.IPS_Policy);
     $("#pop_IPS_Policy_No").val(row.IPS_Policy_No);
     $("#pop_Mal_IP").val(row.SRC_IP_Type);
     $("#pop_Target_IP").val(row.DST_IP_Type);
     $("#pop_Mal_IP_Type").val(row.Mal_IP_Type);
     $("#pop_Regular_Exp_Name").val(row.Regular_Exp_Name);
     $("#sec_log_chkbox").prop('checked', (row.Security_Log_Use === 'true'));
     $("#ti_log_chkbox").prop('checked', (row.TI_Log_Use === 'true'));
//     $('#pop_pattern').val(row.IP_Address);
//     $("#pop_IPS_password").val(row.Password)
//     $("#pop_etc").val(row.Description)
    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();

}

function deleteItem(){

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');
    var rownum = $('input[name=editFeature]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    if( result) {

        var request = $.ajax({
            url: "/ELK/Inter_Operation_Policy/" + row.seq,
            type: "DELETE",
            success: function (data, status) {
                //alert('success');
                $('#demo-foo-filtering').DataTable().ajax.reload();
                DatatableReload();
            },
            error: function (err, status) {
                alert(err.responseText);
            }
        });
    }

    return false;
}

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
       var dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/ELK/Inter_Operation_Policy/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();
                        d.search_keyword_type = $("#search_keyword_type").val();
                        if(($("#search_keyword_type").val() === "Security_Log_Use" || $("#search_keyword_type").val() === "TI_Log_Use") && $("#search_keyword").val() === "사용")
                        {
                            d.search_keyword = "true";
                        }
                        if($("#search_keyword").val() === "없음")
                        {
                            d.search_keyword = "none";
                        }


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
              $('#divTotal').text("총 "+json.recordsFiltered + "건");
              $("#divTotal").attr("data-value", json.recordsFiltered);
            },
            error: function(xhr, error, thrown) {
                alert(error);
                error(xhr, error, thrown);
            },
            dom: 'Bfrtip',
            "pagingType": "full_numbers",
            fixedHeader: true,
            "scrollY" : "600px",
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
                    data : null
                },

                {
                    data : "Type",
                    label: "타입"
                }
                ,
                {
                    data : "IPS_Policy",
                    label: "IPS정책명"
                }
                ,
                {
                    data : "IPS_Policy_No",
                    label: "IPS번호"
                }
                ,
                {
                    data : "SRC_IP_Type",
                    label: "SRC_IP유형"
                }
                ,
                {
                    data : "DST_IP_Type",
                    label: "DST_IP유형"
                }
                ,
                {
                    data : "Mal_IP_Type",
                    label: "Mal_IP 유형"
                }
                ,

//                {
//                    data : "IP_Address",
//                    label: "IP"
//                }
//                ,
//                {
//                    data : "url",
//                    label: "패턴(URL)",
//                    mDataProp: '패턴(URL)',
//                    mRender: function(value) {
//                             if(value !== null)
//                                return value.truncStr(30);
//                             else
//                                return "";
//                             }
//                },

                {
                    data : "Regular_Exp_Name",
                    label: "정규표현식"
                },
                {
                    data : null

                }
                ,
                {
                    data : null

                }

//                ,
//                {
//                    data : "type",
//                    label: "세부유형"
//                },
//                {
//                    data : "cre_dt",
//                    label: "등록일",
//                    mDataProp: 'cre_dt',
//                    mRender: function(value) {
//                             return formatDate(value);
//                             }
//                },
//                {
//                    data : "mod_dt",
//                    label: "수정일"
//                }
                
            ],
            columnDefs : [

                {
                    "targets": 0,
                    orderable: false,
                    className: 'select-check',
                   "render" :function (data, type, row, meta){
                        var btnHtml = '';
                        btnHtml = '<input type="radio" id="horns" name="editFeature" value="'+meta.row+'"/>';
                        return btnHtml;
                    }
                }
                ,
                {
                    "targets": 1,
                    orderable: false,
                    searchable: false

                }
                ,
                {
                    "targets": 5,

                   "render" :function (data, type, row, meta){
                        var booleanValue = row.SRC_IP_Type
                        var btnHtml = '';
                        if (booleanValue === "none")
                        {
                            btnHtml = '없음';
                            return btnHtml;
                        }
                        else
                        {
                            return row.SRC_IP_Type
                        }

//                        btnHtml = '<input type="radio" id="horns" name="editFeature" value="'+meta.row+'"/>';

                    }
                }
                ,
                {
                    "targets": 6,

                   "render" :function (data, type, row, meta){
                        var booleanValue = row.DST_IP_Type
                        var btnHtml = '';
                        if (booleanValue === "none")
                        {
                            btnHtml = '없음';
                            return btnHtml;
                        }
                        else
                        {
                            return row.DST_IP_Type
                        }
                    }
                }
                ,
                {
                    "targets": 7,

                   "render" :function (data, type, row, meta){
                        var booleanValue = row.Regular_Exp_Name
                        var btnHtml = '';
                        if (booleanValue === "none")
                        {
                            btnHtml = '없음';
                            return btnHtml;
                        }
                        else
                        {
                            return row.Regular_Exp_Name
                        }
                    }
                }
                ,
                {
                    "targets": 8,

                   "render" :function (data, type, row, meta){
                         var booleanValue = row.Mal_IP_Type
                        var btnHtml = '';
                        if (booleanValue === "none")
                        {
                            btnHtml = '없음';
                            return btnHtml;
                        }
                        else
                        {
                            return row.Mal_IP_Type
                        }
                    }
                }
                ,
                {
                    "targets": 9,

                   "render" :function (data, type, row, meta){
                        var booleanValue = row.Security_Log_Use
                        var btnHtml = '';
                        if (booleanValue === "true")
                        {
                            btnHtml = '사용';
                        }
                        else
                        {
                            btnHtml = '-';
                        }
//                        btnHtml = '<input type="radio" id="horns" name="editFeature" value="'+meta.row+'"/>';
                        return btnHtml;
                    }
                }
                ,
                {
                    "targets": 10,

                   "render" :function (data, type, row, meta){
                        var booleanValue = row.TI_Log_Use
                        var btnHtml = '';
                        if (booleanValue === "true")
                        {
                            btnHtml = '사용';
                        }
                        else
                        {
                            btnHtml = '-';
                        }
//                        btnHtml = '<input type="radio" id="horns" name="editFeature" value="'+meta.row+'"/>';
                        return btnHtml;
                    }
                }

            ],
            "drawCallback" : function(setting,data){
                    $("input:radio").on('click', function() {
                    // in the handler, 'this' refers to the box clicked on
                    var $box = $(this);
                    if ($box.is(":checked")) {
                        // the name of the box is retrieved using the .attr() method
                        // as it is assumed and expected to be immutable
                        var group = "input:radio[name='" + $box.attr("name") + "']";
                        // the checked state of the group/box on the other hand will change
                        // and the current value is retrieved using .prop() method
                        $(group).prop("checked", false);
                        $box.prop("checked", true);
                    } else {
                        $box.prop("checked", false);
                    }
                });
            }
            ,
            "order" : [[1, 'asc']]
        }).on('draw.dt order.dt search.dt', function () {
                dtTable.column(1, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                cell.innerHTML = i+1;
            });
        }).draw();


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
    });
}

function getReadableFileSizeString(fileSizeInBytes) {
    var i = -1;
    var byteUnits = [' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
    do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
    } while (fileSizeInBytes > 1024);

    return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
};

String.prototype.truncStr = String.prototype.truncStr ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '&hellip;' : this;
      };

function formatDate(date) {
    date = date.replace(" GMT", "");
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    var hour = d.getHours(),
        minutes = d.getMinutes(),
        seconds = d.getSeconds();

        hour = ("0" + hour).slice(-2);
        minutes = ("0" + minutes).slice(-2);
        seconds = ("0" + seconds).slice(-2);


    return [year, month, day].join('-') + " " + [hour, minutes, seconds].join(':');
}

