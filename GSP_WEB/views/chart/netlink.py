#-*- coding: utf-8 -*-
import random
from collections import OrderedDict

import datetime

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import render_template, Blueprint, json, request

from GSP_WEB.common.util import spark_helper
from GSP_WEB.common.util.date_util import Local2UTC
from GSP_WEB.models import Nations
from GSP_WEB.query.link_dna import GetLinkDnaListQueryEs
from GSP_WEB.query.netlink_chart import GetNetLinkChartQuery
from GSP_WEB import login_required, app

blueprint_page = Blueprint('bp_chart_netlink', __name__, url_prefix='/chart')
max_nodes_size = 1000

@blueprint_page.route('/net-link', methods=['GET'])
@login_required
def getNetLink():
    timefrom = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    timeto = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('chart/netlink.html', timefrom = timefrom, timeto=timeto)

@blueprint_page.route('/geo-chart', methods=['GET'])
def getGeoChart():
    return render_template('chart/geochart.html')

@blueprint_page.route('/net-link-dashboard/<string:datasource>', methods=['GET'])
@login_required
def getNetLinkDataDashboard(datasource):

    search_ip = request.args['search_ip']
    max_nodes_size = request.args['max_nodes_size']

    tempTable = 'tab1'
    sqlContext = spark_helper.getSqlContext('*', 'ca_sip_dip', tempTable)

    result1 = sqlContext.sql("select * from tab1")

    collectData = result1.limit(100).collect()


    chartdata = OrderedDict()
    nodes = list()
    links = list()

    uniquenodelist = []

    for doc in collectData:
        if doc['dst_ip'] == None\
                or doc['src_ip'] == None:
            continue
        uniquenodelist.append(doc['dst_ip'])
        uniquenodelist.append(doc['src_ip'])

    uniquenodelist = list(set(uniquenodelist))

    for doc in collectData:
        if doc['src_ip'] == None \
                or doc['dst_ip'] == None:
            continue
        timestamp = doc['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        tcpflag = "URG : {0}, ACK : {1}, PSH : {2}, RST : {3}, SYN : {4}, FIN : {5}"\
            .format(doc['tcp_flags_URG'] , doc['tcp_flags_ACK'] , doc['tcp_flags_PSH']
                    , doc['tcp_flags_RST'], doc['tcp_flags_SYN'], doc['tcp_flags_FIN'])
        distance = doc['geoip_distance']
        link = {
            "source": uniquenodelist.index(doc[7]), #src_ip
            "target": uniquenodelist.index(doc['src_ip']), #dst_ip
            "timestamp" : timestamp,
            "tcpflag" : tcpflag,
            "distance" : distance,
            "svrip_base_conn_cnt" : doc['svrip_base_conn_cnt'],
            "value": 1
        }
        links.append(link)

    for _node in uniquenodelist:
        node = {
            "name": _node,
            "group": 1
        }
        nodes.append(node)

    chartdata["nodes"] = nodes
    chartdata["links"] = links

    return json.dumps(chartdata)

@blueprint_page.route('/rowdatalist/<string:datasource>',methods=["POST"] )
def netflow_es(datasource ):
    recursiveSearchLvl = 3

    search_ip = request.args['search_ip']

    max_nodes_size = int(request.args['max_nodes_size'])
    tempTable = 'tab1'

    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    body = GetLinkDnaListQueryEs(request, max_nodes_size, 0)
    res = None

    if request.form.get('search_src_ip') == "" and request.form.get('search_dst_ip') == "":
        res = es.search(index="gsp-*" , doc_type="link_dna_tuple4", body=body, request_timeout=30)
    else :
        for i in range(0,recursiveSearchLvl):
            if res is not None and res['hits']['hits'].__len__() >= max_nodes_size:
                break
            res = NetLinkReSearch(es, res, max_nodes_size)

    chartdata = OrderedDict()
    nodes = list()
    links = list()

    uniquenodelist = []

    max_nodevalue = 1
    max_link  = dict()
    max_link.update({'bytes': 1, 'pkts': 1, 'session_cnt':1,
                    'tcp_flags_URG': 1, 'tcp_flags_ACK': 1 , 'tcp_flags_PSH': 1,'tcp_flags_RST': 1,
                    'tcp_flags_SYN': 1, 'tcp_flags_FIN': 1, 'tcp_flags_ACK': 1})

    for doc in res['hits']['hits']:
        row = doc['_source']
        if row['src_ip'] == None \
                or row['dst_ip'] == None:
            continue

        if row['data_type'] == 'netflows':
            #Link Value 최대값 저장 (선 굵기 비율 계산용)
            if max_link['bytes'] < float(row['bytes']): max_link['bytes'] = float(row['bytes'])
            if max_link['pkts'] < float(row['pkts']): max_link['pkts'] = float(row['pkts'])
            if max_link['tcp_flags_URG'] < float(row['tcp_flags_URG']): max_link['tcpflags_URG'] = float(row['tcpflags_URG'])
            if max_link['tcp_flags_ACK'] < float(row['tcp_flags_ACK']): max_link['tcp_flags_ACK'] = float(row['tcp_flags_ACK'])
            if max_link['tcp_flags_PSH'] < float(row['tcp_flags_PSH']): max_link['tcp_flags_PSH'] = float(row['tcp_flags_PSH'])
            if max_link['tcp_flags_RST'] < float(row['tcp_flags_RST']): max_link['tcp_flags_RST'] = float(row['tcp_flags_RST'])
            if max_link['tcp_flags_SYN'] < float(row['tcp_flags_SYN']): max_link['tcp_flags_SYN'] = float(row['tcp_flags_SYN'])
            if max_link['tcp_flags_FIN'] < float(row['tcp_flags_FIN']): max_link['tcp_flags_FIN'] = float(row['tcp_flags_FIN'])

        srcNodeName = str(row['src_ip'])
        isExists = next((index for (index, d) in enumerate(uniquenodelist) if d["name"] == srcNodeName), None)
        if isExists is None:
            node_src = dict()
            node_src['name'] = srcNodeName
            node_src['ip'] = row['src_ip']
            node_src['value'] = getValueAlter(row,'session_cnt',1) #원 크기
            node_src['color'] = "#FF7F27"
            node_src['type'] = 'Source'
            uniquenodelist.append(node_src)
            if max_nodevalue < int(getValueAlter(node_src,'value',1)): max_nodevalue = int(getValueAlter(node_src,'value',1))
        else:
            uniquenodelist[isExists]['value'] += getValueAlter(row,'session_cnt',1) #원 크기
            if max_nodevalue < float(uniquenodelist[isExists]['value']): max_nodevalue = float(uniquenodelist[isExists]['value'])

        dstNodeName = row['dst_ip']
        isExists = next((index for (index, d) in enumerate(uniquenodelist) if d["name"] == dstNodeName), None)
        if isExists is None:
            node_dst = dict()
            node_dst['name'] = dstNodeName
            node_dst['ip'] = row['dst_ip']
            node_dst['value'] = getValueAlter(row,'session_cnt',1) #원 크기
            node_dst['color'] = "blue"
            node_dst['type'] = 'destination'
            uniquenodelist.append(node_dst)
            if max_nodevalue < int(getValueAlter(node_dst,'value',1)): max_nodevalue = int(getValueAlter(node_dst,'value',1))
        else:
            uniquenodelist[isExists]['value'] += getValueAlter(row,'session_cnt',1)  # 원 크기
            if max_nodevalue < float(uniquenodelist[isExists]['value']): max_nodevalue = float( uniquenodelist[isExists]['value'])

    #uniquenodelist = list(set(uniquenodelist))

    for doc in res['hits']['hits']:
        row = doc['_source']
        if row['dst_ip'] == None \
                or row['src_ip'] == None:
            continue
        timestamp = Local2UTC(parser.parse(row['session_min_time'])).strftime("%Y-%m-%d %H:%M:%S")
        targetIdx = next((index for (index, d) in enumerate(uniquenodelist) if d["name"] == str(row['dst_ip'])), None)
        sourceIdx = next((index for (index, d) in enumerate(uniquenodelist) if d["name"] == str(row['src_ip'])), None)
        distance = getValueAlter(row,'geoip_distance',None)

        link = {
            "source": targetIdx,  # src_ip
            "target": sourceIdx,  # dst_ip
            "timestamp": timestamp,
            "value": getLineWidth( row.get('bytes'), max_link.get('bytes')),
            "s_count" : row.get('session_cnt'),
            "s_time" : row.get('differ_time'),
            "bytes" : row.get('bytes'),
            "pkts": row.get('pkts'),
            "tcp_urg" : row.get('tcp_flags_URG'),
            "tcp_ack": row.get('tcp_flags_ACK'),
            "tcp_psh": row.get('tcp_flags_PSH'),
            "tcp_rst": row.get('tcp_flags_RST'),
            "tcp_syn": row.get('tcp_flags_SYN'),
            "tcp_fin": row.get('tcp_flags_FIN'),
            "tcp_urg_p": row.get('tcp_flags_URG_P'),
            "tcp_ack_p": row.get('tcp_flags_ACK_P'),
            "tcp_psh_p": row.get('tcp_flags_PSH_P'),
            "tcp_rst_p": row.get('tcp_flags_RST_P'),
            "tcp_syn_p": row.get('tcp_flags_SYN_P'),
            "tcp_fin_p": row.get('tcp_flags_FIN_P'),
            "distance": distance,
            "protocol" : row.get('protocol'),
            "profile" : row.get('profile')
            #,"svrip_base_conn_cnt": row['svrip_base_conn_cnt'],
            #"clip_base_conn_cnt": row['clip_base_conn_cnt']

        }
        links.append(link)

    for _node in uniquenodelist:
        node = {
            "name": _node['name'].replace(' ',''),
            "ip" : _node['ip'],
            "value": getCircleSize(float(_node['value']), max_nodevalue),
            "color" : _node['color'],
            "conCount" : _node['value'],
            "type" : _node['type']
        }
        nodes.append(node)

    chartdata["nodes"] = nodes
    chartdata["links"] = links
    chartdata['maxdata'] = max_link

    return json.dumps(chartdata)

def NetLinkReSearch(es, result, max_node_size):
    next_ip_list = list()
    if result is not None :
        for _row in result['hits']['hits']:
            if next_ip_list.__len__() > max_node_size:
                break;
            i =  next_ip_list.index(_row['_source']['src_ip']) >= 0 if _row['_source']['src_ip'] in next_ip_list else None
            if i is None :
                next_ip_list.append(_row['_source']['src_ip'])
            i = next_ip_list.index(_row['_source']['dst_ip']) >= 0 if _row['_source']['dst_ip'] in next_ip_list else None
            if i is None :
                next_ip_list.append(_row['_source']['dst_ip'])
    else:
        next_ip_list = None

    body = GetLinkDnaListQueryEs(request, max_nodes_size, 0, next_ip_list)
    return es.search(index="gsp-*", doc_type="link_dna_tuple4", body=body, request_timeout=30)

def getLineWidth(curValue, maxValue):
    maxWidth = 5.0
    minWidth = 1.0

    if curValue is None or maxValue is None:
        return minWidth

    size = curValue / float(maxValue) *  maxWidth

    if size < minWidth:
        return minWidth
    else:
        return size

def getCircleSize(curValue, maxValue):
    maxRadius = 20.0
    minRadius = 3.0

    if curValue is None or maxValue is None:
        return minRadius

    size = curValue / float(maxValue) *  maxRadius

    if size < minRadius:
        return minRadius
    else:
        return size


@blueprint_page.route('/ip-geo-data/<string:datasource>', methods=['GET'])
def getgeodata(datasource):
    max_search_node_count = 3;
    es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
    srcip = request.args['srcip'].replace('?','')
    #srcip = srcip[0:srcip.index(":")]
    dstip = request.args['dstip']
    doc = {
        "query" : {
         "bool" : {
         	"must": [
         		{"term" : { "src_ip.keyword" : srcip} },
         		{"term" : { "dst_ip.keyword" : dstip} }
         		]
         }
        },
        "from": 0,
        "size": 1000
    }

    res = es.search(index= "gsp*" + "", doc_type="link_dna_tuple4", body=doc)
    chartdata = OrderedDict()
    nodes = list()
    links = list()

    nethistory = res['hits']['hits']

    _count = 0
    getNodesAndLinks(nethistory, nodes, links, srcip, _count, max_search_node_count)
    getNodesAndLinks(nethistory, nodes, links, dstip, _count, max_search_node_count)

    chartdata["lines"] = links
    chartdata["images"] = nodes

    return json.dumps(chartdata)

def search_link(links, ipsrc, ipdst):
    return [item for item in links if item["source"] == ipsrc and item["target"] == ipdst]

def getNodesAndLinks(nethistory, nodes, links, searchip, recursive_count, max_recursive_count):

    next_searchip = []

    _nethistory = [item for item in nethistory if item['_source'].get('dst_ip') == searchip or item['_source'].get('src_ip') == searchip ]

    for _item in _nethistory:
        if _item['_source'].get('dst_ip') == None or _item['_source'].get('src_ip') == None:
            continue
        ipv4_src_addr = _item['_source']['dst_ip']
        ipv4_dst_addr = _item['_source']['src_ip']

        # 테스트를 위해 src geo 정보는 서울로 고정
        src_latitude = _item['_source']['src_lat']
        src_longitude = _item['_source']['src_lon']
        if src_latitude is None:
            src_latitude = "37.532600"
        if src_longitude is None:
            src_longitude = "127.024612"

        # src_title = "%s : %s %s" % ipv4_src_addr, _item['_source']['src_geoip']['country_name'], _item['_source']['src_geoip']['city_name']
        src_nation_cd = next((index for (index, d) in enumerate(Nations.nations)
                       if d["code"] == _item['_source'].get('src_country_code')), None)
        src_title = "%s : %s %s" % (ipv4_dst_addr, _item['_source'].get('src_country_code'), src_nation_cd)
        dst_nation_cd = next((index for (index, d) in enumerate(Nations.nations)
                              if d["code"] == _item['_source'].get('dst_country_code')), None)
        dst_title = "%s : %s %s" % (ipv4_dst_addr, _item['_source'].get('dst_country_code'), dst_nation_cd)


        # src_latitudes = _item['_source']['src_geoip']['latitudes']
        # src_longitudes = _item['_source']['src_geoip']['longitudes']
        dst_latitude = _item['_source']['dst_lat']
        dst_longitude = _item['_source']['dst_lon']

        result = search_link(links, ipv4_src_addr, ipv4_dst_addr)
        if result.__len__() > 0:
            continue
        else:
            link = {
                "source": ipv4_src_addr,
                "target": ipv4_dst_addr,
                "latitudes": [src_latitude, dst_latitude],
                "longitudes": [src_longitude, dst_longitude],
                "value": 1
            }
            links.append(link)

            # node
            node_src = {
                "id": ipv4_src_addr,
                "title": src_title,
                "latitude": src_latitude,
                "longitude": src_longitude,
                "scale": 1
            }

            node_dst = {
                "id": ipv4_dst_addr,
                "title": dst_title,
                "latitude": dst_latitude,
                "longitude": dst_longitude,
                "scale": 0.5
            }

            nodes.append(node_src)
            nodes.append(node_dst)

            next_searchip.append(ipv4_dst_addr)


    #for문 end

    if recursive_count < max_recursive_count :
        for _next_searchip in next_searchip :
            getNodesAndLinks(nethistory, nodes, links, _next_searchip, recursive_count+1, max_recursive_count)

def getValueAlter(dic, key, default):
    value = dic.get(key)
    if value is None:
        return default
    else:
        return value