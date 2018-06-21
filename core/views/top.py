from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import User, UserData, Plan, PlanDetail,Mob
from core.forms import MobForm

def topView(request):
    return render(request,'core/top.html')