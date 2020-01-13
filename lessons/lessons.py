"""
Lesson storage, saving/loading, etc.
"""

import os
import json
from django.conf import settings

STORAGE_DIR = os.path.join(settings.BASE_DIR, 'storage')

def lesson_filename(userID, lessonID):
    return os.path.join(
        STORAGE_DIR, 
        str(userID), 
        f'{lessonID}.json'
    )

def load_lesson_with_IDs(userID, lessonID):
    """ Load lesson dict from file in storage dump 

        Use when you know IDs of both user and lesson
    """

    with open(lesson_filename(userID, lessonID), 'r') as f:
        return json.load(f)

def load_lesson(user, lessonID):
    """ Load lesson dict from file in storage dump 

        Use when you have user object and lessonID
    """
    
    return load_lesson_with_IDs(user.profile.uuid, lessonID)

def load_all_lessons(user):
    """ Return all of user's lessons as a list """

    lessonFiles = os.listdir(os.path.join(STORAGE_DIR, user.id))
    lessonIDs = [os.path.splitext(f) for f in lessonFiles]
    return [
        load_lesson(user, lessonID)
        for lessonID in lessonIDs
    ]

def save_lesson(user, lessonData):
    """ Save lesson to user's dir in storage dump """

    userID, lessonID = user.profile.uuid, lessonData['id']
    filename = lesson_filename(userID, lessonID)
    try:
        f = open(filename, 'w')
    except FileNotFoundError:
        os.makedirs(filename)
        f = open(filename, 'w')
    json.dump(lesson, f)

def lesson_from_post(post):
    """ Return a lesson from post data """

    return {
        'title':    post.get('titleFormInput'),
        'lesson':   post.get('fullLessonFormTextarea'),
        'examples': post.get('examplesFormTextarea'),
    }
