from dateutil import parser

import datetime

from GSP_WEB.common.util.date_util import Local2UTC


def GetNetLinkChartQuery(request, tblName):
    str_dt = ""
    end_dt = ""
    if request.form['timeFrom'] != "":
        utcTime = Local2UTC(parser.parse(request.form['timeFrom']))
        str_dt = utcTime.strftime('%Y-%m-%d %H:%M:%S')
    if request.form['timeTo'] != "":
        utcTime = Local2UTC(parser.parse(request.form['timeTo']))
        end_dt = utcTime.strftime('%Y-%m-%d %H:%M:%S')
    search_ip = request.form['search_ip']
    search_ip_opt = request.form['search_ip_opt']
    sendbyte_opt = request.form['search_sendbyte_opt']
    sendbyte_value = request.form['search_sendbyte_value']
    receivebyte_opt = request.form['search_receivebyte_opt']
    receivebyte_value = request.form['search_receivebyte_value']
    sendpacket_opt = request.form['search_sendpacket_opt']
    sendpacket_value = request.form['search_sendpacket_value']
    receive_packet_opt = request.form['search_receive_packet_opt']
    receive_packet_value = request.form['search_receive_packet_value']
    session_time_opt = request.form['search_session_time_opt']
    session_time_value = request.form['search_session_time_value']
    session_count_opt = request.form['search_session_count_opt']
    session_count_value = request.form['search_session_count_value']
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
    svr_con_count_opt = request.form['search_svr_con_count_opt']
    svr_con_count_value = request.form['search_svr_con_count_value']
    cli_con_count_opt = request.form['search_cli_con_count_opt']
    cli_con_count_value = request.form['search_cli_con_count_value']
    geo_distance_opt = request.form['search_geo_distance_opt']
    geo_distance_value = request.form['search_geo_distance_value']

    query = """
    select * FROM {0} 
    where
    1 = 1 
     """

    query = query.format(tblName)

    if str_dt != "" and end_dt != "":
        query += "and end_time between '{0}' and '{1}' \n".format(str_dt, end_dt)
    if search_ip != "" and search_ip_opt == "=":
        query += "and ( cl_ip = '{0}' or svr_ip = '{0}' )\n".format(search_ip)
    elif search_ip != "" and search_ip_opt == "!=":
        query += "and ( cl_ip <> '{0}' and svr_ip <> '{0}' )\n".format(search_ip)
    if sendbyte_opt != "" and sendbyte_value != "" :
        query += "and send_bytes {0} {1} \n".format(sendbyte_opt, sendbyte_value)
    if receivebyte_opt != "" and receivebyte_value != "":
        query += "and recv_bytes {0} {1} \n".format(receivebyte_opt, receivebyte_value)
    if  sendpacket_opt != "" and sendpacket_value != "" :
        query += "and send_pkts {0} {1} \n".format(sendpacket_opt, sendpacket_value)
    if receive_packet_opt != "" and receive_packet_value != "":
        query += "and recv_pkts {0} {1} \n".format(receive_packet_opt, receive_packet_value)
    if session_time_opt != "" and session_time_value != "":
        query += "and differ_time {0} {1} \n".format(session_time_opt, session_time_value)
    if session_count_opt != "" and session_count_value != "":
        query += "and session_cnt {0} {1} \n".format(session_count_opt, session_count_value)
    if flag_urg_opt != "" and flag_urg_value != "":
        query += "and tcp_flags_URG {0} {1} \n".format(flag_urg_opt, flag_urg_value)
    if flag_ack_opt != "" and flag_ack_value != "":
        query += "and tcp_flags_ACK {0} {1} \n".format(flag_ack_opt, flag_ack_value)
    if flag_psh_opt != "" and flag_psh_value != "":
        query += "and tcp_flags_PSH {0} {1} \n".format(flag_psh_opt, flag_psh_value)
    if flag_rst_opt != "" and flag_rst_value != "":
        query += "and tcp_flags_RST {0} {1} \n".format(flag_rst_opt, flag_rst_value)
    if flag_syn_opt != "" and flag_syn_value != "":
        query += "and tcp_flags_SYN {0} {1} \n".format(flag_syn_opt, flag_syn_value)
    if flag_fin_opt != "" and flag_fin_value != "":
        query += "and tcp_flags_FIN {0} {1} \n".format(flag_fin_opt, flag_fin_value)
    if svr_con_count_opt != "" and svr_con_count_value != "":
        query += "and svrip_base_conn_cnt {0} {1} \n".format(svr_con_count_opt, svr_con_count_value)
    if cli_con_count_opt != "" and cli_con_count_value != "":
        query += "and clip_base_conn_cnt {0} {1} \n".format(cli_con_count_opt, cli_con_count_value)
    if geo_distance_opt != "" and geo_distance_value != "":
        query += "and geoip_distance {0} {1} \n".format(geo_distance_opt, geo_distance_value)

    return query