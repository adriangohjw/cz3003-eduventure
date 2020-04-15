from locust import HttpLocust, TaskSequence, seq_task, task, between


class UserBehaviour(TaskSequence):


    # user login
    @seq_task(1)
    @task(1)
    def login(self):
        self.client.get('/users/auth?email=jgoh070@e.ntu.edu.sg&password=password_22')


    # load data to display homescreen
    @seq_task(2)
    @task(1)
    def display_homescreen(self):
        self.client.get('/progresses?student_id=22')


    # load notification 
    @seq_task(3)
    @task(1)
    def get_notification(self):
        self.client.get('/challenges?to_student_id=22&is_completed=false')


    # load lesson content 
    @seq_task(4)
    @task(1)
    def load_lesson(self):
        self.client.get('/lessons?topic_id=1&lesson_id=1')


    # Attempt each quiz 3 times
    @seq_task(5)
    @task(3)
    def load_lesson(self):

        # fetch quizzes
        self.client.get('/lessons/quizzes?topic_id=1&lesson_id=1')
        
        # fetch questions for quiz 1
        self.client.get('/quizzes/questions?quiz_id=1')

        # update quiz and question attempts (quiz 1)
        self.client.post('/question_attempts?student_id=22&question_id=1&is_correct=true&duration_ms=5000')
        self.client.post('/question_attempts?student_id=22&question_id=2&is_correct=true&duration_ms=5000')
        self.client.post('/question_attempts?student_id=22&question_id=3&is_correct=true&duration_ms=5000')
        self.client.post('/quiz_attempts?student_id=22&quiz_id=1&score=3')

        # fetch questions for quiz 2
        self.client.get('/quizzes/questions?quiz_id=2')

        # update quiz and question attempts (quiz 2)
        self.client.post('/question_attempts?student_id=22&question_id=4&is_correct=true&duration_ms=5000')
        self.client.post('/question_attempts?student_id=22&question_id=5&is_correct=true&duration_ms=5000')
        self.client.post('/question_attempts?student_id=22&question_id=6&is_correct=false&duration_ms=5000')
        self.client.post('/quiz_attempts?student_id=22&quiz_id=2&score=2')

        # fetch questions for quiz 3
        self.client.get('/quizzes/questions?quiz_id=3')

        # update quiz and question attempts (quiz 3)
        self.client.post('/question_attempts?student_id=22&question_id=7&is_correct=true&duration_ms=5000')
        self.client.post('/question_attempts?student_id=22&question_id=8&is_correct=false&duration_ms=5000')
        self.client.post('/question_attempts?student_id=22&question_id=9&is_correct=false&duration_ms=5000')
        self.client.post('/quiz_attempts?student_id=22&quiz_id=3&score=1')


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(1, 10)
