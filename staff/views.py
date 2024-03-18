from django.db.models.functions import TruncDay
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from main.models import Appointment, Callback
from django.db.models import Sum, Count
from .forms import DateSelectForm
from datetime import datetime
from django.urls import reverse
from main.models import Doctor


class MainPageView(ListView):
    template_name = 'staff/main-staff.html'
    context_object_name = 'appointment'
    paginate_by = 3
    form_class = DateSelectForm

    def get_queryset(self):
        queryset = Appointment.objects.all()
        selected_date = self.request.GET.get('selected_date')
        if selected_date:
            queryset = queryset.filter(appointment_day=selected_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = self.request.GET.get('selected_date')
        context['filter_form'] = self.get_form()
        context['total_appointments'] = Appointment.objects.filter(appointment_day=selected_date).count()
        context['total_revenue_all'] = Appointment.objects.filter(appointment_day=selected_date).aggregate(
            total_price=Sum('doctor__visit_price'))['total_price'] or 0
        context['doctors'] = Doctor.objects.all()
        return context

    def get_form(self):
        return self.form_class(self.request.GET)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            if selected_date:
                return HttpResponseRedirect(reverse('AdminMain') + f'?selected_date={selected_date}')
        return self.get(request, *args, **kwargs)


class AppointmentHistoryView(ListView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'staff/appointment-history.html'
    paginate_by = 10
    form_class = DateSelectForm

    def get_queryset(self):
        queryset = Appointment.objects.all()
        selected_date = self.request.GET.get('selected_date')
        if selected_date:
            queryset = queryset.filter(appointment_day=selected_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = self.request.GET.get('selected_date')
        context['filter_form'] = self.get_form()
        context['total_appointments'] = Appointment.objects.count()
        context['total_revenue_all'] = Appointment.objects.aggregate(total_price=Sum('doctor__visit_price'))[
                                           'total_price'] or 0
        context['doctors'] = Doctor.objects.all()
        return context

    def get_form(self):
        return self.form_class(self.request.GET)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            if selected_date:
                return HttpResponseRedirect(reverse('AdminMain') + f'?selected_date={selected_date}')
        return self.get(request, *args, **kwargs)


class CallbackView(ListView):
    model = Callback
    context_object_name = 'callbacks'
    template_name = 'staff/callback.html'
    paginate_by = 10
    form_class = DateSelectForm

    def get_queryset(self):
        queryset = Callback.objects.all()
        selected_date = self.request.GET.get('selected_date')
        if selected_date:
            queryset = queryset.filter(date=selected_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = self.request.GET.get('selected_date')
        context['filter_form'] = self.get_form()
        context['callbacks_today'] = Callback.objects.filter(date=selected_date).count()
        context['total_callbacks'] = Callback.objects.count()
        return context

    def get_form(self):
        return self.form_class(self.request.GET)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            if selected_date:
                return HttpResponseRedirect(reverse('AdminMain') + f'?selected_date={selected_date}')
        return self.get(request, *args, **kwargs)


class DoctorAppointmentView(ListView):
    model = Appointment
    template_name = 'staff/doctor-appointment.html'
    context_object_name = 'doctor_appointments'  # Обновленное имя контекста

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        selected_date = self.request.GET.get('selected_date')

        queryset = Appointment.objects.filter(doctor_id=doctor_id)  # Фильтрация по id доктора

        if selected_date:
            queryset = queryset.filter(appointment_day=selected_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_form()
        context['total_appointments'] = context['doctor_appointments'].count()
        context['total_price_all'] = context['doctor_appointments'].aggregate(
            total_price=Sum('doctor__visit_price'))['total_price'] or 0
        context['doctors'] = Doctor.objects.all()
        return context

    def get_form(self):
        return DateSelectForm(self.request.GET)


class AnalyticsView(ListView):
    template_name = 'staff/analytics.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_appointments'] = Appointment.objects.filter().count()
        context['total_callbacks'] = Callback.objects.filter().count()
        context['total_revenue_all'] = Appointment.objects.filter().aggregate(
            total_price=Sum('doctor__visit_price'))['total_price'] or 0
        context['doctors'] = Doctor.objects.all()
        appointments_per_day = Appointment.objects.annotate(day=TruncDay('appointment_day')).values('day').annotate(
            count=Count('id')).order_by()
        total_apppointment_days = appointments_per_day.count()
        total_appointments = context['total_appointments']
        if total_apppointment_days > 0:
            average = total_appointments / total_apppointment_days
            context['average_appointments_per_day'] = round(average, 1)

        else:
            context['average_appointments_per_day'] = 0

        revenue_per_day = Appointment.objects.annotate(day=TruncDay('appointment_day')).values('day').annotate(
            daily_revenue=Sum('doctor__visit_price')).order_by()
        total_revenue_days = revenue_per_day.count()
        total_revenue = sum(item['daily_revenue'] for item in revenue_per_day if item['daily_revenue'])

        if total_revenue_days > 0:
            average_revenue = total_revenue / total_revenue_days
            context['average_revenue_per_day'] = round(average_revenue, 1)
        else:
            context['average_revenue_per_day'] = 0

        average_callback_per_day = Callback.objects.annotate(day=TruncDay('date')).values('day').annotate(
            count=Count('id')).order_by()
        total_callback_day = average_callback_per_day.count()
        total_callback = context['total_callbacks']
        if total_callback_day > 0:
            average = total_callback / total_callback_day
            context['average_callback_per_day'] = round(average, 1)
        else:
            context['average_callback_per_day'] = 0

        return context


class DoctorAnalyticsListView(ListView):
    template_name = 'staff/doctor-analytics-list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.all()


class DoctorAnalyticsView(ListView):
    model = Appointment
    template_name = 'staff/doctor-analytics.html'
    context_object_name = 'doctor_analytics'

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        queryset = Appointment.objects.filter(doctor_id=doctor_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_appointments'] = context['doctor_analytics'].count()
        context['total_revenue'] = context['doctor_analytics'].aggregate(
            total_price=Sum('doctor__visit_price'))['total_price'] or 0
        context['doctors'] = Doctor.objects.all()
        return context