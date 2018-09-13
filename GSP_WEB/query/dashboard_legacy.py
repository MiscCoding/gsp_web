
def getTopBoardTotalQuery(timespan):
    query = {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        }
    }
    return query

def getTopBoardQuery(timespan):
    query = {
        "size": 0,
        "aggs": {
            "securitylevel" :{
                "range" : {
                    "field" :"security_level",
                    "ranges" : [
                        {"to" : 3, "key" : "normal"},
                        {"from" : 4, "key" : "danger"}
                    ]
                }
            }
        },
        "query" : {
            "range" : {
                "@timestamp" : {
                    "gte" : "now-"+timespan,
                    "lt" : "now"
                }
            }
        }
    }
    return query


def getWorldChartQuery(timespan, security_level):
    query = {
		"size" : 0,
		"query": {
			"bool": {
				"must": [
					{
						"range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
					},
					{
						"range" :{ "security_level" : { "gte" : security_level } }
					}
				]
			}
		},
		"aggregations" :{
			"group_by_country2" : {
				"terms" : {
					"field" : "dst_geoip.country_code2.keyword"
				}
			}
		}

	}
    return query

def getAnalysisCountQuery(timefrom):
    doc = {
        "size": 0,
        "aggs": {
            "seruitylevel": {
                "range": {
                    "field": "security_level",
                    "ranges": [
                        {"to": 3},
                        {"from": 4}
                    ]
                }
            }
        },
        "query": {
            "range": {
                "@timestamp": {
                    "gte": timefrom,
                    "lt": "now"
                }
            }
        }
    }
    return doc

def getTop10SendBytes(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"send_bytes": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
        	,"avg" : { "avg" : { "field" : "send_bytes" } }
            , "ex_stats": {"extended_stats": {"field": "send_bytes"}}
        }
    }
    return doc

def getTop10RecvBytes(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"recv_bytes": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "recv_bytes"}}
            , "ex_stats": {"extended_stats": {"field": "recv_bytes"}}
        }
    }
    return doc

def getTop10SendPkts(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"send_pkts": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "send_pkts"}}
            , "ex_stats": {"extended_stats": {"field": "send_pkts"}}
        }
    }
    return doc

def getTop10RecvPkts(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"recv_pkts": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "recv_pkts"}}
            , "ex_stats": {"extended_stats": {"field": "recv_pkts"}}
        }
    }
    return doc

def getTop10SessionTime(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"differ_time": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "differ_time"}}
            , "ex_stats": {"extended_stats": {"field": "differ_time"}}
        }
    }
    return doc

def getTop10SessionCount(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"session_cnt": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "session_cnt"}}
            , "ex_stats": {"extended_stats": {"field": "session_cnt"}}
        }
    }
    return doc

def getTop10ServerCon(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"cnt": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "cnt"}}
            , "ex_stats": {"extended_stats": {"field": "cnt"}}
        }
    }
    return doc

def getTop10ClientCon(timespan):
    doc= {
        "size": 0,
        "query": {
	        "bool": {
	            "must": [
	            	{
	                    "range" :{ "@timestamp" : { "gte" : "now-"+timespan, "lte" : "now" } }
	                }
	            ]
	        }
        },
        "aggs" :{
        	"topn" : {
        		"top_hits" : {
        			"sort": [
        				{
        					"cnt": {
        						"order" : "desc"
        						}
        				}
						],
						"size" : 10
        		}
        	}
            , "avg": {"avg": {"field": "cnt"}}
            , "ex_stats": {"extended_stats": {"field": "cnt"}}
        }
    }
    return doc