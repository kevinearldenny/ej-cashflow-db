from django.urls import path
from django.conf.urls import url


from companies import views

app_name = 'companies'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('companies/<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path(r'^companies/create/$', views.create_company, name='create')
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
]