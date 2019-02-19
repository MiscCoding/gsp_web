from datetime import datetime
from elasticsearch import Elasticsearch
from dateutil import parser

from GSP_WEB import db, app
from GSP_WEB.models.CommonCode import CommonCode
import json

class Rules_Crawl():

    def __init__(self):
        self._index = app.config['ELASTICSEARCH_INDEX']
        self._type = "url_jobs"
        self._id = ""
        self.src_ip = ""
        self.dst_ip = ""
        self.uri = ""
        self.domain = ""
        self.isCrawled = 0
        self.depth = 3
        self.src_geoip = {}
        self.dst_geoip = {}
        self.desc = ""
        self.register_path = ""
        self.data_type = "user_define"

    @staticmethod
    def getList(elsaticQuery, request):
        es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
        per_page = int(request.form.get('perpage'))
        start_idx = int(request.form.get('start'))
        search_source = request.form.get('search_source')
        keyword = request.form.get('search_keyword').strip()
        str_dt = "";
        end_dt = "";

        if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
            str_dt = parser.parse(request.form['timeFrom']).strftime("%Y-%m-%dT%H:%M:%S") #str_dt = parser.parse(request.form['timeFrom']).isoformat()
        else:
            str_dt = parser.parse(datetime.now.strftime("%Y-%m-%dT%H:%M:%S")) #str_dt = parser.parse(datetime.utcnow().strftime("%Y-%m-%d %H:%M")).isoformat();

        if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
            end_dt = parser.parse(request.form['timeTo']).strftime("%Y-%m-%dT%H:%M:%S") #end_dt = parser.parse(request.form['timeTo']).isoformat()
        else:
            end_dt = parser.parse(datetime.now.strftime("%Y-%m-%dT%H:%M:%S")) #end_dt = parser.parse(datetime.utcnow().strftime("%Y-%m-%d %H:%M")).isoformat();

        crawls = Rules_Crawl()
        if per_page == None:
            per_page = int(request.form['perpage'])
        if start_idx == None:
            start_idx = int(request.form['start'])
        page_no = int(start_idx / per_page)

        # "range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}
        try:
            doc = {
                "size": per_page,
                "from": start_idx,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {"min_timestamp": {"gte": str_dt, "lte": end_dt}}
                            }
                        ]
                    }
                }
            }
            jsonDic = json.dumps(doc)
            if keyword != "":
                keywordNode = {"wildcard": {"uri": "*" + keyword + "*"}}
                doc["query"]["bool"]["must"].append(keywordNode)
            if search_source != "":
                sourceNode = { "term" : { "register_path" : search_source } }
                doc["query"]["bool"]["must"].append(sourceNode)

            result = es.search(index=elsaticQuery, doc_type=crawls._type, body=doc, request_timeout=60)

        except Exception as e:
            raise e
        return result;

    @staticmethod
    def getCrawlCountDashboard(today=False):

        # end_dt = "now/d"
        # str_dt = "now-1d/d"
        end_dt = "now"
        str_dt = "now/d"

        query = {
            "query": {
                "bool": {
                    "must": [
                        {

                        }

                    ],
                    "should": [

                    ]

                }

            }

        }

        if today is True:
            timeQuery = {"range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}}
            query["query"]["bool"]["must"].append(timeQuery)

        return query

    @staticmethod
    def urlCollectionStatisticsByDailyAggregation(query_type="", days=1):
        end_dt = "now/d"
        str_dt = "now-{}d/d".format(days)

        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [

                    ],
                    "should": [

                    ]

                }

            },
            "aggs": {
                "byday": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "interval": "day"
                    }
                }
            }

        }

        if days is not None:
            timeQuery = {"range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}}
            query["query"]["bool"]["must"].append(timeQuery)

        if (query_type != ""):
            sourceNode = {"term": {"_type": query_type}}
            query["query"]["bool"]["must"].append(sourceNode)



        return query



    @staticmethod
    def insertData(urlCrawl ):
        es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
        doc = {
            'src_ip': urlCrawl.src_ip
            , 'dst_ip': urlCrawl.dst_ip
            , 'uri': urlCrawl.uri
            , 'domain': urlCrawl.domain
            , 'isCrawled': urlCrawl.isCrawled
            , 'depth': urlCrawl.depth
            , 'src_geoip': urlCrawl.src_geoip
            , 'dst_geoip': urlCrawl.dst_geoip
            , 'desc': urlCrawl.desc
            , 'register_path': urlCrawl.register_path
            , '@timestamp': datetime.utcnow().isoformat()
            , 'min_timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        }
        urlCrawl._index = 'gsp-{0}'.format(datetime.now().strftime("%Y.%m.%d"))
        es.index(index=urlCrawl._index, doc_type=urlCrawl._type, body=doc)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    @staticmethod
    def deleteData(urlCrawl, dataDate, u_id):
        es = Elasticsearch([{'host': app.config['ELASTICSEARCH_URI'], 'port': app.config['ELASTICSEARCH_PORT']}])
        # doc = {
        #     'src_ip': urlCrawl.src_ip
        #     , 'dst_ip': urlCrawl.dst_ip
        #     , 'uri': urlCrawl.uri
        #     , 'domain': urlCrawl.domain
        #     , 'isCrawled': urlCrawl.isCrawled
        #     , 'depth': urlCrawl.depth
        #     , 'src_geoip': urlCrawl.src_geoip
        #     , 'dst_geoip': urlCrawl.dst_geoip
        #     , 'desc': urlCrawl.desc
        #     , 'register_path': urlCrawl.register_path
        #     , '@timestamp': datetime.utcnow().isoformat()
        #     , 'min_timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        #
        # }
        dataindex = 'gsp-{0}'.format(dataDate)
        #.format(datetime.now().strftime("%Y.%m.%d"))
        try:
            es.delete(index=dataindex, doc_type="url_jobs", id=u_id)
        # delete(self, index, doc_type, id, params=None)
        except Exception as e:
            raise e

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

