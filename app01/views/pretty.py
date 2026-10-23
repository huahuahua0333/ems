# ============================================================
# 导入模块
# ============================================================
from django.shortcuts import render, redirect   # render渲染模板、redirect重定向
from app01 import models                         # 导入数据库模型
from app01.forms import PrettyModelForm, PrettyEditModelForm  # 导入靓号表单类
from app01.utils.pagination import Pagination    # 导入分页组件


# ============================================================
# 靓号列表页（搜索 + 分页）
# URL: /pretty/list/
# ============================================================
def pretty_list(request):
    """靓号列表（搜索 + 等级筛选 + 状态筛选 + 分页）"""

    # ---- 第1步：获取搜索关键词，动态拼接查询条件 ----
    data_dict = {}                                          # 空字典，存搜索条件
    search_data = request.GET.get("q", "")                 # 从URL取?q=xxx，没传默认空字符串
    if search_data:                                         # 如果用户输入了搜索词
        data_dict["mobile__contains"] = search_data        # 模糊搜索：手机号包含关键词

    # ---- 等级筛选：从URL取?level=1，没传默认空字符串 ----
    level_data = request.GET.get("level", "")
    if level_data:
        data_dict["level"] = level_data                     # 精确匹配等级

    # ---- 状态筛选：从URL取?status=1，没传默认空字符串 ----
    status_data = request.GET.get("status", "")
    if status_data:
        data_dict["status"] = status_data                   # 精确匹配状态

    # ---- 第2步：查询数据库，按ID倒序（最新的排前面）----
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-id")
    # **data_dict：把字典拆成关键字参数，等价于 filter(mobile__contains="xxx")
    # order_by("-id")：负号表示倒序

    # ---- 第3步：实例化分页组件，自动切片取当前页数据 ----
    page_object = Pagination(request, queryset)

    # ---- 第4步：组装上下文传给模板 ----
    context = {
        "queryset": page_object.page_queryset,   # 当前页的数据（不是全部数据）
        "search_data": search_data,              # 搜索词，回填到输入框
        "level_data": level_data,                 # 选中的等级，回填下拉框
        "status_data": status_data,               # 选中的状态，回填下拉框
        "page_string": page_object.html(),       # 分页按钮的HTML代码
    }
    return render(request, "pretty_list.html", context)


# ============================================================
# 新建靓号
# URL: /pretty/add/
# ============================================================
def pretty_add(request):
    """新建靓号"""

    # ---- GET请求：用户打开新建页面，返回空表单 ----
    if request.method == "GET":
        form = PrettyModelForm()                            # 实例化空表单
        return render(request, "pretty_add.html", {"form": form})

    # ---- POST请求：用户提交表单，校验并保存 ----
    form = PrettyModelForm(data=request.POST)              # 用POST数据构造表单
    if form.is_valid():                                     # 自动校验（正则+钩子）
        form.save()                                         # 校验通过，写入数据库
        return redirect("/pretty/list/")                    # 重定向回列表页
    # 校验失败，form里有错误信息，返回页面展示错误
    return render(request, "pretty_add.html", {"form": form})


# ============================================================
# 编辑靓号
# URL: /pretty/<int:nid>/edit/
# ============================================================
def pretty_edit(request, nid):
    """编辑靓号"""

    # ---- 第1步：根据URL中的ID，查出要编辑的那条记录 ----
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if not row_object:                                      # 如果查不到，直接跳回列表
        return redirect("/pretty/list/")

    # ---- GET请求：把已有数据填充到表单，让用户看到原值 ----
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)     # instance= 把已有数据塞进表单
        return render(request, "pretty_edit.html", {"form": form})

    # ---- POST请求：用户提交修改，校验并更新数据库 ----
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    # instance=row_object 告诉ModelForm这是更新（不是新建），save()时执行UPDATE
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


# ============================================================
# 删除靓号
# URL: /pretty/<int:nid>/delete/
# ============================================================
def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()       # 按ID删除
    return redirect("/pretty/list/")                       # 跳回列表页
