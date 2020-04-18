from pprint import pprint
from exceptions import ErrorWithCode

from services.core.dao.StudentsDAO import studentRead
from services.core.dao.ProgressesDAO import progressRead


def progressReadOperation(student_id):
    
    student = studentRead(col='id', value=student_id)

    # student is not found
    if student is None:
        raise ErrorWithCode(409, "No student found")

    # success case
    progresses = progressRead(student_id)

    progress_dict = {}
    progress_dict['topics_temp'] = []


    # add unique topics to the end result
    # check for duplicates in topics (due to left join)
    for p in progresses:
        p_dict = p._asdict()
        progress_dict['topics_temp'].append(
            {
                'id': p_dict['topic_id'],
                'name': p_dict['topic_name'],
                'lessons_temp': []
            }
        )    
    progress_dict['topics'] = []
    for x in progress_dict['topics_temp']:
        if x not in progress_dict['topics']:
            progress_dict['topics'].append(x)
    del progress_dict['topics_temp']
    
    # add unique lessons to topics
    # check for duplicates in lessons to topics (due to left join)
    for p in progresses:
        p_dict = p._asdict()
        for topics in progress_dict['topics']:
            if topics['id'] == p_dict['topic_id']:
                topics['lessons_temp'].append(
                    {
                        'id': p_dict['lesson_id'],
                        'quizzes': []
                    }
                )
    for topic in progress_dict['topics']:
        topic['lessons'] = []
        for x in topic['lessons_temp']:
            if x not in topic['lessons']:
                topic['lessons'].append(x)
        del topic['lessons_temp']

    # add unique quizzes to lessons
    # no need to check for duplicates as (topic_id, lesson_id, quiz_id) has a unique constraint
    for p in progresses:
        p_dict = p._asdict()
        for topics in progress_dict['topics']:
            if topics['id'] == p_dict['topic_id']:
                for lesson in topics['lessons']:
                    if (lesson['id'] == p_dict['lesson_id']) and (p_dict['quiz_id'] is not None):
                        lesson['quizzes'].append(
                            {
                                'id': p_dict['quiz_id'],
                                'max_score': p_dict['sq_attempts_score'],
                                'total_questions': p_dict['count_questions']
                            }
                        )

    # add completion status
    for topic in progress_dict['topics']:
        topic['total_lessons'] = len(topic['lessons'])
        topic['completed_lessons'] = 0
        for lesson in topic['lessons']:
            lesson['total_quizes'] = len(lesson['quizzes'])
            lesson['completed_quizzes'] = 0
            for quiz in lesson['quizzes']:
                if quiz['max_score'] == quiz['total_questions']:
                    quiz['completion_status'] = True
                    lesson['completed_quizzes'] += 1
                else:
                    quiz['completion_status'] = False
            if lesson['total_quizes'] == lesson['completed_quizzes']:
                lesson['completion_status'] = True
                topic['completed_lessons'] += 1
            else:
                lesson['completion_status'] = False
        if topic['total_lessons'] == topic['completed_lessons']:
            topic['completion_status'] = True
        else:
            topic['completion_status'] = False            

    return progress_dict
