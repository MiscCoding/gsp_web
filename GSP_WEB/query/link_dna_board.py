#-*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

from GSP_WEB import app

class link_dna_board:

    @staticmethod
    def getList(indexName, request):
        es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
        per_page = int(request.form.get('perpage'))
        start_idx = int(request.form.get('start'))

        if per_page == None:
            per_page = int(request.form['perpage'])
        if start_idx == None:
            start_idx = int(request.form['start'])
        page_no = int(start_idx / per_page)

        try:
            doc = {
                "query": {
                    "bool": {
                        "must": [
                        ]
                    }
                },
                "size": per_page,
                "from" :  page_no
            }
            
            #검색 조건 적용
            if request.form.get('search_src_ip') is not None and request.form.get('search_src_ip') != '':
                doc["query"]["bool"]["must"].append({
					"term" : {"src_ip.keyword" : request.form.get('search_src_ip') }
				})

            if request.form.get('search_dst_ip') is not None and request.form.get('search_dst_ip') != '':
                doc["query"]["bool"]["must"].append({
                    "term": {"dst_ip.keyword": request.form.get('search_dst_ip')}
                })

            result = es.search(index=indexName, doc_type="link_dna", body=doc, request_timeout=30)

        except Exception as e:
            raise e
        return result;