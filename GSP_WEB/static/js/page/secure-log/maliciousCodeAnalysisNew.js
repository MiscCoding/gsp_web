function isFileValidate(){
    if ($("#pop_file").val() == '' )
        return false;
    else
        return true;
}

function handleMaxWindowValue (){

        $body.addClass("loading");
        var _form  = $('#max_window_value')
        _form.parsley().validate();
        if (_form.parsley().validationResult === true)
        {
            console.log("Input validation confirmed");
        } else {
            alert("Only number is allowed for the max window setting");
            $body.removeClass("loading");
            return;
        }


        var postData = new Object();
        postData.max_window_value = $('#max_window_value').val();

        var request = $.ajax({
            url:"/secure-log/maliciousCodeAnalysis/max_window_value_set",
            type:"PUT",
            data:postData,
            success: function(data, status){
                alert("Max window value has been set.");
                location.reload();
                $body.removeClass("loading");
            },
            error: function(err, status, err2){
                $body.removeClass("loading");

                 alert(err.responseJSON.message);

            }
        });
}

function fileSubmit(){
        if( !isFileValidate())
        {
            alert("업로드할 파일을 선택 해 주세요");
            return false;
        }
        $body.addClass("loading");
        var formData = new FormData($("#formUpload")[0]);

        formData.append("file", $("#pop_file")[0].files[0]);

        var request = $.ajax({
            url:"/secure-log/maliciousCodeAnalysis/malfileUpload",
            type:"POST",
            data:formData,
            processData:false,
            contentType: false,
            success: function(data, status){
               // $('#demo-foo-filtering').DataTable().ajax.reload();
                //$('#modal-popup-file').modal('toggle');
                $('#pop_file_name').val("");
                $('.filebox .upload-hidden').val("");
                alert("Manual file analysis request has been made successfully!");
                DatatableReload();
                $body.removeClass("loading");

            },
            error: function(err, status, err2){
                 //$('#demo-foo-filtering').DataTable().ajax.reload();
                 $('#pop_file_name').val("");
                 $('.filebox .upload-hidden').val("");
                 DatatableReload();
                 $body.removeClass("loading");
                // $('#modal-popup-file').modal('toggle');
                 alert(err.responseJSON.message);
            }
        });


}

function downloadExcel(){
    $body.addClass("loading");
    data = {
        curpage : dtTable.page.info().page,
        start : dtTable.page.info().start,
        max_window_value : $("#max_window_value").val(),
        perpage : $("#perpage").val(),
        //search_type : $("#search_type").val(),
        //search_source : $("#search_source").val(),
        search_security_level_url : $("#search_security_level_url").val(),
        search_security_level_file : $("#search_security_level_file").val(),
        search_keyword_type : $("#search_keyword_type").val(),
        wild_card : checkAsterisk($("#search_keyword").val()),
        search_keyword : $("#search_keyword").val(),
        timeFrom : $("#dateFrom").val(),
        timeTo : $("#dateTo").val(),
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
    form.setAttribute('action', "/secure-log/maliciousCodeAnalysis/excel-list")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
    $body.removeClass("loading");

}

function handleAddSubmit (){
    var _form  = $('#popup-form')
    _form.parsley().validate();

    if( _form.parsley().validationResult) {

        var postData = new Object();
        postData.rule_name = $("#pop_category").val();
        postData.mal_file_name = $("#pop_fname").val();
        postData.pattern = $("#pop_pattern").val();
        postData.uri = $("#pop_url").val();
        postData.analysis_device=$("#pop_description").val();
        postData.detection_source = $("#pop_detection_source").val();
        //postData.size = $("#pop_size").val();
        postData.source = $("#pop_source").val();
        postData.desc = $('#pop_desc').val();

        var request = $.ajax({
            url:"/secure-log/black-list",
            type:"POST",
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

function handleEditSubmit (){

        $body.addClass("loading");
        var postData = new Object();
        postData._index = $("#pop_index").val();
        //postData.mal_file_name =
        postData._id = $("#pop_id").val();
        postData.comment = $("#pop_etc").val();


        var request = $.ajax({
            url:"/secure-log/maliciousCodeAnalysis/updateComment",
            type:"POST",
            data:postData,
            success: function(data, status){


                 $('#modal-popup').modal('toggle');
                location.reload();



            },
            error: function(err, status, err2){


                 location.reload();

                 alert(err.responseJSON.message);
            }
        });


    return false;
}

function reanalysisRequest(_index, _id){

        $body.addClass("loading");
        var postData = new Object();
        postData._index = _index;
        postData._id = _id;

        var request = $.ajax({
            url:"/secure-log/maliciousCodeAnalysis/reanalysisRequest",
            type:"POST",
            data:postData,
            success: function(data, status){
                $body.removeClass("loading");
                alert("Re-analysis request has been sent!");
                DatatableReload();
            },
            error: function(err, status, err2){

                $body.removeClass("loading");
                 alert(err.responseJSON.message);
                 DatatableReload();
            }
        });


    return false;
}

function urlmanualanalysisRequest(){

        $body.addClass("loading");
        var postData = new Object();
        postData._manualurlRequest = $('#manualURLRequest').val();
        //postData._id = _id;

        var request = $.ajax({
            url:"/secure-log/maliciousCodeAnalysis/manualurlanalysisrequest",
            type:"POST",
            data:postData,
            success: function(data, status){
                $body.removeClass("loading");
                alert("Manual URL analysis request has been sent successfully!");
                DatatableReload();
            },
            error: function(err, status, err2){
                DatatableReload();
                $body.removeClass("loading");
                 alert(err.responseJSON.message);
            }
        });


    return false;
}


function showEditDialog(){
    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('수정 할 아이템을 선택 해 주세요');
        return;
    }

    if( $('input[name=dtSelector]input:checked').length > 1){
        alert('Multiple items selected');
        return;
    }


    var rownum = $('input[name=dtSelector]input:checked')[0].value

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    $('#pop_index').val(row._index);
    $('#pop_id').val(row._id);
    $('#pop_etc').val(row._source.comment);

    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').show();
    $('#modal-popup').modal();
}

function showURLDetailDialog(rowNumMeta){

    //var rownum = $('input[name=dtSelector]input:checked')[0].value
    var rownum = rowNumMeta;

    row = $('#demo-foo-filtering').DataTable().data()[rownum];
    var fullUrl = row._source.url;
    var forpartUrl = row._url_fore_part;
    var otherhalf = fullUrl.replace(forpartUrl, "");
    $('#pop_up_full_url').val(row._source.url);
    $('#pop_detail_url').val(row._url_fore_part);
    $('#pop_up_subpath').val(otherhalf);

    $('#btnAddSubmit').hide();
    $('#btnEditSubmit').hide();
    $('#modal-popup-detailed-row-information').modal();
}




function showURIDialog(_id, detailType, index){
//    if( $('input[name=dtSelector]input:checked').length == 0){
//        alert('수정 할 아이템을 선택 해 주세요');
//        return;
//    }
    $body.addClass("loading");

    var postData = new Object();
    postData._id = _id;
    postData.detailType = detailType;
    postData.index = index;

    if(detailType == "file") {
        $("#namebar").text("파일 상세 분석결과");
    } else {
        $("#namebar").text("URI 상세 분석결과");
    }

    var request = $.ajax({
            url:"/secure-log/maliciousCodeAnalysis/getDetailedResult",
            type:"POST",
            data:postData,
            success: function(data, status){
                //$('#demo-foo-filtering').DataTable().ajax.reload();
                for(var i = 0; i<data.data.length; i++){
                    if(typeof data.data[i].imas !== 'undefined'){
                        var jsonObj = JSON.stringify((data.data[i].imas), null, '\t');
                        var date = formatDate(data.data[i].imas['@timestamp']);
                        var exception = data.data[i].imas['result']
                        if(exception === "malware"){
                            $('#imasDetectionResult').text("악성");
                        } else {
                            $('#imasDetectionResult').text("");
                        }
                        if(data.data[i].imas.detail !== ""){
                            $('#imas').val(jsonObj);
                        } else {
                            $('#imas').val(jsonObj);
                        }
                        $('#imasdate').text(date);
                    } else if(typeof data.data[i].zombie !== 'undefined'){
                        var jsonObj = JSON.stringify((data.data[i].zombie), null, '\t');
                        var date = formatDate(data.data[i].zombie['@timestamp']);
                        var exception = data.data[i].zombie['result']
                        if(exception === "malware"){
                            $('#zombieDetectionResult').text('악성');
                        } else {
                            $('#zombieDetectionResult').text('');
                        }

                        if(data.data[i].zombie.detail !== ""){
                            $('#zombie').val(jsonObj);
                        } else {
                            $('#zombie').val(jsonObj);
                        }
                        $('#zombiedate').text(date);
                    }
                }
                $body.removeClass("loading");

                $('#modal-popup-detailed-analysis').modal();
            },
            error: function(err, status, err2){
                 $body.removeClass("loading");
                  $('#imas').val("");
                  $('#zombie').val("");
                 alert(err.responseJSON);
            }
        });
}


function deleteItem(){

    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('삭제 할 아이템을 선택 해 주세요');
        return;
    }

    if( $('input[name=dtSelector]input:checked').length > 1){
        alert('Multiple items selected');
        return;
    }

    var rownum = $('input[name=dtSelector]input:checked')[0].value
    row = $('#demo-foo-filtering').DataTable().data()[rownum];

    var postData = new Object();
    postData._index = row._index;
    postData._id = row._id;

    var result = confirm('해당 아이템을 삭제 하시겠습니까?');
    $body.addClass("loading");

    if(result) {

        var request = $.ajax({
            url: "/secure-log/maliciousCodeAnalysis/deleteSigleElement",
            type: "POST",
            data:postData,
            success: function (data, status) {

                $body.removeClass("loading");
                DatatableReload();
            },
            error: function (err, status) {
                $body.removeClass("loading");
                DatatableReload();
                alert(err.responseText);
            }
        });
    }

    return false;
}

function downloadMalCode(){

    if( $('input[name=dtSelector]input:checked').length == 0){
        alert('삭제 할 아이템을 선택 해 주세요');
        return;
    }

    var rowNumList = [];
    var dataTableRowNumList = [];
    $body.addClass("loading");
    rowNumList = $('input[name=dtSelector]input:checked')

    for (var i = 0; i < rowNumList.length; i++)
    {
        dataTableRowNumList.push($('#demo-foo-filtering').DataTable().data()[rowNumList[i].value]._source.file_path);
    }

//    var rownum = $('input[name=dtSelector]input:checked')[0].value
//    row = $('#demo-foo-filtering').DataTable().data()[rownum];


    $body.addClass("loading");

    data = {
//        _filepath : row._source.file_path
          _filepath : dataTableRowNumList
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
    form.setAttribute('action', "/secure-log/maliciousCodeAnalysis/download")
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
    $body.removeClass("loading");

}

function checkAsterisk(strVar) {
    for (var i=0; i<strVar.length; i++) {
        if(strVar[i] === "*"){
            return "true";
        }
    }
    return "false";
}

//function fractionalNumberChecker(FractionalNumKeyword){
//        var eachNumberList = FractionalNumKeyword.split("/");
//        if (parseInt(eachNumberList[1]) <= 0 || parseInt(eachNumberList[1]).isNaN ==  || parseInt(eachNumberList[1]) == null){
//            return alert("Denominator is zero or negative error.");
//        }
//        return "true";
//}


function GetList(){
    if ($('#demo-foo-filtering').length !== 0) {
        dtTable = $('#demo-foo-filtering').DataTable({
                ajax: {
                    url:"/secure-log/maliciousCodeAnalysis/getlist",
                    type:"POST",
                    "data": function (d) {
                        d.perpage = $("#perpage").val();
                        d.max_window_value = $("#max_window_value").val();
                        //d.search_source = $("#search_source").val();
                        //d.search_keyword = $("#search_keyword").val();
                        d.search_security_level_file = $("#search_security_level_file").val();
                        d.search_security_level_url = $("#search_security_level_url").val();
//                        if($("#search_keyword_type").val() == "uri_analysis_result" || $("#search_keyword_type").val() == "file_analysis_result" ){
//                            result = fractionalNumberChecker($("#search_keyword").val());
//                        }
                        d.search_keyword_type = $("#search_keyword_type").val();
                        d.search_keyword = $("#search_keyword").val();
                        d.wild_card = checkAsterisk(d.search_keyword);
                        d.timeFrom = $("#dateFrom").val();
                        d.timeTo = $("#dateTo").val();
                        localStorage.setItem('max_window_value', $("#max_window_value").val());
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
              $('#divTotal').text("총 "+json.recordsFiltered.toLocaleString() + "건");



            },
            error: function(xhr, error, thrown) {
                $body.removeClass("loading");
                setTimeout(function(){
                    alert("Elasticsearch data retrieval failed. Details are " + error);

                }, 1500);
//                alert(error);
                //error(xhr, error, thrown);
            },
            dom: 'Bfrtip',
            "pagingType": "full_numbers",
            fixedHeader: true,
            "scrollY" : "700px",
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
                        data : "_source.@timestamp",
                        label: "분석일",
                        mDataProp: '분석일',
                        mRender: function(value) {
                                  return formatDate(value);
                                  }
                    },
                    {
                        data : "_source.url",
                        label: "URI"

                    },
                    {
                        data : "_source.dst_ip",
                        label: "IP"
                    },
                    {
                        data : "_source.dst_country_code1",
                        label: "국가코드"
                    },
                    {
                        data : null,
                        label: "파일명[해시값]"

                    },
                    {
                        data : "_source.data_type",
                        label: "탐지점"
                    }
                    ,
                    {
                        data : "_source.malware_comment",
                        label: "탐지명"
                    }
                    ,
                    {
                        data : "_source.detect_cnt_url",
                        label: "URI분석"
                    }
                    ,
                    {
                        data : "_source.detect_cnt_file",
                        label: "파일분석"
                    }
                    ,
                    {
                        data : "_source.comment",
                        label: "비고",
                        mDataProp: '비고',
                        mRender: function(value) {
                                 if (value === 'undefined'){
                                    return "";
                                 } else {
                                    return value.truncStr(15);
                                 }

                        }
                    },
                    {
                        data : null
                    },
                    {
                        data : null
                    }
            ],
            columnDefs : [
                {
                    targets : 0,
                    orderable: false,
                    render : function (data, type, row, meta) {

                        var btnHtml = "<input id='"+ row._id +"' type='checkbox' name='dtSelector' value='"+ meta.row + "'/>";

                        return btnHtml;
                    },
                    searchable: false, "visible": true
                },
                {
                    targets : 2,
                    orderable: false,
                    render : function (data, type, row, meta) {
                        var uri = row._source.url;
                        var btnHtml = '<div class="syst-sm-bg" data-toggle="tooltip" title="'+ uri +'" onclick="showURLDetailDialog(\''+ meta.row+'\')">' + uri.truncStr(30) + '</div>';
                        return btnHtml;
                    },
                    searchable: false, "visible": true
                },
                {
                    targets : 3,
                    orderable: false,

                    searchable: false, "visible": true
                },
                {
                    targets : 4,
                    orderable: false,

                    searchable: false, "visible": true
                },
                {
                    targets : 5,
                    orderable: false,
                    render : function (data, type, row, meta) {
                        var file_name = row._source.file_name;
                        var md5 = row._source.md5;
                        //var btnHtml = '<a href="/secure_log/maliciousCodeAnalysis/download?filepath=\''+ row._source.file_path +'\'" data-method="GET" download>'+ file_name.truncStr(30) +"</a><p>"+ md5.truncStr(40) +"</p>";
                        var btnHtml = '<p>'+ file_name.truncStr(30) +"<br>"+ md5.truncStr(40) +"</p>";
                        return btnHtml;
                    },
                    searchable: false, "visible": true
                },
                {
                    targets : 6,
                    orderable: false,

                    searchable: false, "visible": true
                },
                {
                    targets : 7,
                    orderable: false,

                    searchable: false, "visible": true
                },
                {
                    targets : 8,
                    render : function (data, type, row, meta) {
                        var index = row._index;
                        var urldetectEngine = row._source.detect_engine_url;
                        var malwareornot = "";
                        if(row._source.detect_cnt_url > 0){
                            malwareornot = "악성";
                        } else {
                            malwareornot = "정상";
                        }

                        var urlRatio = row._source.detect_cnt_url+ " / " +row._source.total_cnt_url;

                        var statusIndication = "<p>" + malwareornot +"<br>"+ urlRatio +"<p>";

                        var analysisResult = row._source.status_url;
                        if (row._source.status_url === 'analyzing'){
                            statusIndication = "분석중";
                        }

                        var btnHtml = '<div class="syst-sm-bg" data-toggle="tooltip" title="'+ urldetectEngine +'" onclick="showURIDialog(\''+row._id+'\'' + ', \'url\''+', \''+index+'\')">'+ statusIndication +'</div>';

                        return btnHtml;
                    }
                },
                {
                    targets : 9,
                    render : function (data, type, row, meta) {
                        var index = row._index;
                        var filedetectEngine = row._source.detect_engine_file;
                        var malwareornot = "";
                        if(row._source.detect_cnt_file > 0){
                            malwareornot = "악성";
                        } else {
                            malwareornot = "정상";
                        }

                        var urlRatio = row._source.detect_cnt_file+ " / " +row._source.total_cnt_file;

                        var statusIndication = "<p>" + malwareornot +"<br>"+ urlRatio +"<p>";

                        var analysisResult = row._source.status_file;
                        if (row._source.status_file === 'analyzing'){
                            statusIndication = "분석중";
                        }

                        var btnHtml = '<div class="syst-sm-bg" data-toggle="tooltip" title="'+ filedetectEngine +'" onclick="showURIDialog(\''+row._id+'\'' + ', \'file\''+', \''+ index +'\')">'+ statusIndication +'</div>'

                        return btnHtml;
                    }
                },
                {
                    targets : 10,
                    orderable: false,

                    searchable: false, "visible": true
                },
                {
                    targets : 11,
                    orderable: false,
                    render : function (data, type, row, meta) {
                        var uri = row._source.url;
                        var uriAnalysis = row._source.status_url;
                        var fileAnalysis = row._source.status_file;
                        var btnHtml = "";
                        if (uriAnalysis === "finish" && fileAnalysis === "finish"){
                            btnHtml = '<div class="syst-sm-bg-black" onclick="reanalysisRequest(\''+ row._index+'\', \''+ row._id +'\')" style="width:80px !important; font-align:center !important; margin-left:18%; height:30px!important; padding-top:10px;">요청</div>';
                        }
                        return btnHtml;
                    },
                    searchable: false, "visible": true
                },
                {
                    targets : 12,
                    orderable: false,
                    render : function (data, type, row, meta) {
                        var reanalysis = row._source.is_reanalysis;

                        var btnHtml = "";
                        if (reanalysis === "Y"){
                            btnHtml = 'Y';
                        } else {
                            btnHtml = 'N';
                        }

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
                localStorage.setItem('max_window_value', $("#max_window_value").val());
                $.fn.dataTable.ext.errMode = 'throw';
                 setTimeout(function(){
                        $("#chkBoxes").removeClass("sorting_asc");
                        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
                 }, 350);
                 $body.removeClass("loading");
            }
        }).on('draw.dt', function(){
            //dtTable.rowsgroup.update();
            $('[data-toggle="tooltip"]').tooltip({html: true});
        }).on('error.dt', function(e, settings, technote, message){
            $body.removeClass("loading");
            var startIdx = dtTable.page.info().start;
            var max_window_value = localStorage.getItem('max_window_value');
            if(startIdx > max_window_value)
            {
                alert("Elasticsearch max window setting value is small! Max value is " + max_window_value);
                return;
            }
            alert("Elasticsearch connection timeout error, or  Cannot retrieve data from Elasticsearch "+ e + " " + settings + technote+message);
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

function DatatableReload(){
//if ($('#search_keyword').val() == ""){
//        return alert("검색키워드 입력 하세요!")
//    }
    $body.addClass("loading");
    $('#demo-foo-filtering').DataTable().ajax.reload(function(data){
        $body.removeClass("loading");
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