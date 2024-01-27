from django.urls import path
from . import views

app_name = "Whys"

urlpatterns = [
    path('5-whys/', views.FiveWhys, name="5-whys"),
    path('ranked-problems-statement/<str:pk>/', views.RootProblemStatement.as_view(), name="ranked-problem-statement"),
    path('generate-5-whys/<str:value>/', views.GenerateFiveWhys, name="generate-5-whys"),
    path('two-settings-show-history/<str:pk>/', views.showTwoHistory, name='two-history'),
    path('three-settings-show-history/<str:pk>/', views.showThreeHistory, name='three-history')
]