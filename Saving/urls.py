from django.urls import path

from . import views

app_name = "Saving"

urlpatterns = [
    path('generate/save/', views.SaveProblemStatement.as_view(), name="saveModel"),
    path('save/<str:operation>/', views.SaveOperation.as_view(), name="saveOperation"),
    path('save/', views.Save.as_view(), name="savePage"),
    path('two_show_popup_venn/<int:instance_id>/', views.TwoPopUpVenn, name='two_show_popup_data'),
    path('three_show_popup_venn/<int:instance_id>/', views.ThreePopUpVenn, name='three_show_popup_data'),
]