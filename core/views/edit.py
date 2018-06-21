from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import User, UserData, Plan, PlanDetail,Mob
from core.forms import PlanForm
import datetime


@login_required
def addView(request):
    form = PlanForm()
    if request.method=='POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            planObj = Plan()
            planObj.title = form.cleaned_data['title']
            planObj.endDate = form.cleaned_data['endDate']
            planObj.startDate = form.cleaned_data['startDate']
            planObj.description = form.cleaned_data['description']
            planObj.place = form.cleaned_data['place']
            planObj.admin = request.user
            planObj.hours = int(form.cleaned_data['hours']) * 4 + int(form.cleaned_data['minutes'])
            planObj.startTime = int(form.cleaned_data['startTimeHours']) * 4 + int(form.cleaned_data['startTimeMinutes'])
            planObj.endTime = int(form.cleaned_data['endTimeHours']) * 4 + int(form.cleaned_data['endTimeMinutes'])

            planObj.save()

            diff = planObj.endDate - planObj.startDate
            for d in range(diff.days+1):
                planDetailObj = PlanDetail()
                planDetailObj.date = planObj.startDate + datetime.timedelta(days=d)
                planDetailObj.startTime = planObj.startTime
                planDetailObj.endTime = planObj.endTime
                planDetailObj.plan = planObj

                planDetailObj.save()

            messages.success(request, '予定の作成が完了しました')

            return redirect('plan',planId=planObj.id)

    context = {
        'form':form,
    }

    return render(request,'core/edit.html',context)