from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import User, UserData, Plan, PlanDetail,Mob
from core.forms import MobForm


def planView(request, planId):
    planObj = Plan.objects.get(id=planId)
    planDetailObj = PlanDetail.objects.filter(plan=planObj).order_by('date')
    countX = []
    countO = []
    countN = []
    allStartTime = 95
    allEndTime = 0
    for p in planDetailObj:
        tempX = []
        tempO = []
        tempN = []
        startTime = p.startTime
        endTime = p.endTime

        if startTime != 0:
            for n in range(startTime):
                tempX.append(0)
                tempO.append(0)
                tempN.append(0)
        for n in range(startTime, endTime + 1):
            tempX.append(UserData.objects.filter(planDetail=p, status=UserData.STATUS_X, time=n).count())
            tempO.append(UserData.objects.filter(planDetail=p, status=UserData.STATUS_O, time=n).count())
            tempN.append(UserData.objects.filter(planDetail=p, status=UserData.STATUS_N, time=n).count())
        if endTime < 95:
            for n in range(endTime, 96):
                tempX.append(0)
                tempO.append(0)
                tempN.append(0)
        countX.append(tempX)
        countN.append(tempN)
        countO.append(tempO)

        if startTime < allStartTime:
            allStartTime = startTime
        if endTime > allEndTime:
            allEndTime = endTime

    allNum = Mob.objects.filter(plan=planObj).count()
    print(allNum)
    if allNum == 0:
        allNum = 1

    context = {
        'plan': planObj,
        'planDetails': planDetailObj,
        'countX': countX,
        'countO': countO,
        'countN': countN,
        'count': range(allStartTime//4, (allEndTime+1)//4),
        'allStartTime':allStartTime,
        'allEndTime':allEndTime+1,
        'frac':(allEndTime-allStartTime+1)%4,
        'allNum': allNum,
        'mobs': Mob.objects.filter(plan=planObj),
    }

    return render(request,'core/planView.html', context)


def planMobAddView(request, planId):
    planObj = Plan.objects.get(id=planId)
    form = MobForm()

    if request.method == 'POST':
        form = MobForm(request.POST)
        if form.is_valid():
            mobObj = Mob()
            mobObj.name = form.cleaned_data['name']
            mobObj.plan = planObj

            mobObj.save()

            return redirect('planMob', planId=planId, mobId=mobObj.id)

    context = {
        'form': form,
    }

    return render(request,'core/planMobAddView.html',context)


def planMobView(request, planId, mobId):
    planObj = Plan.objects.get(id=planId)
    planDetailObj = PlanDetail.objects.filter(plan=planObj).order_by('date')
    mobObj = Mob.objects.get(id=mobId)
    countX = []
    countO = []
    countN = []
    allStartTime = 95
    allEndTime = 0
    for p in planDetailObj:
        tempX = []
        tempO = []
        tempN = []
        startTime = p.startTime
        endTime = p.endTime

        if startTime != 0:
            for n in range(startTime):
                tempX.append(0)
                tempO.append(0)
                tempN.append(0)
        for n in range(startTime, endTime + 1):
            tempX.append(UserData.objects.filter(planDetail=p, status=UserData.STATUS_X, time=n, mob=mobObj).count())
            tempO.append(UserData.objects.filter(planDetail=p, status=UserData.STATUS_O, time=n, mob=mobObj).count())
            tempN.append(UserData.objects.filter(planDetail=p, status=UserData.STATUS_N, time=n, mob=mobObj).count())
        if endTime < 95:
            for n in range(endTime, 96):
                tempX.append(0)
                tempO.append(0)
                tempN.append(0)
        countX.append(tempX)
        countN.append(tempN)
        countO.append(tempO)

        if startTime < allStartTime:
            allStartTime = startTime
        if endTime > allEndTime:
            allEndTime = endTime

    allNum = 1

    context = {
        'plan': planObj,
        'planDetails': planDetailObj,
        'countX': countX,
        'countO': countO,
        'countN': countN,
        'count': range(allStartTime//4, (allEndTime+1)//4),
        'allStartTime':allStartTime,
        'allEndTime':allEndTime+1,
        'frac':(allEndTime-allStartTime+1)%4,
        'allNum': allNum,
        'mob': mobObj,
    }

    return render(request,'core/planMobView.html',context)


def planEditView(request, planDetailId,mobId,time):
    time = time - 1
    planDetailObj = PlanDetail.objects.get(id=planDetailId)
    mobObj = Mob.objects.get(id=mobId)

    try:
        userDataObj = UserData.objects.get(planDetail=planDetailObj,mob=mobObj,time=time,status=UserData.STATUS_O)
        userDataObj.delete()
    except:
        userDataObj = UserData()
        userDataObj.planDetail = planDetailObj
        userDataObj.mob = mobObj
        userDataObj.time = time
        userDataObj.status = UserData.STATUS_O

        userDataObj.save()

    return redirect('planMob',planId=planDetailObj.plan_id,mobId=mobId)