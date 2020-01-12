"""
Lesson storage, saving/loading, etc.
"""

import os
import json
from django.conf.settings import BASE_DIR

STORAGE_DIR = os.path.join(BASE_DIR, 'storage')

def load_lesson_with_IDs(userID, lessonID):
    """ Load lesson dict from file in storage dump 

        Use when you know IDs of both user and lesson
    """

    file = os.path.join(STORAGE_DIR, userID, lessonID, '.json')
    with open(file, 'r') as f:
        return json.load(f)

def load_lesson(user, lessonID):
    """ Load lesson dict from file in storage dump 

        Use when you have user object and lessonID
    """
    
    return load_lesson_with_IDs(user.id, lessonID)

def load_all_lessons(user):
    """ Return all of user's lessons as a list """

    lessonFiles = os.listdir(os.path.join(STORAGE_DIR, user.id))
    lessonIDs = [os.path.splitext(f) for f in lessonFiles]
    return [
        load_lesson(user, lessonID)
        for lessonID in lessonIDs
    ]

def save_lesson(user, lesson):
    """ Save lesson to user's dir in storage dump """

    dest = os.path.join(STORAGE_DIR, user.id, lesson['id'])
    with open(dest, 'w') as f:
        json.dump(lesson, f)