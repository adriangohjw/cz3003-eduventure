import sys
from os import path, getcwd
sys.path.append(getcwd())

import csv

from models import db
from run_test import create_app
app = create_app()
app.app_context().push()
db.init_app(app)

from services.core.operations.challenges_operations import initializeChallenge
from services.core.operations.courses_operations import initializeCourse
from services.core.operations.lessons_operations import initializeLesson
from services.core.operations.questionAttempts_operations import initializeQuestionAttempt
from services.core.operations.quizAttempts_operations import initializeQuizAttempt
from services.core.operations.rs_lesson_quiz_contains_operations import initializeRsLessonQuizContain
from services.core.operations.rs_staff_course_teaches_operations import initializeRsStaffCourseTeach
from services.core.operations.rs_student_course_enrols_operations import initializeRsStudentCourseEnrol
from services.core.operations.staffs_operations import initializeStaff
from services.core.operations.students_operations import initializeStudent
from services.core.operations.topics_operations import initializeTopic

from services.quiz.operations.questionChoices_operations import initializeQuestionChoice
from services.quiz.operations.questions_operations import initializeQuestion
from services.quiz.operations.quizzes_operations import initializeQuiz
from services.quiz.operations.rs_quiz_course_assigns_operations import initializeRsQuizCourseAssign
from services.quiz.operations.rs_quiz_question_contains_operations import initializeRsQuizQuestionContain

# empty database to default state with samples
db.session.commit()
db.session.remove()
db.drop_all()
db.create_all()

import time


def add_object(func):
    start_time_local = time.time()
    func()
    print("--- {} seconds ---".format(round(time.time() - start_time_local, 2)))


start_time = time.time()

# add students
def add_users():
    print('\nAdding users...')
    with open('db_populate/users.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_staff = 0
        count_student = 0
        for row in csv_reader:
            if not row['matriculation_number']:
                staff = initializeStaff(
                    email=row['email'],
                    password=row['password'],
                    name=row['name']
                )
                db.session.add(staff)
                count_staff += 1
            else:
                student = initializeStudent(
                    email=row['email'],
                    password=row['password'],
                    matriculation_number=row['matriculation_number'],
                    name=row['name']
                )
                db.session.add(student)
                count_student += 1
        db.session.commit()
        print('>>> {} staffs added'.format(count_staff))
        print('>>> {} staffs added'.format(count_student))

# add courses
def add_courses():
    print('\nAdding courses...')
    with open('db_populate/courses.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_course = 0
        for row in csv_reader:
            course = initializeCourse(
                index=row['index']
            )
            db.session.add(course)
            count_course += 1
        db.session.commit()
        print('>>> {} courses added'.format(count_course))

# add rs_staff_course_teaches
def add_rs_staff_course_teaches():
    print('\nAdding rs_staff_course_teaches...')
    with open('db_populate/rs_staff_course_teaches.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_rs = 0
        for row in csv_reader:
            rs = initializeRsStaffCourseTeach(
                staff_id=row['staff_id'],
                course_index=row['course_index']
            )
            db.session.add(rs)
            count_rs += 1
        db.session.commit()
        print('>>> {} rs added'.format(count_rs))

# add rs_student_course_enrols
def add_rs_student_course_enrols():
    print('\nAdding rs_student_course_enrols...')
    with open('db_populate/rs_student_course_enrols.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_rs = 0
        for row in csv_reader:
            rs = initializeRsStudentCourseEnrol(
                student_id=row['student_id'],
                course_index=row['course_index']
            )
            db.session.add(rs)
            count_rs += 1
        db.session.commit()
        print('>>> {} rs added'.format(count_rs))

# add topics
def add_topics():
    print('\nAdding topics...')
    with open('db_populate/topics.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_topic = 0
        for row in csv_reader:
            topic = initializeTopic(row['name'])
            db.session.add(topic)
            count_topic += 1
        db.session.commit()
        print('>>> {} topics added'.format(count_topic))

# add lessons
def add_lessons():
    print('\nAdding lessons...')
    with open('db_populate/lessons.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_lesson = 0
        for row in csv_reader:
            lesson = initializeLesson(
                topic_id=row['topic_id'],
                name=row['name'],
                content=row['content'],
                url_link=row['url_link']
            )
            db.session.add(lesson)
            count_lesson += 1
        db.session.commit()
        print('>>> {} topics added'.format(count_lesson))

# add quizzes
def add_quizzes():
    print('\nAdding quizzes...')
    with open('db_populate/quizzes.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_quiz = 0
        for row in csv_reader:
            quiz = initializeQuiz(
                staff_id=row['staff_id'],
                name=row['name'],
                is_fast=True if row['is_fast'] == 'TRUE' else False,
                date_start=row['date_start'],
                date_end=row['date_end']
            )
            db.session.add(quiz)
            count_quiz += 1
        db.session.commit()
        print('>>> {} quizzes added'.format(count_quiz))

# add questions
def add_questions():
    print('\nAdding questions...')
    with open('db_populate/questions.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_question = 0
        for row in csv_reader:
            question = initializeQuestion(
                topic_id=row['topic_id'],
                lesson_id=row['lesson_id'],
                description=row['description']
            )
            db.session.add(question)
            count_question += 1
        db.session.commit()
        print('>>> {} questions added'.format(count_question))

# add questionchoices
def add_questionchoices():
    print('\nAdding questionchoices...')
    with open('db_populate/questionchoices.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_questionchoices = 0
        for row in csv_reader:
            questionchoice = initializeQuestionChoice(
                question_id=row['question_id'],
                description=row['description'],
                is_correct=True if row['is_correct'] == 'TRUE' else False
            )
            questionchoice.id = row['id']
            db.session.add(questionchoice)
            count_questionchoices += 1
        db.session.commit()
        print('>>> {} questionchoices added'.format(count_questionchoices))

# add rs_quiz_question_contains
def add_rs_quiz_question_contains():
    print('\nAdding rs_quiz_question_contains...')
    with open('db_populate/rs_quiz_question_contains.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_rs = 0
        for row in csv_reader:
            rs = initializeRsQuizQuestionContain(
                quiz_id=row['quiz_id'],
                question_id=row['question_id']
            )
            db.session.add(rs)
            count_rs += 1
        db.session.commit()
        print('>>> {} rs added'.format(count_rs))

# add rs_quiz_course_assigns
def add_rs_quiz_course_assigns():
    print('\nAdding rs_quiz_course_assigns...')
    with open('db_populate/rs_quiz_course_assigns.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_rs = 0
        for row in csv_reader:
            rs = initializeRsQuizCourseAssign(
                quiz_id=row['quiz_id'],
                course_index=row['course_index']
            )
            db.session.add(rs)
            count_rs += 1
        db.session.commit()
        print('>>> {} rs added'.format(count_rs))

# add rs_lesson_quiz_contains
def add_rs_lesson_quiz_contains():
    print('\nAdding rs_lesson_quiz_contains...')
    with open('db_populate/rs_lesson_quiz_contains.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_rs = 0
        for row in csv_reader:
            rs = initializeRsLessonQuizContain(
                topic_id=row['topic_id'],
                lesson_id=row['lesson_id'],
                quiz_id=row['quiz_id']
            )
            db.session.add(rs)
            count_rs += 1
        db.session.commit()
        print('>>> {} rs added'.format(count_rs))

# add challenges
def add_challenges():
    print('\nAdding challenges...')
    with open('db_populate/challenges.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_challenge = 0
        for row in csv_reader:
            challenge = initializeChallenge(
                from_student_id=row['from_student_id'],
                to_student_id=row['to_student_id'],
                quiz_id=row['quiz_id']
            )
            if row['winner_id'] and (row['is_completed'] == 'TRUE'):
                challenge.winner_id = row['winner_id']
                challenge.is_completed = True
            db.session.add(challenge)
            count_challenge += 1
        db.session.commit()
        print('>>> {} challenges added'.format(count_challenge))

# add quizattempts
def add_quizattempts():
    print('\nAdding quizattempts...')
    with open('db_populate/quizattempts.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_quizattempts = 0
        for row in csv_reader:
            quizattempt = initializeQuizAttempt(
                student_id=row['student_id'],
                quiz_id=row['quiz_id'],
                score=row['score']
            )
            db.session.add(quizattempt)
            count_quizattempts += 1
        db.session.commit()
        print('>>> {} quizattempts added'.format(count_quizattempts))

# add questionattempts
def add_questionattempts():
    print('\nAdding questionattempts...')
    with open('db_populate/questionattempts.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        count_questionattempts = 0
        for row in csv_reader:
            questionattempt = initializeQuestionAttempt(
                student_id=row['student_id'],
                question_id=row['question_id'],
                is_correct=True if row['is_correct'] == 'TRUE' else False,
                duration_ms=row['duration_ms']
            )
            db.session.add(questionattempt)
            count_questionattempts += 1
        db.session.commit()
        print('>>> {} questionattempts added'.format(count_questionattempts))

add_object(add_users)
add_object(add_courses)
add_object(add_rs_student_course_enrols)
add_object(add_rs_staff_course_teaches)
add_object(add_topics)
add_object(add_lessons)
add_object(add_quizzes)
add_object(add_questions)
add_object(add_questionchoices)
add_object(add_rs_quiz_question_contains)
add_object(add_rs_quiz_course_assigns)
add_object(add_rs_lesson_quiz_contains)
add_object(add_challenges)
add_object(add_quizattempts)
add_object(add_questionattempts)

print("\nDB population completed")
print("--- {} seconds ---".format(round(time.time() - start_time, 2)))
