from pprint import pprint
from exceptions import ErrorWithCode
import statistics
import numpy as np

from services.core.dao.StatisticsDAO import \
    statRead


def statReadOperation():

    raw_stats = statRead()

    stat_dict = {}
    stat_dict['stats_temp'] = []

    # add unique courses
    for s in raw_stats:
        s_dict = s._asdict()
        stat_dict['stats_temp'].append(
            {
                'course_index': s_dict['course_index'],
                'quizzes_temp': []
            }
        )
    stat_dict['stats'] = []
    for x in stat_dict['stats_temp']:
        if x not in stat_dict['stats']:
            stat_dict['stats'].append(x)
    del stat_dict['stats_temp']

    # add unique quizzes to courses
    for s in raw_stats:
        s_dict = s._asdict()
        for stat in stat_dict['stats']:
            if stat['course_index'] == s_dict['course_index']:
                stat['quizzes_temp'].append(
                    {
                        'id': s_dict['quiz_id'],
                        'name': s_dict['quiz_name'],
                        'attempts': []
                    }
                )
    for stat in stat_dict['stats']:
        stat['quizzes'] = []
        for x in stat['quizzes_temp']:
            if x not in stat['quizzes']:
                stat['quizzes'].append(x)
        del stat['quizzes_temp']

    # add unique attempts to quizzes
    for s in raw_stats:
        s_dict = s._asdict()
        for stat in stat_dict['stats']:
            if stat['course_index'] == s_dict['course_index']:
                for quiz in stat['quizzes']:
                    if quiz['id'] == s_dict['quiz_id'] and s_dict['attempt_score'] is not None:
                        quiz['attempts'].append(s_dict['attempt_score'])

    # add statistics to quizzes
    for stat in stat_dict['stats']:
        for quiz in stat['quizzes']:
            
            try:
                quiz['avg_score'] = round(statistics.mean(quiz['attempts']), 2)
            except statistics.StatisticsError:
                quiz['avg_score'] = None
                
            try:    
                quiz['max_score'] = max(quiz['attempts'])
            except ValueError:
                quiz['max_score'] = None

            try:
                quiz['min_score'] = min(quiz['attempts'])
            except ValueError:
                quiz['min_score'] = None

            try:
                quiz['stdev'] = round(statistics.stdev(quiz['attempts']), 2)
            except statistics.StatisticsError:
                quiz['stdev'] = None

            try:
                quiz['25th_percentile'] = round(np.percentile(quiz['attempts'], 25), 2)
                quiz['75th_percentile'] = round(np.percentile(quiz['attempts'], 75), 2)
                quiz['95th_percentile'] = round(np.percentile(quiz['attempts'], 95), 2)
            except IndexError:
                quiz['25th_percentile'] = None
                quiz['75th_percentile'] = None
                quiz['95th_percentile'] = None
 
    return stat_dict
