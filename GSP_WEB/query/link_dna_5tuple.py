from datetime import datetime, timedelta
from dateutil import parser
from flask import json

from GSP_WEB import db_session
from GSP_WEB.common.util.date_util import Local2UTC
from GSP_WEB.common.util.elasticsearch_helper import CreateFilterQuery, CreateEsQuery, CreateFilterQuery_IP, \
    CreateFilterQuery_AdditionalIP
from GSP_WEB.models.Rules_Profile import Rules_Profile


def GetLinkDnaListQueryEs(request, per_page = None, start_idx = None, add_ip = None):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = Local2UTC(parser.parse(request.form['timeFrom'])).isoformat()
    else:
        str_dt = (datetime.utcnow()- timedelta(hours=1)).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = Local2UTC(parser.parse(request.form['timeTo'])).isoformat()
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

    #region get parameter
    search_data_type = request.form.get("search_data_type")
    search_src_ip = request.form.get('search_src_ip')
    search_src_ip_opt = request.form.get('search_src_ip_opt')
    search_dst_ip = request.form.get('search_dst_ip')
    search_dst_ip_opt = request.form.get('search_dst_ip_opt')
    search_src_port_value = request.form.get('search_src_port_value')
    search_src_port_opt = request.form.get('search_src_port_opt')
    search_dst_port_value = request.form.get('search_dst_port_value')
    search_dst_port_opt = request.form.get('search_dst_port_opt')
    search_protocol_opt = request.form.get('search_protocol_opt')
    search_protocol_value = request.form.get('search_protocol_value')
    search_packet_opt = request.form['search_packet_opt']
    search_packet_value = request.form['search_packet_value']
    search_bytes_opt = request.form['search_bytes_opt']
    search_bytes_value = request.form['search_bytes_value']
    flag_urg_opt = request.form['search_flag_urg_opt']
    flag_urg_value = request.form['search_flag_urg_value']
    flag_ack_opt = request.form['search_flag_ack_opt']
    flag_ack_value = request.form['search_flag_ack_value']
    flag_psh_opt = request.form['search_flag_psh_opt']
    flag_psh_value = request.form['search_flag_psh_value']
    flag_rst_opt = request.form['search_flag_rst_opt']
    flag_rst_value = request.form['search_flag_rst_value']
    flag_syn_opt = request.form['search_flag_syn_opt']
    flag_syn_value = request.form['search_flag_syn_value']
    flag_fin_opt = request.form['search_flag_fin_opt']
    flag_fin_value = request.form['search_flag_fin_value']
    geo_distance_opt = request.form['search_geo_distance_opt']
    geo_distance_value = request.form['search_geo_distance_value']
    search_src_country = request.form.get('search_src_country')
    search_dst_country = request.form.get('search_dst_country')
    search_syslog_name_opt = request.form.get('search_syslog_name_opt')
    search_syslog_name_value = request.form.get('search_syslog_name_value')
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


    #region make query

    if str_dt != "" and end_dt != "":
        query = { "range":{"min_timestamp": {"gte": str_dt, "lte": end_dt}} }
        mustlist.append(query)

    if search_data_type != "" and search_data_type is not None:
        query = CreateFilterQuery_IP("=", "data_type", search_data_type)
        mustlist.append(query)

    if search_src_ip != "" and search_src_ip is not None  and search_src_ip_opt != "":
        query = CreateFilterQuery_IP(search_src_ip_opt, "src_ip", search_src_ip)
        if search_src_ip_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if search_dst_ip != ""and search_dst_ip is not None and search_dst_ip_opt != "":
        query = CreateFilterQuery_IP(search_dst_ip_opt, "dst_ip", search_dst_ip)
        if search_dst_ip_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_src_port_value is not None and search_src_port_value != "" :
        query = CreateFilterQuery(search_src_port_opt, "src_port", search_src_port_value)
        if search_src_port_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_dst_port_value is not None and search_dst_port_value != "" :
        query = CreateFilterQuery(search_dst_port_opt, "dst_port", search_dst_port_value)
        if search_dst_port_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if search_protocol_value is not None and search_protocol_value != "" :
        query = CreateFilterQuery(search_protocol_opt, "protocol", search_protocol_value)
        if search_protocol_opt != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)

    if  search_packet_opt != "" and search_packet_value != "" :
        query = CreateFilterQuery(search_packet_opt, "in_pkts", search_packet_value)
        if search_packet_value != "!=":
            mustlist.append(query)
        else:
            notmustlist.append(query)
    if search_bytes_opt != "" and search_bytes_value != "":
        query = CreateFilterQuery(search_bytes_opt, "in_bytes", search_bytes_value)
        if search_bytes_value != "!=":
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