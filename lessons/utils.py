from django.http import Http404
from django.utils import timezone
from django.db import DataError
from lessons.models import Lesson
import json
import string
import random
from datetime import timedelta
import math

def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def nearest_hour(dt):
    """ Round datetime to nearest hour """

    atTheHour = dt.replace(second=0, microsecond=0, minute=0, hour=dt.hour)
    if dt.minute < 30:
        return atTheHour
    else:
        return atTheHour + timedelta(hours=1)

def get_new_lesson_data():
    """ Return an empty lesson (for new lesson creation) """

    return  {
        'title':    f'New lesson (#{ random_string(8) })',
        'lesson':   '',
        'examples': [],
    }

def get_validated_lesson_data(request):
    """ From a request, raise Http404 or return validated lessonData """

    examples = []
    for k, v in request.POST.items():
        # Only use non-empty questions and answers
        if 'question' in k and v:
            qid = k.split('-')[-1]
            question = v
            answer = request.POST.get(f'answer-{ qid }')
            if answer:
                examples.append({'question': question, 'answer': answer})
                
    lessonData = {
        'title':    request.POST.get('titleFormInput'),
        'lesson':   request.POST.get('fullLessonFormTextarea'),
        'examples': examples,
    }
    
    for field, maxLength in (('title', 500), ('lesson', 10000), ('examples', 500)):
        if lessonData.get(field) is None:
            raise Http404(f'The required lesson field "{ field }" is missing')
        if field == 'examples':
            examples = lessonData[field]
            for i, ex in enumerate(examples):
                if len(ex['question']) > maxLength or len(ex['answer']) > maxLength:
                    raise Http404(f'Sorry, review question { i } is too long. The max length is { maxLength } characters.')        
        elif len(lessonData[field]) > maxLength:
            raise Http404(f'Sorry, the { field } section is too long. The max length is { maxLength } characters.')
    return lessonData

def read_lesson_data(lesson):
    lesson.file.open(mode='r')
    lessonData = json.loads(lesson.file.read())
    lesson.file.close()
    return lessonData

def get_review_QnAs(lesson):
    data = read_lesson_data(lesson)
    return [(ex['question'], ex['answer']) for ex in data['examples']]

nextReviewTimedeltaTable = {
    0: None, # stage before user correctly answers once
    1: timedelta(hours=4),
    2: timedelta(hours=8),
    3: timedelta(days=1),
    4: timedelta(days=2),
    5: timedelta(days=4),
    6: timedelta(weeks=2),
    7: timedelta(days=30),
    8: timedelta(days=90),
    9: None, # user has completely finished reviews
}

def new_review_stage(lesson, isCorrect):
    if isCorrect:
        return lesson.review_stage + 1
    else:
        incorrectPenalty = math.ceil(0.5 * lesson.review_incorrect)
        stagePenalty = 1 if lesson.review_stage < 5 else 2
        return max(1, lesson.review_stage - (incorrectPenalty * stagePenalty))

def update_review_fields(lesson, isCorrect):
    now = timezone.now()
    if lesson.next_review_time > now:
        raise DataError('The lesson is not available for review yet.')
    if isCorrect:
        lesson.review_correct += 1
    else:
        lesson.review_incorrect += 1
    lesson.review_stage = new_review_stage(lesson, isCorrect)
    lesson.next_review_time = nearest_hour(
        now + nextReviewTimedeltaTable[lesson.review_stage]
    )
    lesson.save(update_fields=[
        'review_correct',
        'review_incorrect',
        'review_stage',
        'next_review_time',
    ])
    print(f'Updated lesson { lesson.id }')