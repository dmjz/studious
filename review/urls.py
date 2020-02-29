from django.urls import path
from review.views import review, add_review, available, save_progress, lesson_details

urlpatterns = [
    path('', review, name='review'),
    path('add/<int:lesson_id>', add_review, name='add_review'),
    path('available/', available, name='available'),
    path('save-progress/', save_progress, name='save_progress'),
    path('lesson-details/', lesson_details, name='lesson_details'),
]