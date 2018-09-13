#-*- coding: utf-8 -*-
import datetime

from dateutil import parser
from flask import json
from sqlalchemy import text

from GSP_WEB import db


class Link_Element_List:
    total = 0
    data = None



    def getList(self,start_idx, pagesize, keyword):

        totalQuery = '''
        select count(id) from (
            select id from GSP_WEB.Link_Element_TypeA
            union
            select id from GSP_WEB.Link_Element_TypeB) as a
        '''

        totalResult = db.engine.execute(totalQuery).fetchall()
        self.total = totalResult[0][0]

        query =\
            '''select * from ( 
                    select id, 'A-Type' as source, dst_columns_name as column_name, description as description
                    , src_type as src_type, src_columns_name as src_columns_name
                    ,use_yn as use_yn, cre_dt as cre_dt, mod_dt as mod_dt
                    , 'TypeA' as ElementType
                    , '' as operate_function
                    , '' as timespan
                    , '' as analysis_cycle
                    from GSP_WEB.Link_Element_TypeA
                    where del_yn = 'N' and dst_columns_name like '%{2}%'
                    union
                    select id, 'B-Type' as source, dst_columns_name as column_name, description as description,
                    '' as src_type, '' as src_columns_name
                    ,use_yn as use_yn, cre_dt as cre_dt, mod_dt as mod_dt
                    , 'TypeB' as ElementType
                    , operate_function as operate_function
                    , timespan
                    , analysis_cycle
                    from GSP_WEB.Link_Element_TypeB
                    where del_yn = 'N' and dst_columns_name like '%{2}%'
                    ) as a order by id desc limit {0}, {1}'''.format(start_idx, pagesize, keyword)

        sql = text(query)
        queryResult = db.engine.execute(sql).fetchall()

        result = list()
        for row in queryResult:
            dictRow = dict()
            for col in row.keys():
                if type(row[col]) is datetime.datetime:
                    dictRow[col] = row[col].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    dictRow[col] = row[col]
            result.append(dictRow)


        self.data = result
        return

    @staticmethod
    def getAnalysisResult( request):
        per_page = int(request.form.get('perpage'))
        start_idx = int(request.form.get('start'))
        src_ip = request.form.get('search_src_ip')
        dst_ip =  request.form.get('search_dst_ip')

        if per_page == None:
            per_page = int(request.form['perpage'])
        if start_idx == None:
            start_idx = int(request.form['start'])
        page_no = int(start_idx / per_page)

        doc = {
            "query": {
                "bool": {

                    "must": [
                    ]
                }
            },
            "size": per_page,
            "from": start_idx
        }


        # flagMatchPhraseListElement = {"match_phrase": {"flag_list" : "5"}}
        # doc["query"]["bool"]["should"] = flagMatchPhraseListElement ##Condition added. it only retrieves elements with flag_list above 5 for better Pie chart display

        if src_ip == '' or dst_ip == '':
            flagMatchPhraseListElement = {"range": {"pkts-dispersion": {"gte": 70}}}
            doc["query"]["bool"]["should"] = flagMatchPhraseListElement ##data is retrieved as to pkts-dispersion over 70

        # sortNode = {"@timestamp": {"order": "desc", "unmapped_type": "date"}}  # sort condition added to sort it by timestamp.
        # sortNode = {"flag_list": {"order": "desc"}}
        # doc["sort"] = sortNode



        if src_ip is not None and src_ip != "":
            sourceNode = {"term": {"src_ip.keyword": src_ip}}
            doc["query"]["bool"]["must"].append(sourceNode)

        if dst_ip is not None and dst_ip != "":
            sourceNode = {"term": {"dst_ip.keyword": dst_ip}}
            doc["query"]["bool"]["must"].append(sourceNode)

        return doc

    @staticmethod
    def getTotalAnalysisResultCount(request): #link count method and query added
        per_page = int(request.form.get('perpage'))
        start_idx = int(request.form.get('start'))
        src_ip = request.form.get('search_src_ip')
        dst_ip = request.form.get('search_dst_ip')

        if per_page == None:
            per_page = int(request.form['perpage'])
        if start_idx == None:
            start_idx = int(request.form['start'])
        page_no = int(start_idx / per_page)

        doc = {
            "query": {
                "bool": {

                    "must": [
                    ]
                }
            }
            #"size": per_page
            #"from": start_idx
        }

        # flagMatchPhraseListElement = {"match_phrase": {"flag_list": "5"}}
        # doc["query"]["bool"][
        #     "should"] = flagMatchPhraseListElement  ##Condition added. it only retrieves elements with flag_list above 5 for better Pie chart display

        if src_ip is not None and src_ip != "":
            sourceNode = {"term": {"src_ip.keyword": src_ip}}
            doc["query"]["bool"]["must"].append(sourceNode)

        if dst_ip is not None and dst_ip != "":
            sourceNode = {"term": {"dst_ip.keyword": dst_ip}}
            doc["query"]["bool"]["must"].append(sourceNode)

        return doc