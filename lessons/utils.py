from django.http import Http404
from lessons.models import Lesson
import json
import string
import random

def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

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