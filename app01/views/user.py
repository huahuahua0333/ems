from django.shortcuts import render, redirect
from app01 import models
from app01.forms import UserModelForm, UserEditModelForm


def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all()
    return render(request, "user_list.html", {"queryset": queryset})


def user_add(request):
    """新建用户（ModelForm）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/user/list/")

    if request.method == "GET":
        form = UserEditModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """删除用户"""
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
