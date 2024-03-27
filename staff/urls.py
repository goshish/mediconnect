from django.urls import path
from .views import MainPageView, AnalyticsView, CallbackView, DoctorAppointmentView, AppointmentHistoryView, \
    DoctorAnalyticsListView, DoctorAnalyticsView, MonthListView, MonthAnalyticsView

urlpatterns = [
    path('main/', MainPageView.as_view(), name='AdminMain'),
    path('analytics/', AnalyticsView.as_view(), name='Analytics'),
    path('callback/', CallbackView.as_view(), name='Callback'),
    path('doctor-appointments/<int:doctor_id>/', DoctorAppointmentView.as_view(), name='DocAnalytics'),
    path('appointment-history/', AppointmentHistoryView.as_view(), name='AppHistory'),
    path('doctor-analytics/', DoctorAnalyticsListView.as_view(), name='DoctorAnalyticsList'),
    path('doctor-analytics/<int:doctor_id>/', DoctorAnalyticsView.as_view(), name='DoctorAnalytics'),
    path('month-list/', MonthListView.as_view(), name='MonthlyList'),
    path('monthly-analytics/<int:month>', MonthAnalyticsView.as_view(), name='month_analytics'),
]
