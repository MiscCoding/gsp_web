from GSP_WEB import app
from GSP_WEB.common.util.date_util import Local2UTC
from datetime import datetime, timedelta
from dateutil import parser

from GSP_WEB.models.CommonCode import CommonCode


def getCncLogQueryCountFileAnalysisStatus(request,query_type):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    # if per_pageP is None:
    #     per_page = int(request.form['perpage'])
    # else:
    #     per_page = per_pageP if per_pageP <= 10000 else 10000

    start_idx = int(request.form['start'])

    query = {
        # "size": per_page,
        # "from": start_idx,
        "query": {
            "bool": {
                "must": [
                    {

                        "range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}
                    },
                    {
                        "term": {"analysis_type": query_type}
                    }
                    # ,

                ]
            }
        }
        # , "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "date"}}]
    }

    # typeQuery = {"range": {"security_level": {"gte": 4}}}
    # query["query"]["bool"]["must"].append(typeQuery)
    search_type = request.form.get("search_type")
    if search_type is not None and search_type != "":
        type = CommonCode.query.filter_by(GroupCode='an_data_from').filter_by(Code=search_type).first()
        keywordQuery = {"term": {"data_from.keyword": type.EXT1}}
        query["query"]["bool"]["must"].append(keywordQuery)

    search_security_level = request.form.get("search_security_level")
    if search_security_level is not None and search_security_level != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level == "1" else ""
        if search_security_level == "1":
            secQuery = {"range": {"security_level": {"gte": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
            query["query"]["bool"]["must"].append(secQuery)
        else:
            secQuery = {"range": {"security_level": {"lt": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
            query["query"]["bool"]["must"].append(secQuery)

    search_keyword = request.form.get('search_keyword').strip()  # request.form['search_keyword'] # search does not happen here. it will be done in a higher python layer.
    if search_keyword != '':

        search_keyword_type = request.form['search_keyword_type']

        if search_type == '001' or search_type == '003':
            search_keyword_type = "collect_uri"
        keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
        query["query"]["bool"]["must"].append(keywordQuery)

    # match is replaced with "match_phrase" at Aug. 8th, 2018

    return query





def getCncLogQueryURLCount(request,query_type):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    # if per_pageP is None:
    #     per_page = int(request.form['perpage'])
    # else:
    #     per_page = per_pageP

    start_idx = int(request.form['start'])

    query = {
        # "size" : per_page,
        # "from" : start_idx,
		"query": {
			"bool": {
				"must": [
					{


                        "range" :{ "@timestamp" : { "gte" : str_dt, "lte" : end_dt } }
					},
                    {
                        "term" : { "analysis_type" : query_type}
                    }
                    #,

				]
			}
		}
       # , "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "date"}}]
	}

    search_keyword_type = request.form['search_type']
    if search_keyword_type != '':
        if search_keyword_type == '001':
            search_keyword = "NPC"
        elif search_keyword_type == '002':
            search_keyword = "IMAS"

        search_keyword_type = "data_from"

        keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
        query["query"]["bool"]["must"].append(keywordQuery)

    search_security_level = request.form.get("search_security_level")
    if search_security_level is not None and search_security_level != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level == "1" else ""
        if search_security_level == "1":
            secQuery = {"range": {"security_level": {"gte" : int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']) } }}
            query["query"]["bool"]["must"].append(secQuery)
        else:
            secQuery = {"range": {"security_level": {"lt": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
            query["query"]["bool"]["must"].append(secQuery)

    search_keyword_type = 'uri'
    search_keyword = request.form['search_keyword']
    if search_keyword != '':
        keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
        query["query"]["bool"]["must"].append(keywordQuery)

    return query


def getCncLogQueryURL(request,query_type, per_pageP=None):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    if per_pageP is None:
        per_page = int(request.form['perpage'])
    else:
        per_page = per_pageP if per_pageP <= 10000 else 10000

    start_idx = int(request.form['start'])

    query = {
		"size" : per_page,
        "from" : start_idx,
		"query": {
			"bool": {
				"must": [
					{


                        "range" :{ "@timestamp" : { "gte" : str_dt, "lte" : end_dt } }
					},
                    {
                        "term" : { "analysis_type" : query_type}
                    }
                    #,

				]
			}
		}
       # , "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "date"}}]
	}

    search_keyword_type = request.form['search_type']
    if search_keyword_type != '':
        if search_keyword_type == '001':
            search_keyword = "NPC"
        elif search_keyword_type == '002':
            search_keyword = "IMAS"

        search_keyword_type = "data_from"

        keywordQuery = { "match_phrase" : { search_keyword_type : search_keyword } }
        query["query"]["bool"]["must"].append(keywordQuery)

    search_security_level = request.form.get("search_security_level")
    if search_security_level is not None and search_security_level != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level == "1" else ""
        if search_security_level == "1":
            secQuery = {"range": {"security_level": {"gte" : int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']) } }}
            query["query"]["bool"]["must"].append(secQuery)
        else:
            secQuery = {"range": {"security_level": {"lt": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
            query["query"]["bool"]["must"].append(secQuery)

    search_keyword_type = 'uri'
    search_keyword = request.form['search_keyword']
    if search_keyword != '':

        keywordQuery = { "match_phrase" : { search_keyword_type : search_keyword } }
        query["query"]["bool"]["must"].append(keywordQuery)



    return query


def getCncLogQuery(request,query_type, per_pageP=None):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    if per_pageP is None:
        per_page = int(request.form['perpage'])
    else:
        per_page = per_pageP if per_pageP <= 10000 else 10000


    start_idx = int(request.form['start']) # must is changed to should on Aug. 8th, 2018



    query = {
		"size" : per_page,
        "from" : start_idx,
		"query": {
			"bool": {
				"must": [
					{


                        "range" :{ "@timestamp" : { "gte" : str_dt, "lte" : end_dt } }
					},
                    {
                        "term" : { "analysis_type" : query_type}
                    }


				],
                "should" : [

                ]



			}
		}
       # , "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "date"}}]
	}

    #typeQuery = {"range": {"security_level": {"gte": 4}}}
    #query["query"]["bool"]["must"].append(typeQuery)
    search_type = request.form.get("search_type")
    if search_type is not None and search_type != "":
        type = CommonCode.query.filter_by(GroupCode='an_data_from').filter_by(Code=search_type).first()
        keywordQuery = {"term": { "data_from.keyword": type.EXT1}}
        query["query"]["bool"]["must"].append(keywordQuery)

    search_security_level = request.form.get("search_security_level")
    if search_security_level is not None and search_security_level != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level == "1" else ""
        if search_security_level == "1":
            secQuery = {"range": {"security_level": {"gte" : int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN']) } }}
            query["query"]["bool"]["must"].append(secQuery)
        else:
            secQuery = {"range": {"security_level": {"lt": int(app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'])}}}
            query["query"]["bool"]["must"].append(secQuery)

    search_keyword = request.form.get('search_keyword').strip() #request.form['search_keyword'] # search does not happen here. it will be done in a higher python layer.

    ##-------------------------------------------------------------------------------
    # if search_keyword != '':
    #     search_keyword_type = request.form['search_keyword_type']
    #
    #     if (search_type == '001' or search_type == '003') and search_keyword_type=="uri":
    #         search_keyword_type = "collect_uri"
    #         keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
    #         query["query"]["bool"]["must"].append(keywordQuery)
    #     elif search_type == '002' and search_keyword_type=="uri":
    #         search_keyword_type = "uri"
    #         keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
    #         query["query"]["bool"]["must"].append(keywordQuery)
    #
    #     elif search_keyword_type=="uri":
    #         search_keyword_type = "uri"
    #
    #         keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
    #         query["query"]["bool"]["should"].append(keywordQuery)
    #
    #         search_keyword_type = "collect_uri"
    #         keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
    #         query["query"]["bool"]["should"].append(keywordQuery)
    #
    #     elif search_keyword_type=="md5":
    #         search_keyword_type = "md5"
    #         keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
    #         wildCard = {"wildcard": {search_keyword_type: "*"+ search_keyword + "*"}}
    #         query["query"]["bool"]["must"].append(keywordQuery)
    #         query["query"]["bool"]["must"][2]=(wildCard)
    ##-------------------------------------------------------------------------------
        # match is replaced with "match_phrase" on Aug. 8th, 2018

    #test
    if search_keyword != '':
        search_keyword_type = request.form['search_keyword_type']

        if (search_type == '001' or search_type == '003') and search_keyword_type=="uri":
            search_keyword_type = "collect_uri"
            keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
            wildCard = {"wildcard": {search_keyword_type: "*" + search_keyword + "*"}}
            query["query"]["bool"]["must"].append(keywordQuery)
            #query["query"]["bool"]["must"][2] = (wildCard)

        elif search_type == '002' and search_keyword_type=="uri":
            search_keyword_type = "uri"
            keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
            wildCard = {"wildcard": {search_keyword_type: "*" + search_keyword + "*"}}
            query["query"]["bool"]["must"].append(keywordQuery)
            #query["query"]["bool"]["must"][2] = (wildCard)


        # elif search_keyword_type=="uri":
        #     search_keyword_type = "uri"
        #
        #     keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
        #     wildCard = {"wildcard": {search_keyword_type: "*" + search_keyword + "*"}}
        #     query["query"]["bool"]["should"].append(wildCard)
        #
        #     search_keyword_type = "collect_uri"
        #     keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
        #     wildCard = {"wildcard": {search_keyword_type: "*" + search_keyword + "*"}}
        #     query["query"]["bool"]["should"].append(wildCard)


        elif search_keyword_type=="md5":
            search_keyword_type = "md5"
            keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
            wildCard = {"wildcard": {search_keyword_type: "*"+ search_keyword + "*"}}
            query["query"]["bool"]["must"].append(wildCard)
           # query["query"]["bool"]["must"][2]=(wildCard)
    #-------------------------------------------------------------------------------

    return query

def getMaliciousCodeStatisticsDataCountAggsByDays(query_type="", days=1, detectedMalFileCount = 'no'):
    # end_dt = "now/d"
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
                    "field": "kor_timestamp",
                    "interval": "day"
                }
            }
        }

    }

    if days is not None:
        timeQuery = {"range": {"kor_timestamp": {"gte": str_dt, "lte": end_dt}}}
        query["query"]["bool"]["must"].append(timeQuery)

    if (query_type != ""):
        if app.config["NEW_ES"]:
            pass
            # sourceNode = { "match_all": {} }
            # query["query"]["bool"]["must"].append(sourceNode)
        else:
            sourceNode = {"term": {"_type": query_type}}
            query["query"]["bool"]["must"].append(sourceNode)

    if detectedMalFileCount == "yes":
        sourceNode = {"range": {"detect_cnt_file": {"gte": "1" }}}
        query["query"]["bool"]["must"].append(sourceNode)

    return query

def initializationMaxWindowQuery(maxWindow = 500000):
    query = {
        "max_result_window" : maxWindow
    }
    return query


def getMaliciousCodeLogData(request,query_type, per_pageP=None):
    str_dt = ""
    end_dt = ""

    columnIndex = request.form.get('columnIndex')
    sort_style = request.form.get('sort_style')

    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    if per_pageP is None:
        per_page = int(request.form['perpage'])
    else:
        per_page = per_pageP if per_pageP <= 10000 else 10000


    start_idx = int(request.form['start']) # must is changed to should on Aug. 8th, 2018

    if app.config["NEW_ES"]:
        query = {
            "size": per_page,
            "from": start_idx,
            "query": {
                "bool": {
                    "must": [
                        {

                            "range": {"kor_timestamp": {"gte": str_dt, "lte": end_dt}}
                        }


                    ],
                    "should": [

                    ]

                }
                # ,
                # "wildcard":
                # {
                #
                # }
            }
            , "sort": [
                # {"@timestamp": {"order": "desc", "unmapped_type": "date"}}
            ]
        }

    else:
        query = {
            "size": per_page,
            "from": start_idx,
            "query": {
                "bool": {
                    "must": [
                        {

                            "range": {"kor_timestamp": {"gte": str_dt, "lte": end_dt}}
                        },
                        {
                            "term": {"_type": query_type}
                        }

                    ],
                    "should": [

                    ]

                }
                # ,
                # "wildcard":
                # {
                #
                # }
            }
            , "sort": [
                # {"@timestamp": {"order": "desc", "unmapped_type": "date"}}
            ]
        }




    if columnIndex == "kor_timestamp" and sort_style:
        sortContent = {columnIndex : {"order" : sort_style, "unmapped_type" : "date" }}
    elif (columnIndex == "detect_cnt_url" or columnIndex == "detect_cnt_file") and sort_style:
        sortContent = {columnIndex: {"order": sort_style, "unmapped_type": "integer"}}
    elif columnIndex != "default" and sort_style != "default":
        sortContent = {columnIndex: {"order": sort_style, "unmapped_type": "text"}}
    else:
        sortContent = {"kor_timestamp" : {"order" : "desc", "unmapped_type" : "date" }}

    query["sort"].append(sortContent)




    #typeQuery = {"range": {"security_level": {"gte": 4}}}
    #query["query"]["bool"]["must"].append(typeQuery)
    # search_type = request.form.get("search_type")
    # if search_type is not None and search_type != "":
    #     type = CommonCode.query.filter_by(GroupCode='an_data_from').filter_by(Code=search_type).first()
    #     keywordQuery = {"term": { "data_from.keyword": type.EXT1}}
    #     query["query"]["bool"]["must"].append(keywordQuery)

    search_security_level_file = request.form.get("search_security_level_file")
    if search_security_level_file is not None and search_security_level_file != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level_file == "1" else ""
        if search_security_level_file == "1":
            secQuery = {"range": {"detect_cnt_file": {"gte" : search_security_level_file } }}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_file == "2":
            secQuery = {"term": {"status_file": "analyzing"}}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_file == "0":
            secQuery = {"term": {"detect_cnt_file": 0}}
            thrdQuery = {"term": {"status_file": "finish"}}
            query["query"]["bool"]["must"].append(secQuery)
            query["query"]["bool"]["must"].append(thrdQuery)
        else:
            pass


    search_security_level_uri = request.form.get("search_security_level_url")
    if search_security_level_uri is not None and search_security_level_uri != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level_uri == "1" else ""
        if search_security_level_uri == "1":
            secQuery = {"range": {"detect_cnt_url": {"gte" : search_security_level_uri } }}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_uri == "2":
            secQuery = {"term": {"status_url": "analyzing"}}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_uri == "0":
            secQuery = {"term": {"detect_cnt_url": 0}}
            thrdQuery = {"term": {"status_url": "finish"}}
            query["query"]["bool"]["must"].append(secQuery)
            query["query"]["bool"]["must"].append(thrdQuery)
        else:
            pass
        # if search_security_level_uri == "1":
        #     secQuery = {"range": {"detect_cnt_url": {"gte": search_security_level_uri}}}
        #     query["query"]["bool"]["must"].append(secQuery)
        # else:
        #     secQuery = {"range": {"detect_cnt_url": {"lt": search_security_level_uri}}}
        #     query["query"]["bool"]["must"].append(secQuery)

    search_keyword = request.form.get('search_keyword').strip() #request.form['search_keyword'] # search does not happen here. it will be done in a higher python layer.


    if search_keyword != '':
        search_keyword_type = str(request.form['search_keyword_type'])
        wild_card = str(request.form['wild_card'])
        if wild_card == 'false':
            keywordQuery = {"match": {search_keyword_type : {"query" : search_keyword, "type" : "phrase"}}}
            query["query"]["bool"]["must"].append(keywordQuery)
        elif wild_card == 'true':
            wildcard_query = {"wildcard":{search_keyword_type : str(search_keyword)}}
            query["query"]["bool"]["must"].append(wildcard_query)

            # keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
            # wildCard = {"wildcard": {search_keyword_type: "*" + search_keyword + "*"}}
            # query["query"]["bool"]["must"].append(keywordQuery)
            #query["query"]["bool"]["must"][2] = (wildCard)
    #-------------------------------------------------------------------------------

    return query


def getMaliciousCodeLogDataCountDashboard(query_type, today=False):
    nowtime = datetime.now()
    start_of_day = datetime(nowtime.year, nowtime.month, nowtime.day)

    if app.config["NEW_ES"]:
        query = {
            "query": {
                "bool": {
                    "must": [
                            {
                                "match_all": {}
                            }
                    ],

                    "should": [

                    ]

                }

            }

        }
    else:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {



                        },
                        {
                            "term" : { "_type" : query_type}
                        }


                    ],
                    "should" : [

                    ]



                }

            }

        }


    if today is True:
        timeQuery = {"range" : {"@timestamp": {"gte": start_of_day, "lte": nowtime}}}
        query["query"]["bool"]["must"].append(timeQuery)


    return query


def getMaliciousCodeLogDetailData(request,query_type):

     # must is changed to should on Aug. 8th, 2018
    _id = request.form.get('_id');

    query = {
		"query": {
			"bool": {
				"must": [

				]
			}
		}
	}

    if app.config["NEW_ES"]:
        secQuery = {"match": {"analysis_info_id": {"query": _id}}}
    else:
        secQuery = {"match": {"analysis_info_id": {"query": _id, "type": "phrase"}}}


    query["query"]["bool"]["must"].append(secQuery)

    return query


def updateCommentQuery(request, query_type):

    _id = request.form.get('_id')
    comment = request.form.get('comment')


    query = {
        "doc" : {
            "comment" : comment
        }
    }
    # secQuery = {"match": {"analysis_info_id": {"query": _id, "type": "phrase"}}}
    # query["query"]["bool"]["must"].append(secQuery)



    return query


def reanalysisRequestQuery(request, query_type):

    #_id = request.form.get('_id')
    #comment = "reanalysis"


    query = {
        "doc" : {
            "request": "reanalysis"
        }
    }
    # secQuery = {"match": {"analysis_info_id": {"query": _id, "type": "phrase"}}}
    # query["query"]["bool"]["must"].append(secQuery)



    return query


def deleteSingleItemQuery(request, query_type):

    _id = request.form.get('_id')
    comment = request.form.get('comment')


    query = {
        "doc" : {
            "comment" : comment
        }
    }
    # secQuery = {"match": {"analysis_info_id": {"query": _id, "type": "phrase"}}}
    # query["query"]["bool"]["must"].append(secQuery)



    return query


def getMaliciousCodeLogDataCount(request,query_type, per_pageP=None):
    str_dt = ""
    end_dt = ""
    if request.form.get('timeFrom') is not None and request.form.get('timeFrom') != "":
        str_dt = parser.parse(request.form['timeFrom']).isoformat()
    if request.form.get('timeTo') is not None and request.form['timeTo'] != "":
        end_dt = parser.parse(request.form['timeTo']).isoformat()

    if per_pageP is None:
        per_page = int(request.form['perpage'])
    else:
        per_page = per_pageP if per_pageP <= 10000 else 10000


    start_idx = int(request.form['start']) # must is changed to should on Aug. 8th, 2018




    query = {

		"query": {
			"bool": {
				"must": [
					{


                        "range" :{ "kor_timestamp" : { "gte" : str_dt, "lte" : end_dt } }
					},
                    {
                        "term" : { "_type" : query_type}
                    }


				],
                "should" : [

                ]



			}
            # ,
            # "wildcard":
            # {
            #
            # }
		}
    # ,"sort": [{"@timestamp": {"order": "desc", "unmapped_type": "date"}}]
	}

    #typeQuery = {"range": {"security_level": {"gte": 4}}}
    #query["query"]["bool"]["must"].append(typeQuery)
    # search_type = request.form.get("search_type")
    # if search_type is not None and search_type != "":
    #     type = CommonCode.query.filter_by(GroupCode='an_data_from').filter_by(Code=search_type).first()
    #     keywordQuery = {"term": { "data_from.keyword": type.EXT1}}
    #     query["query"]["bool"]["must"].append(keywordQuery)

    search_security_level_file = request.form.get("search_security_level_file")
    if search_security_level_file is not None and search_security_level_file != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level_file == "1" else ""
        if search_security_level_file == "1":
            secQuery = {"range": {"detect_cnt_file": {"gte" : search_security_level_file } }}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_file == "2":
            secQuery = {"term": {"status_file": "analyzing"}}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_file == "0":
            secQuery = {"term": {"detect_cnt_file": 0}}
            thrdQuery = {"term": {"status_file": "finish"}}
            query["query"]["bool"]["must"].append(secQuery)
            query["query"]["bool"]["must"].append(thrdQuery)
        else:
            pass


    search_security_level_uri = request.form.get("search_security_level_url")
    if search_security_level_uri is not None and search_security_level_uri != "":
        security_level = app.config['ANALYSIS_RESULTS_SECURITY_LEVEL_MIN'] if search_security_level_uri == "1" else ""
        if search_security_level_uri == "1":
            secQuery = {"range": {"detect_cnt_url": {"gte" : search_security_level_uri } }}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_uri == "2":
            secQuery = {"term": {"status_url": "analyzing"}}
            query["query"]["bool"]["must"].append(secQuery)
        elif search_security_level_uri == "0":
            secQuery = {"term": {"detect_cnt_url": 0}}
            thrdQuery = {"term": {"status_url": "finish"}}
            query["query"]["bool"]["must"].append(secQuery)
            query["query"]["bool"]["must"].append(thrdQuery)
        else:
            pass
        # if search_security_level_uri == "1":
        #     secQuery = {"range": {"detect_cnt_url": {"gte": search_security_level_uri}}}
        #     query["query"]["bool"]["must"].append(secQuery)
        # else:
        #     secQuery = {"range": {"detect_cnt_url": {"lt": search_security_level_uri}}}
        #     query["query"]["bool"]["must"].append(secQuery)

    search_keyword = request.form.get('search_keyword').strip() #request.form['search_keyword'] # search does not happen here. it will be done in a higher python layer.


    if search_keyword != '':
        search_keyword_type = str(request.form['search_keyword_type'])
        wild_card = str(request.form['wild_card'])
        if wild_card == 'false':
            keywordQuery = {"match": {search_keyword_type : {"query" : search_keyword, "type" : "phrase"}}}
            query["query"]["bool"]["must"].append(keywordQuery)
        elif wild_card == 'true':
            wildcard_query = {"wildcard":{search_keyword_type : str(search_keyword)}}
            query["query"]["bool"]["must"].append(wildcard_query)

            # keywordQuery = {"match_phrase": {search_keyword_type: search_keyword}}
            # wildCard = {"wildcard": {search_keyword_type: "*" + search_keyword + "*"}}
            # query["query"]["bool"]["must"].append(keywordQuery)
            #query["query"]["bool"]["must"][2] = (wildCard)
    #-------------------------------------------------------------------------------

    return query