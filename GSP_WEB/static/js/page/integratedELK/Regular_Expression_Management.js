function isFileValidate(){
    if ($("#pop_file").val() == '' )
        return false;
    else
        return true;
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
    form.setAttribute('action', "/ELK/Regular_Expression_Management/excel-list")
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
    form.setAttribute('action', "/ELK/Regular_Expression_Management/sample-excel-list")
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
            url:"/ELK/Regular_Expression_Management/uploadlist",
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

    if( $("#pop_IPS").val() !== '' || $("#pop_pattern").val() !== '') {

        var postData = new Object();
        postData.Regular_Exp_Name = $("#pop_Regular_Exp_Name").val();
//        postData.IP_Address = $("#pop_pattern").val();
//        postData.Password = $("#pop_IPS_password").val();
        postData.Regular_Exp = $("#pop_Regular_Exp").val();
        postData.Description = $("#pop_etc").val();
//        postData.desc = $('#pop_desc_drop').val();


        var request = $.ajax({
            url:"/ELK/regular-expression-list",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
                DatatableReload();
            },
            error: function(err, status, err2, temp){
                 alert(err.responseJSON.message);
            }
        });
    }

    return false;
}

function handleEditSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.seq = $("#pop_seq").val();
        postData.Regular_Exp_Name = $("#pop_Regular_Exp_Name").val();
        postData.Regular_Exp = $("#pop_Regular_Exp").val();
//        postData.IP_Address = $("#pop_pattern").val();
//        postData.Password = $("#pop_IPS_password").val();
        postData.Description = $("#pop_etc").val();
//        postData.desc = $('#pop_desc_drop').val();


        var request = $.ajax({
            url:"/ELK/Regular_Expression_Management/"+ postData.seq,
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

    return false;
}

function showEditDialog(id){
    if($('input[name=editFeature]input:checked').length == 0){
        alert('수정할 아이템을 선택하세요!');
        return
    }

    var rownum = $('input[name=editFeature]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];



     $('#pop_seq').val(row.seq);
     $('#pop_Regular_Exp_Name').val(row.Regular_Exp_Name);
     $('#pop_Regular_Exp').val(row.Regular_Exp);
//     $('#pop_pattern').val(row.IP_Address);
//     $("#pop_IPS_password").val(row.Password)
     $("#pop_etc").val(row.Description)
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
            url: "/ELK/Regular_Expression_Management/" + row.seq,
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

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
       var dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/ELK/Regular_Expression_Management/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();
                        d.search_keyword_type = $("#search_keyword_type").val();
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
                    data : "Regular_Exp_Name",
                    label: "정규표현식 이름"
                }
                ,
                {
                    data : "Regular_Exp",
                    label: "정규표현식"
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
                    data : "Description",
                    label: "비고"
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
                    className: 'select-checkbox',
                   "render" :function (data, type, row, meta){
                        var btnHtml = '';
                        btnHtml = '<input type="checkbox" id="horns" name="editFeature" value="'+meta.row+'"/>';
                        return btnHtml;
                    }
                }
                ,
                {
                    "targets": 1,
                    orderable: false,
                    searchable: false

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

