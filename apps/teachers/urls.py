from django.urls import path
from .views import AssignmetsView


urlpatterns = [
  path('assignments/', AssignmetsView.as_view(), name='teachers-assignments')
]
