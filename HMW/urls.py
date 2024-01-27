from django.urls import path

from . import views

app_name = 'HMW'

urlpatterns = [
    path('HMW/', views.HMWPage, name="HMW"),
    path('root-problem/', views.GeneratePotentialRootProblem.as_view(), name="root-problem"),
    path('generated-5-hmws/<str:value>/', views.GenerateFiveHMW.as_view(), name='five_hmw'),
    path('generate-elevator-pitch/', views.GenerateElevatorPitch.as_view(), name='elevator-pitch'),
    path('update-elevator-pitch/', views.updateElevatorPitch, name='update-elevator-pitch'),
    path('get-problem-statemen-and-whys/', views.getProblemStatementAndWhys, name="get-problem-statement-and-whys")
]