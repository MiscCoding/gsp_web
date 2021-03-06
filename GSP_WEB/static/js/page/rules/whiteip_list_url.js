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
            url:"/rules/ip-url-white-list/whitelistPeriodSet",
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

function pageMoveFeature(){
    $body.addClass("loading");
    var pageIndexValue = $('#page_move_no_input').val();
    var table = $('#demo-foo-filtering').DataTable();
    var currentPageindex = table.page.info().page;
    var totalPages = table.page.info().pages;

    if(pageIndexValue <= 1)
    {
        pageIndexValue = 1
    }
    if(pageIndexValue >= (totalPages))
    {
        pageIndexValue = (totalPages);
    }

    $('#page_move_no_input').val("");

    table.page(pageIndexValue-1).draw( 'page' );
//    $body.removeClass("loading");

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
        search_keyword_type : $("#search_keyword_type").val(),
        columnIndex : window.localStorage.getItem('columnIndex'),
        sort_style : window.localStorage.getItem('sorting_style')

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
    form.setAttribute('action', "/rules/ip-url-white-list/excel-list")
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
    form.setAttribute('action', "/rules/ip-url-white-list/sample-excel-list")
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
            url:"/rules/ip-url-white-list/uploadlist",
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

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.type = $("#pop_type").val();
        postData.pattern = $("#pop_pattern").val();
        postData.mask = $("#pop_mask").val();
        postData.url = $("#pop_url").val();
        postData.desc = $('#pop_desc_drop').val();


        var request = $.ajax({
            url:"/rules/ip-url-white-list",
            type:"POST",
            data:postData,
            success: function(data, status){
                $('#demo-foo-filtering').DataTable().ajax.reload();
                $('#modal-popup').modal('toggle');
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
        postData.type = $("#pop_type").val();
        postData.pattern = $("#pop_pattern").val();
        postData.mask = $("#pop_mask").val();
        postData.url = $("#pop_url").val();
        postData.desc = $('#pop_desc_drop').val();


        var request = $.ajax({
            url:"/rules/ip-url-white-list/"+ postData.seq,
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

    if($('input[name=editFeature]input:checked').length > 1){
        alert('More than two item were selected!');
        return
    }

    var rownum = $('input[name=editFeature]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    $('#pop_seq').val(row.seq);
    $("#pop_type").val(row.type);
    $('#pop_pattern').val(row.ip);
    $("#pop_mask").val(row.mask);
    $('#pop_desc').val(row.description);
    $('#pop_desc_drop').val(row.description);
    $('#pop_url').val(row.url);
    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();
}

function deleteItem(){

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');

    var rowNumList = [];
    var dataTableRowNumList = [];
    $body.addClass("loading");
    rowNumList = $('input[name=editFeature]input:checked')

    for (var i = 0; i < rowNumList.length; i++)
    {
        dataTableRowNumList.push($('#demo-foo-filtering').DataTable().data()[rowNumList[i].value].seq);
    }

//    var postData = new Object();
//    postData.dataTableRowNumList = dataTableRowNumList;
    //var rownum = $('input[name=editFeature]input:checked')[0].value

//    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    if( result) {

        var request = $.ajax({
            url: "/rules/ip-url-white-list-delete",

            type:"POST",
            data: JSON.stringify({ deleteItemList : dataTableRowNumList}),
            dataType:"json",
            contentType:"application/json;charset=UTF-8",
//            url: "/rules/ip-url-white-list/" + row.seq,
//            type: "DELETE",
            success: function (data, status) {
                //alert('success');

                $('#demo-foo-filtering').DataTable().ajax.reload();
                $body.removeClass("loading");
            },
            error: function (err, status) {
                $body.removeClass("loading");
                setTimeout(function (){
                    alert(err.responseText);
                }, 350);

            }
        });
    }

    return false;
}

function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/rules/ip-url-white-list/list",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.search_source = $("#search_source").val();
                        d.search_keyword = $("#search_keyword").val();
                        d.search_keyword_type = $("#search_keyword_type").val();
                        d.columnIndex = window.localStorage.getItem('columnIndex');
                        d.sort_style = window.localStorage.getItem('sorting_style');
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
              $body.removeClass("loading");
              $('#divTotal').text("총 "+json.recordsFiltered + "건");
            },
            error: function(xhr, error, thrown) {
                alert(error);
                error(xhr, error, thrown);
                $body.removeClass("loading");
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
            sort: true,
            ordering: true,
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
                    data : "ip",
                    label: "IP"
                },
                {
                    data : "mask",
                    label: "Mask"
                },
                {
                    data : "url",
                    label: "패턴(URL)",
                    mDataProp: '패턴(URL)',
                    mRender: function(value) {
                             if(value !== null)
                                return value.truncStr(30);
                             else
                                return "";
                             }
                },

                {
                    data : "description",
                    label: "유형"
                },
                {
                    data : "type",
                    label: "세부유형"
                },
                {
                    data : "cre_dt",
                    label: "등록일",
                    mDataProp: 'cre_dt',
                    mRender: function(value) {
                             return formatDate(value);
                             }
                },
                {
                    data : "mod_dt",
                    label: "수정일"
                }
                
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
                    },
                    searchable: false, "visible": true
                }

            ],
            "drawCallback" : function(setting,data){
//                    $("input:checkbox").on('click', function() {
//                    // in the handler, 'this' refers to the box clicked on
//                    var $box = $(this);
//                    if ($box.is(":checked")) {
//                        // the name of the box is retrieved using the .attr() method
//                        // as it is assumed and expected to be immutable
//                        var group = "input:checkbox[name='" + $box.attr("name") + "']";
//                        // the checked state of the group/box on the other hand will change
//                        // and the current value is retrieved using .prop() method
//                        $(group).prop("checked", false);
//                        $box.prop("checked", true);
//                    } else {
//                        $box.prop("checked", false);
//                    }
//                });
                $body.removeClass("loading");


                var theTableName = "whitelistpage2";
                 setTimeout(function(){
                        if((sessionStorage.getItem(theTableName) !== null))
                        {
                            if (sessionStorage.getItem(theTableName).length >= 1)
                            {
                                        var theTableWidth = parseInt(window.sessionStorage.getItem(theTableName));

                                        $(".dataTables_scrollHeadInner").width(theTableWidth);
                                        $(".table .table-striped .table-bordered .toggle-circle .m-b-0 .dataTable .no-footer").width(theTableWidth);

                                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();

                            }
                        }
                         $("#chkBoxes").removeClass("sorting_asc");
                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                 }, 350);

                if(sessionStorage.getItem(theTableName) === null)
                {
                    sessionStorage.setItem(theTableName, $(".dataTables_scrollHeadInner").width());
                }






                setTimeout(function(){
                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                        $("#chkBoxes").removeClass("sorting_asc");
                }, 350);

                var table = $('#demo-foo-filtering').DataTable();
                var currentPageindex = table.page.info().page;
                var totalPages = table.page.info().pages;

//
                $('#demo-foo-filtering_next').on( 'click', function () {
                       $body.addClass("loading");
                       var nextPageIndex = currentPageindex + 1;
                       if(nextPageIndex >= totalPages){
                          nextPageIndex = totalPages - 1;
                       }
                       table.page(nextPageIndex).draw( 'page' );
                });

                 $('#demo-foo-filtering_previous').on( 'click', function () {
                        $body.addClass("loading");
                        var previousPageIndex = currentPageindex - 1;
                        if (previousPageIndex < 0){
                            previousPageIndex = 0;
                        }
                        table.page(previousPageIndex).draw( 'page' );
                 });

                 $(".paginate_button").on('click', function(){
                    $body.addClass("loading");
                 });
            }
        }).on('error.dt', function(e, settings, technote, message){
            $body.removeClass("loading");
            alert("MySQL connection timeout error, or  Cannot retrieve data from MySQL ");
        });
    }
}

//var table = $('#demo-foo-filtering').DataTable();
//var currentPageindex = table.page.info();
//
//$('#demo-foo-filtering_next').on( 'click', function () {
//                       table.page( currentPageindex + 1 ).draw( 'page' );
//});
//
//$('#demo-foo-filtering_previous').on( 'click', function () {
//                        table.page(currentPageindex - 1).draw( 'page' );
//});

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
    $body.addClass("loading");
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

$(".categorySort").click(function(event){
    console.log(event.target.id + " has been clicked.");
    console.log(event.target.className + "  is the className");
    sorting = (event.target.className).split(" ")[1];
    if(sorting == "sorting" || sorting == "sorting_desc") {
        window.localStorage.setItem('sorting_style', "desc")
    } else {
        window.localStorage.setItem('sorting_style', "asc")
    }
    $body.addClass("loading");
    window.localStorage.setItem('columnIndex', event.target.id);

    DatatableReload();

});

var whetherChecked = false;

$("#topbox").click(function(e){
    console.log("All check button has been clicked");
    console.log("Checked? : " + whetherChecked);
    if ($('#topbox').checked === false ){
        whetherChecked = false;
    }


    if(this.checked === true)
    {
        for (var i = 0; i < $('td input[type="checkbox"]').length; i++)
        {
                $('td input[type="checkbox"]')[i].checked = true;
        }
        whetherChecked = true;
    }
    else
    {
        for (var i = 0; i < $('td input[type="checkbox"]').length; i++)
        {
                $('td input[type="checkbox"]')[i].checked = false;
        }
        whetherChecked = false;

    }
});

