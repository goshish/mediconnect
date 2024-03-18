from django.urls import path
from .views import MainPageView, AnalyticsView, CallbackView, DoctorAppointmentView, AppointmentHistoryView, \
    DoctorAnalyticsListView, DoctorAnalyticsView

urlpatterns = [
    path('main/', MainPageView.as_view(), name='AdminMain'),
    path('analytics/', AnalyticsView.as_view(), name='Analytics'),
    path('callback/', CallbackView.as_view(), name='Callback'),
    path('doctor-appointments/<int:doctor_id>/', DoctorAppointmentView.as_view(), name='DocAnalytics'),
    path('appointment-history/', AppointmentHistoryView.as_view(), name='AppHistory'),
    path('doctor-analytics/', DoctorAnalyticsListView.as_view(), name='DoctorAnalyticsList'),
    path('doctor-analytics/<int:doctor_id>/', DoctorAnalyticsView.as_view(), name='DoctorAnalytics'),
]
