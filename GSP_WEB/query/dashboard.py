#-*- coding: utf-8 -*-
topboardQuery = \
u"""
select MID(cnc.cre_dt,1,10) as date, count(cnc.seq) as count, code.EXT1 as type, code.Code as Code
    from GSP_WEB.Rules_CNC as cnc
    left join GSP_WEB.ca100 as code
    on cnc.rule_type = code.idx
    where MID(cnc.cre_dt,1,10) = MID(now(),1,10)
    group by MID(cnc.cre_dt,1,10), cnc.rule_type
    union
    select  MID(cre_dt,1,10) as date,count(seq) as count, '악성 코드' as type, '-' as Code
    from GSP_WEB.Rules_BlackList
    where MID(cre_dt,1,10) = MID(now(),1,10)
    group by MID(cre_dt,1,10)
union
select MID(cnc.cre_dt,1,10) as date, count(cnc.seq) as count, code.EXT1 as type, code.Code as Code
    from GSP_WEB.Rules_CNC as cnc
    left join GSP_WEB.ca100 as code
    on cnc.rule_type = code.idx
    where MID(cnc.cre_dt,1,10) = MID(date_add(now(), interval -1 day),1,10)
    group by MID(cnc.cre_dt,1,10), cnc.rule_type
    union
    select  MID(cre_dt,1,10) as date,count(seq) as count, '악성 코드' as type, '-' as Code
    from GSP_WEB.Rules_BlackList
    where MID(cre_dt,1,10) = MID(date_add(now(), interval -1 day),1,10)
    group by MID(cre_dt,1,10)
"""
def yesterdayUrlFileAnalysis(request, query_type):
    per_page = 1
    start_idx = 0
    end_dt = "now-1d/d"
    str_dt = "now-2d/d"

    # "now-1d/d", "now/d"

    query = {
        "size": per_page,
        "from": start_idx,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}
                    }, {
                        "term": {"analysis_type": query_type}
                    }

                ]
            }
        }
    }

    return query


def topboardEsQuery(dateFrom, dateTo):
    query = {
        "size": 0,
        "query":
            {
                "bool": {
                    "must": [
                        {"range": {"@timestamp": {
							"gt": dateFrom,
							"lte": dateTo
						}}}]
                }

            },
        "aggs": {
            "types": {
                "terms": {"field": "_type"}
            }
        }
    }

    return query



def DashboardTotalLinkCount(field,today=False):

        end_dt = "now/d"
        str_dt = "now-1d/d"

        query = {
            "query": {
                "bool": {
                    "must": [


                    ],
                    "should": [

                    ]

                }

            }

        }

        if today is True:
            timeQuery = {"range": {"@timestamp": {"gte": str_dt, "lte": end_dt}}}
            query["query"]["bool"]["must"].append(timeQuery)


        if (field != ""):
            sourceNode = {"exists": {"field" : field}}
            query["query"]["bool"]["must"].append(sourceNode)


        return query


linechartQuery = \
u"""
select a.date, a.count, a.type, a.Code from
(
select MID(cnc.cre_dt,1,10) as date, count(cnc.seq) as count, code.EXT1 as type, code.Code as Code
    from GSP_WEB.Rules_CNC as cnc
    left join GSP_WEB.ca100 as code
    on cnc.rule_type = code.idx
    where cnc.cre_dt > date_add(now(), interval -30 day)
    group by MID(cnc.cre_dt,1,10), cnc.rule_type
union
select  MID(cre_dt,1,10) as date,count(seq) as count, '악성 코드' as type, '-' as Code
from GSP_WEB.Rules_BlackList
where cre_dt > date_add(now(), interval -30 day) 
group by MID(cre_dt,1,10)
) as a
order by a.date, a.type;
"""

barchartQuery = \
"""
select a.date, sum(a.count) as count from
(
	select MID(cre_dt,1,10) as date, count(seq) as count, 'etc' as t
	from GSP_WEB.Rules_CNC as cnc
	where cre_dt > date_add(now(), interval -30 day) 
	group by MID(cre_dt,1,10)
	union
	select  MID(cre_dt,1,10) as date,count(seq) as count, 'black' as t
	from GSP_WEB.Rules_BlackList
	where cre_dt > date_add(now(), interval -30 day) 
	group by MID(cre_dt,1,10)
) as a
group by a.date
order by a.date;
"""

gridQuery = \
u"""
select date
,cast(sum(IF( code ='001', count, 0)) as UNSIGNED) as 'C&C 서버'
,cast(sum(IF( code ='003', count, 0)) as UNSIGNED) as '악성코드 유포지'
,cast(sum(IF( code ='-', count, 0) ) as UNSIGNED) as '악성코드'
from
(
	select MID(cnc.cre_dt,1,7) as date, count(cnc.seq) as count, code.EXT1 as type, code.CODE as code
		from GSP_WEB.Rules_CNC as cnc
		left join GSP_WEB.ca100 as code
		on cnc.rule_type = code.idx
		where cnc.cre_dt > date_add(now(), interval -3 month)
		group by MID(cnc.cre_dt,1,7), cnc.rule_type
	union
	select MID(cnc.cre_dt,1,7) as date, count(cnc.seq) as count,  '악성코드', '-' as code
	from GSP_WEB.Rules_BlackList as cnc
	where cnc.cre_dt > date_add(now(), interval -3 month)
	group by MID(cnc.cre_dt, 1, 7)
) as a
group by date
order by date desc
"""

def getWorldChartQuery(str_dt, ed_dt, security_level):
    query = {
		"size" : 0,
		"query": {
			"bool": {
				"must": [
					{
						"range" :{ "@timestamp" : {
							"gte" : str_dt
							, "lte" : ed_dt
													} }
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