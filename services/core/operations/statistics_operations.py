from pprint import pprint
from exceptions import ErrorWithCode
import statistics
import numpy as np

from services.core.dao.StatisticsDAO import \
    statRead, lessonCompletedRead


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


def lessonCompletedReadOperation():

    raw_stats = lessonCompletedRead()

    stat_dict = {}
    stat_dict['courses'] = []

    # add unique courses to end result
    course_list = []
    for item in raw_stats:
        item_course = item._asdict()['course_index']
        if (item_course not in course_list) and (item_course is not None):
            course_list.append(item_course)
            stat_dict['courses'].append(
                {
                    'course_index': item_course,
                    'progress': []
                }
            )

    # add topic to progress of every course
    topic_list = []
    for item in raw_stats:
        item_topic_id, item_topic_name = item._asdict()['topic_id'], item._asdict()['topic_name']
        if (item_topic_id not in topic_list):
            topic_list.append(item_topic_id)
            for course in stat_dict['courses']:
                course['progress'].append(
                    {
                        'topic_id': item_topic_id,
                        'topic_name': item_topic_name,
                        'lessons_temp': []
                    }
                )

    # add lesson to topic of every course
    for item in raw_stats:
        i_dict = item._asdict()
        for course in stat_dict['courses']:
            for topic in course['progress']:
                if topic['topic_id'] == i_dict['topic_id']:
                    topic['lessons_temp'].append(
                        {
                            'lesson_id': i_dict['lesson_id'],
                            'lesson_name': i_dict['lesson_name'],
                            'count_completed': 0
                        }
                    )
    for course in stat_dict['courses']:
        for topic in course['progress']:
            topic['lessons'] = []
            for x in topic['lessons_temp']:
                if x not in topic['lessons']:
                    topic['lessons'].append(x)
            del topic['lessons_temp']


    # add completion status
    for item in raw_stats:
        i_dict = item._asdict()
        if (i_dict['student_id'] is not None) and (i_dict['score'] == i_dict['count_questions']):
            for course in stat_dict['courses']:
                for topic in course['progress']:
                    for lesson in topic['lessons']:
                        if (topic['topic_id'] == i_dict['topic_id']) and (lesson['lesson_id'] == i_dict['lesson_id']):
                            lesson['count_completed'] += 1
                            
    return stat_dict
