from django.urls import path
from review.views import review, add_review, available

urlpatterns = [
    path('', review, name='review'),
    path('add/<int:lesson_id>', add_review, name='add_review'),
    path('available/', available, name='available'),
]