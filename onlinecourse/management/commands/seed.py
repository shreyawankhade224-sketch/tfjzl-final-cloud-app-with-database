from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from onlinecourse.models import Choice, Course, Enrollment, Lesson, Question


class Command(BaseCommand):
    help = "Create demo data: admin user, learner user, a course with lessons and an exam."

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        learner, created = User.objects.get_or_create(
            username='learner', defaults={'first_name': 'Shreya'})
        if created:
            learner.set_password('learner123')
            learner.save()

        course, _ = Course.objects.get_or_create(
            name='Intro to Django',
            defaults={'description': 'Learn the basics of building web apps with Django.'})

        if not course.lesson_set.exists():
            Lesson.objects.create(course=course, order=1, title='What is Django?',
                                  content='Django is a high-level Python web framework.')
            Lesson.objects.create(course=course, order=2, title='Models and the Admin',
                                  content='Models define your data; the admin site manages it.')
            Lesson.objects.create(course=course, order=3, title='Views and Templates',
                                  content='Views handle requests and templates render HTML.')

        if not course.question_set.exists():
            q1 = Question.objects.create(
                course=course, grade=1,
                question_text='Which language is Django written in?')
            for text, ok in [('Python', True), ('Java', False), ('Ruby', False)]:
                Choice.objects.create(question=q1, choice_text=text, is_correct=ok)

            q2 = Question.objects.create(
                course=course, grade=1,
                question_text='Which of these are Django components? (select all that apply)')
            for text, ok in [('Models', True), ('Views', True),
                             ('Templates', True), ('Spring Beans', False)]:
                Choice.objects.create(question=q2, choice_text=text, is_correct=ok)

            q3 = Question.objects.create(
                course=course, grade=1,
                question_text='Which command applies database migrations?')
            for text, ok in [('python manage.py migrate', True),
                             ('python manage.py runserver', False),
                             ('python manage.py startapp', False)]:
                Choice.objects.create(question=q3, choice_text=text, is_correct=ok)

        Enrollment.objects.get_or_create(user=learner, course=course)
        Enrollment.objects.get_or_create(
            user=User.objects.get(username='admin'), course=course)
        self.stdout.write(self.style.SUCCESS(
            "Demo data ready. Logins: admin/admin123 and learner/learner123"))
