#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import parser
from flask import json

from GSP_WEB import db_session
from GSP_WEB.common.util.elasticsearch_helper import CreateFilterQuery, CreateEsQuery, CreateFilterQuery_IP, \
    CreateFilterQuery_AdditionalIP
from GSP_WEB.models.Rules_Profile import Rules_Profile


def GetLinkDnaListQueryEs(request, per_page = None, start_idx = None, add_ip = None):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    else:
        str_dt = (datetime.utcnow()- timedelta(hours=1)).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()
    else:
        end_dt = datetime.utcnow().isoformat()

    if request.form.get('timeSpan') is not None and request.form.get('timeSpan') != "":
        str_dt = "now-"+request.form.get('timeSpan')
        end_dt = "now"

    if per_page == None:
        per_page = int(request.form['perpage'])
    if start_idx == None:
        start_idx = int(request.form['start'])
    page_no = int(start_idx / per_page)

    search_profile_seq = request.form.get('search_profile')
    search_profile = ''
    search_profile_result = db_session.query(Rules_Profile).filter_by(seq=search_profile_seq).first()
    if search_profile_result is None:
        search_profile = ''
    else:
        search_profile = search_profile_result.name

    #region get parameter
    search_data_type = request.form.get("search_data_type")
    search_src_ip = request.form.get('search_src_ip_value')
    search_src_ip_opt = request.form.get('search_src_ip_opt')
    search_dst_ip = request.form.get('search_dst_ip_value')
    search_dst_ip_opt = request.form.get('search_dst_ip_opt')
    search_src_port_value = request.form.get('search_src_port_value')
    search_src_port_opt = request.form.get('search_src_port_opt')
    search_dst_port_value = request.form.get('search_dst_port_value')
    search_dst_port_opt = request.form.get('search_dst_port_opt')
    search_protocol_opt = request.form.get('search_protocol_opt')
    search_protocol_value = request.form.get('search_protocol_value')
    byte_opt = request.form['search_bytes_opt']
    byte_value = request.form['search_bytes_value']
    packet_opt = request.form['search_pkts_opt']
    packet_value = request.form['search_pkts_value']
    session_time_opt = request.form['search_differ_time_opt']
    session_time_value = request.form['search_differ_time_value']
    session_count_opt = request.form['search_session_cnt_opt']
    session_count_value = request.form['search_session_cnt_value']
    flag_urg_opt   = request.form['search_tcp_flag_URG_opt']
    flag_urg_value = request.form['search_tcp_flag_URG_value']
    flag_ack_opt   = request.form['search_tcp_flag_ACK_opt']
    flag_ack_value = request.form['search_tcp_flag_ACK_value']
    flag_psh_opt   = request.form['search_tcp_flag_PSH_opt']
    flag_psh_value = request.form['search_tcp_flag_PSH_value']
    flag_rst_opt   = request.form['search_tcp_flag_RST_opt']
    flag_rst_value = request.form['search_tcp_flag_RST_value']
    flag_syn_opt   = request.form['search_tcp_flag_SYN_opt']
    flag_syn_value = request.form['search_tcp_flag_SYN_value']
    flag_fin_opt   = request.form['search_tcp_flag_FIN_opt']
    flag_fin_value = request.form['search_tcp_flag_FIN_value']
    #flag_percentage
    flag_per_urg_opt   = request.form.get('search_tcp_flag_URG_P_opt')
    flag_per_urg_value = request.form.get('search_tcp_flag_URG_P_value')
    flag_per_ack_opt   = request.form.get('search_tcp_flag_ACK_P_opt')
    flag_per_ack_value = request.form.get('search_tcp_flag_ACK_P_value')
    flag_per_psh_opt   = request.form.get('search_tcp_flag_PSH_P_opt')
    flag_per_psh_value = request.form.get('search_tcp_flag_PSH_P_value')
    flag_per_rst_opt   = request.form.get('search_tcp_flag_RST_P_opt')
    flag_per_rst_value = request.form.get('search_tcp_flag_RST_P_value')
    flag_per_syn_opt   = request.form.get('search_tcp_flag_SYN_P_opt')
    flag_per_syn_value = request.form.get('search_tcp_flag_SYN_P_value')
    flag_per_fin_opt   = request.form.get('search_tcp_flag_FIN_P_opt')
    flag_per_fin_value = request.form.get('search_tcp_flag_FIN_P_value')
    #flag_percentage end
    geo_distance_opt = request.form['search_geoip_distance_opt']
    geo_distance_value = request.form['search_geoip_distance_value']
    search_src_country = request.form.get('search_src_country_value')
    search_dst_country = request.form.get('search_dst_country_value')
    #endregion
    #syslog 관련
    search_syslog_name_opt =request.form.get('search_geoip_distance_opt')
    search_syslog_name_value = request.form.get('search_geoip_distance_value')
    search_msg_opt = request.form.get('search_msg_opt')
    search_msg_value = request.form.get('search_msg_value')
    #endregion

    query = """
    select * FROM {0} 
    where
    1 = 1 
     """

    mustlist = []
    notmustlist = []
    shouldlist = []

    # if search_profile != "":
    #     profileName = "*"+search_profile+"*"
    #     query = dict()
    #     profile_dict = dict()
    #     profile_dict["profile"] = profileName.encode('utf8')
    #     query["wildcard"] = profile_dict
    #     #query = { "wildcard" : { "profile" :  profileName.encode("utf-8")} }
    #     mustlist.append(query)

    #region make query

    if str_dt != "" and end_dt != "":
        query = { "range":{"min_timestamp": {"gte": str_dt, "lte": end_dt}} }
        mustlist.append(query)

    if search_data_type != "":
        query = CreateFilterQuery_IP("=", "data_type", search_data_type)
        mustlist.append(query)

    if search_src_ip != "" and search_src_ip is not None  and search_src_ip_opt != "" and add_ip is None:
        query = CreateFilterQuery_IP(search_src_ip_opt, "src_ip", search_src_ip)
        if search_src_ip_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if search_dst_ip != ""and search_dst_ip is not None and search_dst_ip_opt != "" and add_ip is None:
        query = CreateFilterQuery_IP(search_dst_ip_opt, "dst_ip", search_dst_ip)
        if search_dst_ip_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if add_ip is not None:
        query = CreateFilterQuery_AdditionalIP(add_ip)
        mustlist.append(query)

    if search_src_port_value is not None and search_src_port_value != "" :
        query = CreateFilterQuery_IP(search_src_port_opt, "src_port", search_src_port_value)
        if search_src_port_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_dst_port_value is not None and search_dst_port_value != "" :
        query = CreateFilterQuery_IP(search_dst_port_opt, "dst_port", search_dst_port_value)
        if search_dst_port_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_protocol_value is not None and search_protocol_value != "" :
        query = CreateFilterQuery_IP(search_protocol_opt, "protocol", search_protocol_value)
        if search_protocol_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if byte_opt != "" and byte_value != "" :
        query = CreateFilterQuery(byte_opt, "bytes", byte_value)
        if byte_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if  packet_opt != "" and packet_value != "" :
        query = CreateFilterQuery(packet_opt, "pkts", packet_value)
        if packet_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if session_time_opt != "" and session_time_value != "":
        query = CreateFilterQuery(session_time_opt, "differ_time", session_time_value)
        if session_time_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if session_count_opt != "" and session_count_value != "":
        query = CreateFilterQuery(session_count_opt, "session_cnt", session_count_value)
        if session_count_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_urg_opt != "" and flag_urg_value != "":
        query = CreateFilterQuery(flag_urg_opt, "tcp_flags_URG", flag_urg_value)
        if flag_urg_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_ack_opt != "" and flag_ack_value != "":
        query = CreateFilterQuery(flag_ack_opt, "tcp_flags_ACK", flag_ack_value)
        if flag_ack_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_psh_opt != "" and flag_psh_value != "":
        query = CreateFilterQuery(flag_psh_opt, "tcp_flags_PSH", flag_psh_value)
        if flag_psh_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_rst_opt != "" and flag_rst_value != "":
        query = CreateFilterQuery(flag_rst_opt, "tcp_flags_RST", flag_rst_value)
        if flag_rst_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_syn_opt != "" and flag_syn_value != "":
        query = CreateFilterQuery(flag_syn_opt, "tcp_flags_SYN", flag_syn_value)
        if flag_syn_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_fin_opt != "" and flag_fin_value != "":
        query = CreateFilterQuery(flag_fin_opt, "tcp_flags_FIN", flag_fin_value)
        if flag_fin_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if flag_per_urg_value is not None and flag_per_urg_value != "":
        query = CreateFilterQuery(flag_per_urg_opt, "tcp_flags_URG_P", flag_per_urg_value)
        if flag_per_urg_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_ack_value is not None and flag_per_ack_value != "":
        query = CreateFilterQuery(flag_per_ack_opt, "tcp_flags_ACK_P", flag_per_ack_value)
        if flag_per_ack_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_psh_value is not None and flag_per_psh_value != "":
        query = CreateFilterQuery(flag_per_psh_opt, "tcp_flags_PSH_P", flag_per_psh_value)
        if flag_per_psh_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_rst_value is not None and flag_per_rst_value != "":
        query = CreateFilterQuery(flag_per_rst_opt, "tcp_flags_RST_P", flag_per_rst_value)
        if flag_per_rst_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_syn_value is not None and flag_per_syn_value != "":
        query = CreateFilterQuery(flag_per_syn_opt, "tcp_flags_SYN_P", flag_per_syn_value)
        if flag_per_syn_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_fin_value is not None and flag_per_fin_value != "":
        query = CreateFilterQuery(flag_per_fin_opt, "tcp_flags_FIN_P", flag_per_fin_value)
        if flag_per_fin_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if geo_distance_opt != "" and geo_distance_value != "":
        query = CreateFilterQuery(geo_distance_opt, "geoip_distance", geo_distance_value)
        if geo_distance_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_src_country is not None and search_src_country != "" :
        query = CreateFilterQuery("=", "src_country_code.keyword", search_src_country)
        mustlist.append(query)

    if search_dst_country is not None and search_dst_country != "" :
        query = CreateFilterQuery("=", "dst_country_code.keyword", search_dst_country)
        mustlist.append(query)

    if search_syslog_name_value is not None and search_syslog_name_value != "" :
        query = CreateFilterQuery(search_syslog_name_opt, "syslog_name.keyword", search_syslog_name_value)
        if search_syslog_name_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_msg_value is not None and search_msg_value != "" :
        query = CreateFilterQuery(search_msg_opt, "msg", "*" + search_msg_value + "*")
        if search_msg_opt == "like":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    #endregion

    completeQuery = CreateEsQuery(per_page, page_no*per_page, mustlist, notmustlist, shouldlist )

    return completeQuery

def GetLinkDnaDetailQuery(request, tblName):
    query ={

    }
    return

def GetLinkDnaListQueryForProfile(params):
    jsonData = json.loads(params)
    str_dt = ""
    end_dt = ""
    if jsonData.get('timeFrom') is not None and jsonData.get('timeFrom') != "":
        str_dt = parser.parse(jsonData.get('timeFrom')).isoformat()
    else:
        str_dt = (datetime.utcnow()- timedelta(hours=1)).isoformat()
    if jsonData.get('timeTo') is not None and jsonData.get('timeTo') != "":
        end_dt = parser.parse(jsonData.get('timeTo')).isoformat()
    else:
        end_dt = datetime.utcnow().isoformat()

    search_data_type = jsonData.get("search_data_type")
    search_src_ip = jsonData.get('search_src_ip_value')
    search_src_ip_opt = jsonData.get('search_src_ip_opt')
    search_dst_ip = jsonData.get('search_dst_ip_value')
    search_dst_ip_opt = jsonData.get('search_dst_ip_opt')
    search_src_port_value = jsonData.get('search_src_port_value')
    search_src_port_opt = jsonData.get('search_src_port_opt')
    search_protocol_opt = jsonData.get('search_protocol_opt')
    search_protocol_value = jsonData.get('search_protocol_value')
    byte_opt = jsonData.get('search_bytes_opt')
    byte_value = jsonData.get('search_bytes_value')
    packet_opt = jsonData.get('search_pkts_opt')
    packet_value = jsonData.get('search_pkts_value')
    session_time_opt = jsonData.get('search_differ_time_opt')
    session_time_value = jsonData.get('search_differ_time_value')
    session_count_opt = jsonData.get('search_session_cnt_opt')
    session_count_value = jsonData.get('search_session_cnt_value')
    flag_urg_opt   = jsonData.get('search_tcp_flag_URG_opt')
    flag_urg_value = jsonData.get('search_tcp_flag_URG_value')
    flag_ack_opt   = jsonData.get('search_tcp_flag_ACK_opt')
    flag_ack_value = jsonData.get('search_tcp_flag_ACK_value')
    flag_psh_opt   = jsonData.get('search_tcp_flag_PSH_opt')
    flag_psh_value = jsonData.get('search_tcp_flag_PSH_value')
    flag_rst_opt   = jsonData.get('search_tcp_flag_RST_opt')
    flag_rst_value = jsonData.get('search_tcp_flag_RST_value')
    flag_syn_opt   = jsonData.get('search_tcp_flag_SYN_opt')
    flag_syn_value = jsonData.get('search_tcp_flag_SYN_value')
    flag_fin_opt   = jsonData.get('search_tcp_flag_FIN_opt')
    flag_fin_value = jsonData.get('search_tcp_flag_FIN_value')
    # flag_percentage
    flag_per_urg_opt   = jsonData.get('search_tcp_flag_URG_P_opt')
    flag_per_urg_value = jsonData.get('search_tcp_flag_URG_P_value')
    flag_per_ack_opt   = jsonData.get('search_tcp_flag_ACK_P_opt')
    flag_per_ack_value = jsonData.get('search_tcp_flag_ACK_P_value')
    flag_per_psh_opt   = jsonData.get('search_tcp_flag_PSH_P_opt')
    flag_per_psh_value = jsonData.get('search_tcp_flag_PSH_P_value')
    flag_per_rst_opt   = jsonData.get('search_tcp_flag_RST_P_opt')
    flag_per_rst_value = jsonData.get('search_tcp_flag_RST_P_value')
    flag_per_syn_opt   = jsonData.get('search_tcp_flag_SYN_P_opt')
    flag_per_syn_value = jsonData.get('search_tcp_flag_SYN_P_value')
    flag_per_fin_opt   = jsonData.get('search_tcp_flag_FIN_P_opt')
    flag_per_fin_value = jsonData.get('search_tcp_flag_FIN_P_value')
    # flag_percentage end
    geo_distance_opt = jsonData.get('search_geoip_distance_opt')
    geo_distance_value = jsonData.get('search_geoip_distance_value')
    search_src_country = jsonData.get('search_src_country_value')
    search_dst_country = jsonData.get('search_dst_country_value')

    search_syslog_name_opt = jsonData.get('search_geo_distance_opt')
    search_syslog_name_value = jsonData.get('search_geo_distance_value')
    search_msg_opt = jsonData.get('search_msg_opt')
    search_msg_value = jsonData.get('search_msg_value')

    query = """
    select * FROM {0} 
    where
    1 = 1 
     """

    mustlist = []
    notmustlist = []
    shouldlist = []

    if str_dt != "" and end_dt != "":
        query = { "range":{"min_timestamp": {"gte": str_dt, "lte": end_dt}} }
        mustlist.append(query)

    if search_data_type != "":
        query = CreateFilterQuery_IP("=", "data_type", search_data_type)
        mustlist.append(query)

    if search_src_ip != "" and search_src_ip is not None  and search_src_ip_opt != "":
        query = CreateFilterQuery(search_src_ip_opt, "src_ip", search_src_ip)
        if search_src_ip_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if search_dst_ip != ""and search_dst_ip is not None and search_dst_ip_opt != "":
        query = CreateFilterQuery(search_dst_ip_opt, "dst_ip", search_dst_ip)
        if search_dst_ip_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_src_port_opt != "" and search_src_port_value != "" :
        query = CreateFilterQuery(search_src_port_opt, "src_port", search_src_port_value)
        if search_src_port_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_protocol_value is not None and search_protocol_value != "" :
        query = CreateFilterQuery(search_protocol_opt, "protocol", search_protocol_value)
        if search_protocol_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if byte_opt != "" and byte_value != "" :
        query = CreateFilterQuery(byte_opt, "bytes", byte_value)
        if byte_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if  packet_opt != "" and packet_value != "" :
        query = CreateFilterQuery(packet_opt, "pkts", packet_value)
        if packet_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if session_time_opt != "" and session_time_value != "":
        query = CreateFilterQuery(session_time_opt, "differ_time", session_time_value)
        if session_time_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if session_count_opt != "" and session_count_value != "":
        query = CreateFilterQuery(session_count_opt, "session_cnt", session_count_value)
        if session_count_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_urg_opt != "" and flag_urg_value != "":
        query = CreateFilterQuery(flag_urg_opt, "tcp_flags_URG", flag_urg_value)
        if flag_urg_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_ack_opt != "" and flag_ack_value != "":
        query = CreateFilterQuery(flag_ack_opt, "tcp_flags_ACK", flag_ack_value)
        if flag_ack_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_psh_opt != "" and flag_psh_value != "":
        query = CreateFilterQuery(flag_psh_opt, "tcp_flags_PSH", flag_psh_value)
        if flag_psh_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_rst_opt != "" and flag_rst_value != "":
        query = CreateFilterQuery(flag_rst_opt, "tcp_flags_RST", flag_rst_value)
        if flag_rst_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_syn_opt != "" and flag_syn_value != "":
        query = CreateFilterQuery(flag_syn_opt, "tcp_flags_SYN", flag_syn_value)
        if flag_syn_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_fin_opt != "" and flag_fin_value != "":
        query = CreateFilterQuery(flag_fin_opt, "tcp_flags_FIN", flag_fin_value)
        if flag_fin_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_urg_opt != "" and flag_per_urg_value != "":
        query = CreateFilterQuery(flag_per_urg_opt, "tcp_flags_URG_P", flag_per_urg_value)
        if flag_per_urg_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_ack_opt != "" and flag_per_ack_value != "":
        query = CreateFilterQuery(flag_per_ack_opt, "tcp_flags_ACK_P", flag_per_ack_value)
        if flag_per_ack_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_psh_opt != "" and flag_per_psh_value != "":
        query = CreateFilterQuery(flag_per_psh_opt, "tcp_flags_PSH_P", flag_per_psh_value)
        if flag_per_psh_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_rst_opt != "" and flag_per_rst_value != "":
        query = CreateFilterQuery(flag_per_rst_opt, "tcp_flags_RST_P", flag_per_rst_value)
        if flag_per_rst_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_syn_opt != "" and flag_per_syn_value != "":
        query = CreateFilterQuery(flag_per_syn_opt, "tcp_flags_SYN_P", flag_per_syn_value)
        if flag_per_syn_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if flag_per_fin_opt != "" and flag_per_fin_value != "":
        query = CreateFilterQuery(flag_per_fin_opt, "tcp_flags_FIN_P", flag_per_fin_value)
        if flag_per_fin_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if geo_distance_opt != "" and geo_distance_value != "":
        query = CreateFilterQuery(geo_distance_opt, "geoip_distance", geo_distance_value)
        if geo_distance_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_src_country is not None and search_src_country != "" :
        query = CreateFilterQuery("=", "src_country_code.keyword", search_src_country)
        mustlist.append(query)

    if search_dst_country is not None and search_dst_country != "" :
        query = CreateFilterQuery("=", "dst_country_code.keyword", search_dst_country)
        mustlist.append(query)

    if search_syslog_name_value is not None and search_syslog_name_value != "" :
        query = CreateFilterQuery(search_syslog_name_opt, "syslog_name.keyword", search_syslog_name_value)
        if search_syslog_name_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_msg_value is not None and search_msg_value != "" :
        query = CreateFilterQuery(search_msg_opt, "msg", "*" + search_msg_value + "*")
        if search_msg_opt == "like":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    completeQuery = CreateEsQuery(10000, 0, mustlist, notmustlist, shouldlist )

    return completeQuery

def GetProfileOperation(pattern_ui, profile_name, group_code):
    uiElements =json.loads(pattern_ui)
    results = dict()
    results['keys'] = list()

    values = [item for item in uiElements if item.find('_value') > 0 and uiElements[item] != '' ]

    for _val in values:
        key = _val.replace('search_', '').replace('_value', '')
        value = uiElements[_val]
        opt = uiElements.get(_val.replace('_value', '_opt'))
        if opt == None:
            opt = '='

        results['keys'].append( {
            key : {
            'opt' : opt,
            'val' : value
            }
        })
        results['profile_name'] = profile_name
        results['group_code'] = group_code

    return json.dumps(results, ensure_ascii=False)

#region Server Connection Count
def GetLinkDnaTuple3(start_time, end_time, con_src_from, con_src_to):
    str_dt = parser.parse(start_time+":00").isoformat()
    end_dt = parser.parse(end_time+":00").isoformat()

    doc = {
        "size": 1000,
        "query":
            {
                "bool": {
                    "must": [
                        {
                            "range": {"start_time": {"gte": str_dt, "lte": end_dt}}
                        }
                    ]
                }
            }
        ,
        "sort": [
            {
                "cnt": {
                    "order": "desc"
                }
            }
        ]
    }

    if con_src_from != "" or con_src_to != "":
        con_range = { "range" : { "cnt" : {} }}
        doc['query']['bool']['must'].append(con_range)

    if con_src_from != '':
        doc['query']['bool']['must'][1]['range']['cnt']['gte'] = con_src_from
    if con_src_to != '':
        doc['query']['bool']['must'][1]['range']['cnt']['lte'] = con_src_to

    return doc

#region Client Connection Count
def GetLinkDnaTuple2(start_time, end_time, con_src_from, con_src_to):
    str_dt = parser.parse(start_time).isoformat()
    end_dt = parser.parse(end_time).isoformat()

    doc = {
        "size": 1000,
        "query":
            {
                "bool": {
                    "must": [
                        {
                            "range": {"start_time": {"gte": str_dt, "lte": end_dt}}
                        }
                    ]
                }
            }
        ,
        "sort": [
            {
                "cnt": {
                    "order": "desc"
                }
            }
        ]
    }

    if con_src_from != "" or con_src_to != "":
        con_range = { "range" : { "cnt" : {} }}
        doc['query']['bool']['must'].append(con_range)

    if con_src_from != '':
        doc['query']['bool']['must'][1]['range']['cnt']['gte'] = con_src_from
    if con_src_to != '':
        doc['query']['bool']['must'][1]['range']['cnt']['lte'] = con_src_to

    return doc

#region Server Connection Count
def GetServerConnectionCount(start_time, end_time, src_ip, src_port):

    doc = {
        "size": 1,
        "query":
            {
                "bool": {
                    "must": [
                        {
                            "term": {"start_time": start_time.isoformat()}
                        },
                        {
                            "term": {"end_time": end_time.isoformat()}
                        },
                        {
                            "term": { "src_ip.keyword": src_ip }
                        },
                        {
                            "term": { "src_port": src_port }
                        }
                    ]
                }
            }
    }

    return doc

#region Get Matched Info (Traffic Data, SysLog)
def GetMatchedInfo(start_time, end_time, src_ip, src_port, dst_ip):

    doc = {
        "size": 1,
        "query":
            {
                "bool": {
                    "must": [
                        {
                            "range": {"@timestamp":
                                {
                                    "gte": start_time.isoformat(),
                                    "lte" : end_time.isoformat()
                                }
                            }
                        },
                        {
                            "term": { "src_ip.keyword": src_ip }
                        },
                        {
                            "term": { "src_port": src_port }
                        },
                        {
                            "term": {"dst_ip.keyword": dst_ip}
                        }
                    ]
                }
            }
    }

    return doc

#region Server Connection Count
def GetClientConnectionCount(start_time, end_time, dst_ip):

    doc = {
        "size": 1,
        "query":
            {
                "bool": {
                    "must": [
                        {
                            "term": {"start_time": start_time.isoformat()}
                        },
                        {
                            "term": {"end_time": end_time.isoformat()}
                        },
                        {
                            "term": { "dst_ip.keyword": dst_ip }
                        }
                    ]
                }
            }
    }

    return doc