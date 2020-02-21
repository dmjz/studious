from django.http import Http404
from django.utils import timezone
from django.db import DataError
from lessons.models import Lesson
from lessons.newlessontext import newLessonText
import json
import string
import random
from datetime import timedelta
import math
import re

def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def nearest_hour(dt):
    """ Round datetime to nearest hour """

    atTheHour = dt.replace(second=0, microsecond=0, minute=0, hour=dt.hour)
    if dt.minute < 30:
        return atTheHour
    else:
        return atTheHour + timedelta(hours=1)

def clean_csv_tags(s):
    """ Clean string of tags separated by commas """

    split = s.split(',')
    cleaned = [re.sub(r'\s+', ' ', t).strip() for t in split]
    cleaned = [t for t in cleaned if t]
    if cleaned: 
        return ','.join(cleaned)
    return ''

def hash_tags(s):
    """ Process str of tags separated by commas into string
        of cleaned tags prefixed by hashes
        e.g. raw,tag,string -> #raw #tag #string
    """

    if not s:
        return ''
    clean = clean_csv_tags(s).split(',')
    res = ''
    for t in clean: 
        res += ('#' + t + ' ')
    return res.strip()

def get_new_lesson_data():
    """ Return an empty lesson (for new lesson creation) """

    return  {
        'title':    f'New lesson (#{ random_string(8) })',
        'lesson':   newLessonText,
        'examples': [{'question': 'question 1', 'answer': 'answer 1'}],
        'tags':     '',
    }

def get_validated_lesson_data(request_or_dict):
    """ From a request, raise Http404 or return validated lessonData 
        (can also pass dict of lesson data)
    """

    try:
        data = request_or_dict.POST
    except AttributeError:
        lessonData = {
            'title':    request_or_dict.get('title'),
            'lesson':   request_or_dict.get('lesson'),
            'examples': request_or_dict.get('examples'),
            'tags':     request_or_dict.get('tags'),
        }
    else:
        examples = []
        for k, v in data.items():
            # Only use non-empty questions and answers
            if 'question' in k and v:
                qid = k.split('-')[-1]
                question = v
                answer = data.get(f'answer-{ qid }')
                if answer:
                    examples.append({'question': question, 'answer': answer})
        lessonData = {
            'title':    data.get('titleFormInput'),
            'lesson':   data.get('fullLessonFormTextarea'),
            'examples': examples,
            'tags':     data.get('tagsFormInput'),
        }
    lessonData['tags'] = clean_csv_tags(lessonData['tags'])

    for field, maxLength in (('title', 500), ('lesson', 10000), ('examples', 500)):
        if lessonData.get(field) is None:
            raise Http404(f'The required lesson field "{ field }" is missing')
        if field == 'examples':
            examples = lessonData[field]
            if not examples:
                raise Http404('You must have at least one nonempty question-answer pair')
            for i, ex in enumerate(examples):
                if len(ex['question']) > maxLength or len(ex['answer']) > maxLength:
                    raise Http404(f'Sorry, review question { i } is too long. The max length is { maxLength } characters.')        
        elif len(lessonData[field]) > maxLength:
            raise Http404(f'Sorry, the { field } section is too long. The max length is { maxLength } characters.')
    return lessonData

def read_lesson_data(lesson):
    """ Open a lesson's file and return the data """

    lesson.file.open(mode='r')
    lessonData = json.loads(lesson.file.read())
    lesson.file.close()
    return lessonData

def get_review_QnAs(lesson):
    """ Parse lesson's data and return list of question, answer pairs """

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
    """ Return next review stage (after user answers a lesson's review) """

    if isCorrect:
        return lesson.review_stage + 1
    else:
        incorrectPenalty = math.ceil(0.5 * lesson.review_incorrect)
        stagePenalty = 1 if lesson.review_stage < 5 else 2
        return max(1, lesson.review_stage - (incorrectPenalty * stagePenalty))

def update_review_fields(lesson, isCorrect):
    """ Update lesson fields relating to reviews """

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

def search_tokens(lesson):
    """ Return search tokens from title, tags of lesson """

    return [
        t.strip().lower() for t in (lesson.tags.split(',') + lesson.title.split()) if t
    ]

def search_lessons(searchText):
    """ Return (terms, results) where terms are parsed search text,
        results are lessons returned by the search

        Searches tokens from split title and tags against tokens from searchText
    """

    terms = searchText.lower().split()
    results = [
        lesson for lesson in Lesson.objects.filter(is_public=True)
        if any((term in search_tokens(lesson) for term in terms))
    ]
    return (terms, results)