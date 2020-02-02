from django.urls import path
from review.views import review

urlpatterns = [
    path('', review, name='review'),
]