from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_control.decorators import show_to_patient

from user_control.models import PatientModel, UserModel
from .forms import *
from .models import HistoryModel


@login_required(login_url="login")
def history_home_view(request, pk):
    request_user = UserModel.objects.get(id=request.user.id)
    user = UserModel.objects.get(id=pk)
    patient = PatientModel.objects.get(user=user)
    records = HistoryModel.objects.filter(user=patient)

    is_patient = False
    if request_user.is_patient:
        is_patient = True

    context = {
        "patient": patient,
        "records": records,
        "is_patient": is_patient,
    }
    return render(request, "pages/patient-history/history-home.html", context)


@login_required(login_url="login")
@show_to_patient()
def history_create_view(request, pk):
    request_user = UserModel.objects.get(id=request.user.id)
    user = UserModel.objects.get(id=pk)
    if request_user != user:
        return render(request, '401.html')

    task = "Create New"
    form = AddEditHistoryForm()
    patient = PatientModel.objects.get(user=user)
    print(patient)
    if request.method == "POST":
        form = AddEditHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            history = form.save(commit=False)
            history.user = patient
            history.save()
            return redirect("history-detail", pk, history.id)
    
    context = {
        "task": task,
        "form": form,
    }
    return render(request, "pages/patient-history/history-create-update.html", context)


@login_required(login_url="login")
def history_detail_view(request, pk, historyId):
    request_user = UserModel.objects.get(id=request.user.id)
    user = UserModel.objects.get(id=pk)
    if request_user != user:
        return render(request, '401.html')

    record = HistoryModel.objects.get(id=historyId)
    patient = record.user

    edit_access = False
    if request.user.is_authenticated and request.user.is_patient:
        if request.user == patient.user:
            edit_access = True

    context = {
        "record": record,
        "patient": patient,
        "edit_access": edit_access,
    }
    return render(request, "pages/patient-history/history-detail.html", context)


@login_required(login_url="login")
@show_to_patient()
def history_update_view(request, pk, historyId):
    request_user = UserModel.objects.get(id=request.user.id)
    user = UserModel.objects.get(id=pk)
    if request_user != user:
        return render(request, '401.html')

    task = "Update"
    record = HistoryModel.objects.get(id=historyId)
    patient = record.user
    form = AddEditHistoryForm(instance=record)

    if request.method == "POST":
        form = AddEditHistoryForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect("history-detail", record.user.user.id, record.id)

    context = {
        "task": task,
        "form": form,
        "record": record,
        "patient": patient,
    }

    return render(request, "pages/patient-history/history-create-update.html", context)


@login_required(login_url="login")
@show_to_patient()
def history_delete_view(request, pk, historyId):
    request_user = UserModel.objects.get(id=request.user.id)
    user = UserModel.objects.get(id=pk)
    if request_user != user:
        return render(request, '401.html')

    record = HistoryModel.objects.get(id=historyId)
    patient = record.user

    if request.method == 'POST':
        record.delete()
        return redirect("history-home", patient.user.id)

    context = {
        "record": record,
        "patient": patient,
    }

    return render(request, "pages/patient-history/history-delete.html", context)
