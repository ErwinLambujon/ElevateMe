from django.urls import path

from . import views

app_name = 'Ranking'

urlpatterns = [
    path('ranking/', views.ranking, name="ranking"),
    path('ranking/<int:setting>/', views.ShowLists.as_view(), name="twoLists"),
    path('add-to-table/', views.AddToTable.as_view(), name="add-to-table")
]