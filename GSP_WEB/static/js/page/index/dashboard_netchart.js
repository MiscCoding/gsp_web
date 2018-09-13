function reloadData() {
    //$('#divSearch').loading();
    //force.data(nodes);
    //$("#detailSearch").collapse();
}
var tooltip = d3.select("body")
    .append("div")
    .attr("class","tooltip")
    .style("opacity", 0);

var nodetooltip = d3.select("body")
    .append("div")
    .attr("class","tooltip")
    .style("opacity", 0);

var width = 1920,
    height = 520

var nominal_base_node_size = 8;
var nominal_text_size = 10;
var max_text_size = 24;
var nominal_stroke = 1.5;
var max_stroke = 4.5;
var max_base_node_size = 36;
var min_zoom = 0.1;
var max_zoom = 7;
var link, node, text,circle;
var text_center = false;
var outline = false;

var highlight_color = "#ccc";
var highlight_trans = 0.1;
var default_link_color = "#ccc";

var focus_node = null,
    highlight_node = null;

var svg = d3.select("#linkedChart").append("svg")
    .attr("width", "100%")
    .attr("height", height)
    .attr("margin-top", 50);

var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])
var g = svg.append("g");

var size = d3.scale.pow().exponent(1)
    .domain([1,100])
    .range([8,24]);

var force = d3.layout.force()
    .gravity(0.05)
    .distance(120)
    .charge(-375)
    .size([width, height]);

var tocolor = "fill";
var towhite = "stroke";
if (outline) {
    tocolor = "stroke"
    towhite = "fill"
}

var linkedByIndex = {};
var nodes, links, maxdata;

function reloadData() {
    // var _form  = $('#formSearch')
    // _form.parsley().validate();
    // if( !_form.parsley().validationResult)
    //     return;

    // $('#divSearch').loading();
    // $("#detailSearch").collapse('hide');

    d3.select("g").selectAll("*").remove();
    var datasource = $('#datasource').val();
    var search_ip = $('#search_ip').val();
    var max_nodes_size = $('#max_nods').val();

    link = g.selectAll(".link");
    node = g.selectAll('.node');

    url = '/chart/rowdatalist/' + datasource + '?search_ip=' + search_ip + '&max_nodes_size=' + 500
    var pass_data =
        +"&timeFrom="// + $("#dateFrom").val()
        +"&timeTo="// + $("#dateTo").val()
        +"&timeSpan=" + $("#timeSetting").val()
        +"&search_ip="
        +"&search_ip_opt="
        +"&search_sendbyte_opt="// + $("#search_sendbyte_opt").val()
        +"&search_sendbyte_value="// + $("#search_sendbyte_value").val()
        +"&search_receivebyte_opt="// + $("#search_receivebyte_opt").val()
        +"&search_receivebyte_value="// + $("#search_receivebyte_value").val()
        +"&search_sendpacket_opt="// + $("#search_sendpacket_opt").val()
        +"&search_sendpacket_value="// + $("#search_sendpacket_value").val()
        +"&search_receive_packet_opt="// + $("#search_receive_packet_opt").val()
        +"&search_receive_packet_value="// + $("#search_receive_packet_value").val()
        +"&search_session_time_opt="// + $("#search_session_time_opt").val()
        +"&search_session_time_value="// + $("#search_session_time_value").val()
        +"&search_session_count_opt="// + $("#search_session_count_opt").val()
        +"&search_session_count_value="// + $("#search_session_count_value").val()
        +"&search_flag_urg_opt="// + $("#search_flag_urg_opt").val()
        +"&search_flag_urg_value="// + $("#search_flag_urg_value").val()
        +"&search_flag_ack_opt="// + $("#search_flag_ack_opt").val()
        +"&search_flag_ack_value="// + $("#search_flag_ack_value").val()
        +"&search_flag_psh_opt="// + $("#search_flag_psh_opt").val()
        +"&search_flag_psh_value="// + $("#search_flag_psh_value").val()
        +"&search_flag_rst_opt="// + $("#search_flag_rst_opt").val()
        +"&search_flag_rst_value="// + $("#search_flag_rst_value").val()
        +"&search_flag_syn_opt="// + $("#search_flag_syn_opt").val()
        +"&search_flag_syn_value="// + $("#search_flag_syn_value").val()
        +"&search_flag_fin_opt="// + $("#search_flag_fin_opt").val()
        +"&search_flag_fin_value="// + $("#search_flag_fin_value").val()
        +"&search_svr_con_count_opt="// + $("#search_svr_con_count_opt").val()
        +"&search_svr_con_count_value="// + $("#search_svr_con_count_value").val()
        +"&search_cli_con_count_opt="// + $("#search_cli_con_count_opt").val()
        +"&search_cli_con_count_value="// + $("#search_cli_con_count_value").val()
        +"&search_geo_distance_opt="// + $("#search_geo_distance_opt").val()
        +"&search_geo_distance_value=";// + $("#search_geo_distance_value").val();


    d3.json(url, function (error, json) {
        //$('#divSearch').loading('stop');
        if (error) throw error;

        if (json.nodes.length == 0) {
            alert('조회된 데이터가 없습니다.');
            return;
        }

        force
            .nodes(json.nodes)
            .links(json.links)
            .start();

        nodes = force.nodes();
        links = force.links();
        maxdata = json.maxdata;

        // add the links and the arrows
        var path = svg.append("svg:g").selectAll("path")
            .data(force.links())
            .enter().append("svg:path")
            //    .attr("class", function(d) { return "link " + d.type; })
            .attr("class", "link")
            .attr("marker-end", "url(#end)");

        link = g.selectAll(".link")
            .data(json.links)
            .enter().append("line")
            .attr("class", "link")
            .style("cursor", "pointer")
            .style("stroke-width", function(d){ return getLineWidth(d); })
            .attr("marker-end", "url(#end)");

        node = g.selectAll(".node")
            .data(json.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.on("dblclick.zoom", function (d) {
            d3.event.stopPropagation();
            var dcx = (window.innerWidth / 2 - d.x * zoom.scale());
            var dcy = (window.innerHeight / 2 - d.y * zoom.scale());
            zoom.translate([dcx, dcy]);
            g.attr("transform", "translate(" + dcx + "," + dcy + ")scale(" + zoom.scale() + ")");
        });

        circle = node.append("circle")
            .attr("r", function(d) {
                return d.value;
                //return d.value * 3;
            }).style("fill", function(d) { return d.color; });

        text = node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name
            });

        node.on("mouseover", function (d) {
            set_highlight(d);

            nodetooltip.transition()
                .duration(300)
                .style("opacity", .9);
            tooltipHtml = ("<p>Server IP : {0}</p><p>접속수 : {1}</p>")
                .format(d.name, d.conCount.toLocaleString());
            nodetooltip.html(tooltipHtml)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 10) + "px");
        }).on("mouseout", function (d) {
            svg.style("cursor", "move");
            nodetooltip.transition()
                .duration(100)
                .style("opacity", 0);
            exit_highlight();
        }).on("mousedown", function (d, i) {

            var isShift = !!window.event.shiftKey;
            if(isShift){

                nodes.splice(i, 1);
                links = links.filter(function(l) {
                    return l.source !== d && l.target !== d;
                });

                d3.event.stopPropagation();

                restart();
                return;
            }

            d3.event.stopPropagation();
            focus_node = d;
            set_focus(d);
            if (highlight_node === null) set_highlight(d);


        });

        d3.select(window).on("mouseup",
            function () {
                if (focus_node !== null) {
                    focus_node = null;
                    if (highlight_trans < 1) {

                        circle.style("opacity", 1);
                        text.style("opacity", 1);
                        link.style("opacity", 1);
                    }
                }

                if (highlight_node === null) exit_highlight();
            });


        force.on("tick", function () {
            link.attr("x1", function (d) {
                return d.source.x;
            })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        });

        zoom.on("zoom", function (target) {
            var stroke = nominal_stroke;
            if (nominal_stroke * zoom.scale() > max_stroke) stroke = max_stroke / zoom.scale();
            //link.style("stroke-width", stroke);
            circle.style("stroke-width", stroke);

            var base_radius = nominal_base_node_size;
            if (nominal_base_node_size * zoom.scale() > max_base_node_size) base_radius = max_base_node_size / zoom.scale();
            circle.attr("d", d3.svg.symbol()
                .size(function (d) {
                    //return Math.PI * Math.pow(size(d.value) * base_radius / nominal_base_node_size || base_radius, 2);
                    return d.value;
                })
                .type(function (d) {
                    return d.type;
                }))

            circle.attr("r", function (d) {
                //return (size(d.value) * base_radius / nominal_base_node_size || base_radius);
                return d.value;
            })
            if (!text_center) text.attr("dx", function (d) {
                //return (size(d.value) * base_radius / nominal_base_node_size || base_radius);
                return d.value
            });

            var text_size = nominal_text_size;
            //if (nominal_text_size * zoom.scale() > max_text_size) text_size = max_text_size / zoom.scale();
            //text.style("font-size", text_size + "px");

            //var g = svg[0][0].children[0];
            //g.setAttribute("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
            g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        });

        link.on("mouseover", function (d) {
            set_highlight(d);
            tooltip.transition()
                .duration(300)
                .style("opacity", .9);
            tcp_flag = "URG : {0}, ACK : {1}, PSH : {2}, RST : {3}, SYN : {4}, FIN : {5}".format(
                d.tcp_urg, d.tcp_ack, d.tcp_psh,d.tcp_rst, d.tcp_syn, d.tcp_fin);
            tooltipHtml = ("<p>Server IP:{0} Client IP:{1}</p><p>타임 스탬프:{2}</p><p>세션수:{3} 세션접속시간(초):{12}</p>"
                    +"<p>송신량:{4} 수신량:{5}</p><p>패킷량(송신):{6} 패킷량(수신):{7}</p><p>TCP Flag:[{8}]</p><p>지리적 거리:{9}km.</p>"
                    +"<p>Protocol:{10}</p><p>Server 접속수:{11} Client 접속수:{12}</p>")
                    .format(d.source.name, d.target.name,  d.timestamp, d.s_count.toLocaleString(), d.s_bytes.toLocaleString()
                    , d.r_bytes.toLocaleString(),d.s_pkts.toLocaleString(), d.r_pkts.toLocaleString(), tcp_flag, d.distance
                    , d.protocol, d.svrip_base_conn_cnt.toLocaleString(), d.clip_base_conn_cnt.toLocaleString(), d.s_time);
            tooltip.html(tooltipHtml)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 10) + "px");
        }).on("mouseout", function (d) {
            svg.style("cursor", "move");
            tooltip.transition()
                .duration(100)
                .style("opacity", 0);
        }).on("click", function (d) {
            var res = confirm('해당 IP(' + d.source.name + ')의 GEO 정보를 검색하시겠습니까?');
            datasource = $('#datasource').val();
            if (res)
                window.location = '/chart/geo-chart?datasource='+datasource+'&srcip=' + d.source.name + '&dstip=' + d.target.name + '&timestamp=' + d.timestamp
        });


        svg.call(zoom);

        resize();

        function resize() {
            //var width = window.innerWidth, height = window.innerHeight;
            svg.attr("width", width).attr("height", height);

            force.size([force.size()[0] + (width - width) / zoom.scale(), force.size()[1] + (height - height) / zoom.scale()]).resume();
            width = width;
            height = height;
        }

        link.forEach(function (d) {
            linkedByIndex[d.source + "," + d.target] = true;
        });

    })
        .header("Content-Type","application/x-www-form-urlencoded")
        .send("POST", pass_data);
}


function addTooltip(circle) {
    var x = parseFloat(circle.attr("cx"));
    var y = parseFloat(circle.attr("cy"));
    var r = parseFloat(circle.attr("r"));
    var text = circle.attr("id");

    var tooltip = d3.select("#plot")
        .append("text")
        .text(text)
        .attr("x", x)
        .attr("y", y)
        .attr("dy", -r * 2)
        .attr("id", "tooltip");

    var offset = tooltip.node().getBox().width / 2;

    if ((x - offset) < 0) {
        tooltip.attr("text-anchor", "start");
        tooltip.attr("dx", -r);
    }
    else if ((x + offset) > (width - margin)) {
        tooltip.attr("text-anchor", "end");
        tooltip.attr("dx", r);
    }
    else {
        tooltip.attr("text-anchor", "middle");
        tooltip.attr("dx", 0);
    }
}

function exit_highlight() {
    highlight_node = null;
    if (focus_node === null) {
        svg.style("cursor", "move");
        if (highlight_color != "white") {
            circle.style(towhite, "white");
            text.style("font-weight", "normal");
            link.style("stroke", function (o) {
                return (isNumber(o.score) && o.score >= 0) ? color(o.score) : default_link_color
            });
        }

    }
}

function set_focus(d) {
    if (highlight_trans < 1) {
        circle.style("opacity", function (o) {
            return isConnected(d, o) ? 1 : highlight_trans;
        });

        text.style("opacity", function (o) {
            return isConnected(d, o) ? 1 : highlight_trans;
        });

        link.style("opacity", function (o) {
            return o.source.index == d.index || o.target.index == d.index ? 1 : highlight_trans;
        });
    }
}

function set_highlight(d) {
    //hight 기능 off
    svg.style("cursor", "pointer");
    if (focus_node !== null) d = focus_node;
    highlight_node = d;

    if (highlight_color != "white") {
        circle.style(towhite, function (o) {
            return isConnected(d, o) ? highlight_color : "white";
        });
        text.style("font-weight", function (o) {
            return isConnected(d, o) ? "bold" : "normal";
        });
        link.style("stroke", function (o) {
            return o.source.index == d.index || o.target.index == d.index ? highlight_color : ((isNumber(o.score) && o.score >= 0) ? color(o.score) : default_link_color);
        });
    }

    if( d.target != null) {  //포커스가 link일때
        link.style("stroke", function (o) {
            return o.source.index == d.index || o.target.index == d.index ? highlight_color : ((isNumber(o.score) && o.score >= 0) ? color(o.score) : default_link_color);
        });
    }
}

function isConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
}

function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function restart() {
    node = node.data(nodes);

    node.exit()
        .remove();

    link = link.data(links);
    link.enter().insert("line", ".node")
        .style("stroke-width", function(d){ return getLineWidth(d); })
        .attr("class", "link");
    link.exit()
        .remove();

    force.start();
}

function deleteNode(){
    var _form  = $('#formSearch')
    _form.parsley().validate();
    if( !_form.parsley().validationResult)
        return;

    for( i = 0 ; i < link[0].length; i ++){
        _link = link[0][i];
    }

    // change the visibility of the connection path
    //결과내 재검색
    link.style("visibility", function(o) {
        var isVisibility = true;

        //IP
        var ip = $("#search_ip").val();
        var ip_opt = $("#search_ip_opt").val();
        if( ip != ''){
            isVisibility = (isVisibility &OperationValue(ip_opt, ip, o.source.name)) > 0;
            isVisibility = (isVisibility &OperationValue(ip_opt, ip, o.target.name)) > 0;
        }

        //송신량
        var sbytes = $('#search_sendbyte_value').val().trim();
        var sbytes_opt = $('#search_sendbyte_opt').val().trim();
        if( sbytes != ''){
            isVisibility = (isVisibility &OperationValue(sbytes_opt, sbytes, o.s_bytes)) > 0;
        }
        //수신량
        var rbytes = $('#search_receivebyte_value').val().trim();
        var rbytes_opt = $('#search_receivebyte_opt').val().trim();
        if( rbytes != ''){
            isVisibility = (isVisibility &OperationValue(rbytes_opt, rbytes, o.r_bytes)) > 0 ;
        }
        //송신 패킷수
        var spkts = $('#search_sendpacket_value').val().trim();
        var spkts_opt = $('#search_sendpacket_opt').val().trim();
        if( spkts != ''){
            isVisibility = (isVisibility &OperationValue(spkts_opt, spkts, o.s_pkts)) > 0 ;
        }
        //수신 패킷수
        var rpkts = $('#search_receive_packet_value').val().trim();
        var rpkts_opt = $('#search_receive_packet_opt').val().trim();
        if( rpkts != ''){
            isVisibility = (isVisibility &OperationValue(rpkts_opt, rpkts, o.r_pkts)) > 0 ;
        }
        //세션 유지시간
        var rpkts = $('#search_session_time_value').val().trim();
        var rpkts_opt = $('#search_session_time_opt').val().trim();
        if( rpkts != ''){
            isVisibility = (isVisibility &OperationValue(rpkts_opt, rpkts, o.s_time)) > 0 ;
        }
        //세션 수
        var session_cnt = $('#search_session_count_value').val().trim();
        var session_cnt_opt = $('#search_session_count_opt').val().trim();
        if( session_cnt != ''){
            isVisibility = (isVisibility &OperationValue(session_cnt_opt, session_cnt, o.s_count)) > 0 ;
        }
        //TCP Flag
        var tcp_urg = $('#search_flag_urg_value').val().trim();
        var tcp_urg_opt = $('#search_flag_urg_opt').val().trim();
        if( tcp_urg != ''){
            isVisibility = (isVisibility &OperationValue(tcp_urg_opt, tcp_urg, o.tcp_urg)) > 0 ;
        }
        //TCP Flag
        var tcp_ack = $('#search_flag_ack_value').val().trim();
        var tcp_ack_opt = $('#search_flag_ack_opt').val().trim();
        if( tcp_ack != ''){
            isVisibility = (isVisibility &OperationValue(tcp_ack_opt, tcp_ack, o.tcp_ack)) > 0 ;
        }
        //TCP Flag
        var tcp_psh = $('#search_flag_psh_value').val().trim();
        var tcp_psh_opt = $('#search_flag_psh_opt').val().trim();
        if( tcp_psh != ''){
            isVisibility = (isVisibility &OperationValue(tcp_psh_opt, tcp_psh, o.tcp_psh)) > 0 ;
        }
        //TCP Flag
        var tcp_rst = $('#search_flag_rst_value').val().trim();
        var tcp_rst_opt = $('#search_flag_rst_opt').val().trim();
        if( tcp_rst != ''){
            isVisibility = (isVisibility &OperationValue(tcp_rst_opt, tcp_rst, o.tcp_rst)) > 0 ;
        }
        //TCP Flag
        var tcp_syn = $('#search_flag_syn_value').val().trim();
        var tcp_syn_opt = $('#search_flag_syn_opt').val().trim();
        if( tcp_syn != ''){
            isVisibility = (isVisibility &OperationValue(tcp_syn_opt, tcp_syn, o.tcp_syn)) > 0 ;
        }
        //TCP Flag
        var tcp_fin = $('#search_flag_fin_value').val().trim();
        var tcp_fin_opt = $('#search_flag_fin_opt').val().trim();
        if( tcp_fin != ''){
            isVisibility = (isVisibility &OperationValue(tcp_fin_opt, tcp_fin, o.tcp_fin)) > 0 ;
        }
        //지리적 거리
        var distance = $('#search_geo_distance_value').val().trim();
        var distance_opt = $('#search_geo_distance_opt').val().trim();
        if( distance != ''){
            isVisibility = (isVisibility &OperationValue(distance_opt, distance, o.distance)) > 0 ;
        }
        //서버 기준 접속수 clip_base_conn_cnt
        var svr_con = $('#search_svr_con_count_value').val().trim();
        var svr_con_opt = $('#search_svr_con_count_opt').val().trim();
        if( svr_con != ''){
            isVisibility = (isVisibility &OperationValue(svr_con_opt, svr_con, o.svrip_base_conn_cnt)) > 0 ;
        }
        //서버 기준 접속수 clip_base_conn_cnt
        var cli_con = $('#search_cli_con_count_value').val().trim();
        var cli_con_opt = $('#search_cli_con_count_opt').val().trim();
        if( cli_con != ''){
            isVisibility = (isVisibility &OperationValue(cli_con_opt, cli_con, o.clip_base_conn_cnt)) > 0 ;
        }

        return isVisibility ? "visible" : "hidden";
    });

    // change the visibility of the node
    // if all the links with that node are invisibile, the node should also be invisible
    // otherwise if any link related to that node is visibile, the node should be visible
    node.style("visibility", function(o, i) {
        var lHideNode = true;
        link.each(function(d, i){
            if(d.source === o || d.target === o)
            {
                visibility = $(this).css("visibility");
                if( visibility === "visible")
                {
                    lHideNode = false;
                    // we need show the text for this circle
                    d3.select(d3.selectAll(".nodeText")[0][i]).style("visibility","visible");
                    return "visible";
                }
            }
        });
        if(lHideNode)
        {
            // we need hide the text for this circle
            d3.select(d3.selectAll(".nodeText")[0][i]).style("visibility","hidden");
            return "hidden";
        }
    });
}

function OperationValue(operate, targetValue, srcValue){
    if(operate == '>' )
        return srcValue > targetValue;
    else if(operate == '>=')
        return srcValue >= targetValue;
    else if(operate == '=')
        return srcValue == targetValue;
    else if(operate == '!=')
        return srcValue != targetValue;
    else if(operate == '<=')
        return srcValue <= targetValue;
    else if(operate == '<')
        return srcValue < targetValue;
    else if(operate == '<=')
        return srcValue <= targetValue;
}

function findItem(item, index, array){
    if( item.__data__["r_bytes"] >15000)
        return true;
}

String.prototype.format = function() {
    var str = this;
    for (var i = 0; i < arguments.length; i++) {
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        str = str.replace(reg, arguments[i]);
    }
    return str;
}

function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

jQuery(document).ready(function(){
    //reloadData();
});

$('#search_svr_con_count_v').click(function() {
    if ($(this).is(':checked')) {
        $('#search_ci_con_count_v').checked = true;
    } else {
        $('#search_ci_con_count_v').checked = false;
    }
});
$('#search_ci_con_count_v').click(function(){
    if($(this).is(':checked')){
        $('#search_cli_con_count_v').checked = true;
    } else {
        $('#search_cli_con_count_v').checked = false;
    }
});

function getLineWidth(d)
{
    opt = $("#lineOpt").val();
    if(opt == 'sendBytes'){
        return getPercentage(d.s_bytes, maxdata.send_bytes);
    }
    if(opt == 'rcvBytes'){
        return getPercentage(d.r_bytes, maxdata.recv_bytes);
    }
    if(opt == 'sendPkts'){
        return getPercentage(d.s_pkts, maxdata.send_pkts);
    }
    if(opt == 'rcvPkts'){
        return getPercentage(d.r_pkts, maxdata.recv_pkts);
    }
    if(opt == 'sessionCnt'){
        return getPercentage(d.s_count, maxdata.session_cnt);
    }
    if(opt == 'tcp_urg'){
        return getPercentage(d.tcp_urg, maxdata.tcp_flags_URG);
    }
    if(opt == 'tcp_ack'){
        return getPercentage(d.tcp_ack, maxdata.tcp_flags_ACK);
    }
    if(opt == 'tcp_psh'){
        return getPercentage(d.tcp_psh, maxdata.tcp_flags_PSH);
    }
    if(opt == 'tcp_rst'){
        return getPercentage(d.tcp_rst, maxdata.tcp_flags_RST);
    }
    if(opt == 'tcp_syn'){
        return getPercentage(d.tcp_syn, maxdata.tcp_flags_SYN);
    }
    if(opt == 'tcp_fin'){
        return getPercentage(d.tcp_fin, maxdata.tcp_flags_FIN);
    }
}

function getPercentage(curVal, maxVal){
    _minWidth = 1.0;
    _maxWidth = 8.0;
    percentage = curVal.toFixed(2) / maxVal.toFixed(2) ;
    size = percentage * _maxWidth;

    if (size < _minWidth)
        return _minWidth;
    else
        return size;
}

function onLineOptChanged(){
    reloadLines();
}

function reloadLines() {
    for(i=0; i < link[0].length; i++)
    {
        _link = link[0][i];
        _link.style['stroke-width'] = getLineWidth(_link.__data__);
        //_link.style("stroke-width", function(d){ return getLineWidth(d); })
    }

    force.start();
}