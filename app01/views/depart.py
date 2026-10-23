from django.shortcuts import render, redirect
from app01 import models


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()
    return render(request, "depart_list.html", {"queryset": queryset})


def depart_add(request):
    """新建部门"""
    if request.method == "GET":
        return render(request, "depart_add.html")

    title = request.POST.get("title")
    if title:
        models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """编辑部门"""
    row_object = models.Department.objects.filter(id=nid).first()
    if request.method == "GET":
        return render(request, "depart_edit.html", {"row_object": row_object})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def depart_delete(request, nid):
    """删除部门"""
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")
