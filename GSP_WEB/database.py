
def init_db(db):
    from GSP_WEB.models import Account, StandardLog, IP_WhiteList, IP_BlackList,  Rules_CNC \
            ,Rules_BlackList, Rules_WhiteList, Rules_Snort, Rules_Profile,GlobalSetting \
            ,Rules_FileAnalysis, Rules_Profile_Group, Rules_White_IP, Rules_White_IP_URL, Link_Element_TypeA \
            ,Link_Element_TypeB, DNA_Element, DNA_Schedule, DNA_StandardData, Data_Element, Rules_IP_Collection, wl_maintenance_period, TI_Dashboard_data, malicious_info
    db.create_all()
    db_session = db.session
    return

