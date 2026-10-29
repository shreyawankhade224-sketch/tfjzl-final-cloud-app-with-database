from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Course, Enrollment, Submission


def course_list(request):
    courses = Course.objects.order_by('-total_enrollment')[:10]
    return render(request, 'onlinecourse/course_list_bootstrap.html',
                  {'course_list': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html',
                  {'course': course})


def extract_answers(request):
    """Collect the ids of every checked choice from the POST data."""
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            submitted_answers.append(int(request.POST[key]))
    return submitted_answers


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Auto-enroll the user if they have not been enrolled yet.
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(extract_answers(request))
    return HttpResponseRedirect(reverse(
        'onlinecourse:show_exam_result', args=(course.id, submission.id)))


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = [choice.id for choice in submission.choices.all()]

    total_score = 0
    score = 0
    for question in course.question_set.all():
        total_score += question.grade
        if question.is_get_score(selected_ids):
            score += question.grade

    grade = int(score / total_score * 100) if total_score else 0
    context = {
        'course': course,
        'selected_ids': selected_ids,
        'score': score,
        'total_score': total_score,
        'grade': grade,
        'passed': grade >= 80,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
