# 联通员工管理系统（EMS）

基于 **Django 4.2 + MySQL + Bootstrap 3** 开发的轻量级员工管理系统，模拟联通公司内部管理后台，涵盖部门管理、员工管理、靓号管理三大核心模块。

---

## 功能模块

### 1. 部门管理
- 部门列表展示
- 新建部门（手动表单提交）
- 编辑部门信息
- 删除部门（级联删除关联员工）

### 2. 员工管理
- 员工列表展示（关联部门名称）
- 新建员工（ModelForm自动生成表单 + Bootstrap日期选择器）
- 编辑员工信息
- 删除员工
- 字段：姓名、密码、年龄、账户余额、入职时间、性别、所属部门

### 3. 靓号管理（核心模块）
- **列表展示**：分页显示靓号数据
- **搜索功能**：按手机号模糊搜索
- **新建靓号**：ModelForm + 正则校验手机号格式 + 数据库去重
- **编辑靓号**：排除自身后去重校验
- **删除靓号**：带确认提示
- **分页组件**：封装通用Pagination类，保留搜索条件翻页

---

## 技术栈

| 类别 | 技术 |
|---|---|
| 后端框架 | Django 4.2 |
| 数据库 | MySQL 8.0（通过PyMySQL连接） |
| 前端 | HTML + Bootstrap 3.4.1 + jQuery 3.6.0 |
| 日期插件 | bootstrap-datepicker |
| 架构模式 | MTV（Model-Template-View） |

---

## 项目结构

```
ems/
├── manage.py                 # Django项目入口
├── ems/                      # 项目配置目录
│   ├── __init__.py           # PyMySQL适配
│   ├── settings.py           # 项目配置（数据库、时区、静态文件）
│   ├── urls.py               # 全局路由
│   └── wsgi.py               # WSGI部署
├── app01/                    # 业务应用
│   ├── models.py             # 数据模型（Department/UserInfo/PrettyNum）
│   ├── forms.py              # ModelForm表单类
│   ├── views/                # 视图函数（按模块拆分）
│   │   ├── depart.py         # 部门管理视图
│   │   ├── user.py           # 用户管理视图
│   │   └── pretty.py         # 靓号管理视图
│   └── utils/                # 公共组件
│       ├── bootstrap.py      # BootStrapModelForm基类
│       └── pagination.py     # 通用分页组件
├── templates/                # HTML模板
│   ├── layout.html           # 母版（导航栏+公共资源）
│   ├── depart_list.html      # 部门列表
│   ├── depart_add.html       # 新建部门
│   ├── depart_edit.html      # 编辑部门
│   ├── user_list.html        # 员工列表
│   ├── user_add.html         # 新建员工
│   ├── user_edit.html        # 编辑员工
│   ├── pretty_list.html      # 靓号列表（搜索+分页）
│   ├── pretty_add.html       # 新建靓号
│   └── pretty_edit.html      # 编辑靓号
└── static/                   # 静态资源
    ├── js/jquery-3.6.0.min.js
    └── plugins/
        ├── bootstrap-3.4.1/  # Bootstrap CSS/JS/fonts
        └── bootstrap-datepicker/  # 日期选择器
```

---

## 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+
- pip

### 安装依赖
```bash
pip install django==4.2 pymysql
```

### 数据库配置
创建MySQL数据库：
```sql
CREATE DATABASE ems DEFAULT CHARSET utf8mb4;
```

修改 `ems/settings.py` 中的数据库连接：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ems',
        'USER': 'root',
        'PASSWORD': '你的密码',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 数据迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 启动项目
```bash
python manage.py runserver 127.0.0.1:8000
```

访问 http://127.0.0.1:8000/ ，自动跳转到部门列表页。

---

## 核心知识点

### 1. 模板继承
- 母版 `layout.html` 定义公共导航栏和资源引入
- 子页面用 `{% extends 'layout.html' %}` 继承
- `{% block content %}{% endblock %}` 填充页面独有内容

### 2. ModelForm组件
- 自动根据Model生成HTML表单
- 自动校验用户输入
- `form.save()` 自动写入数据库
- `BootStrapModelForm` 基类自动加Bootstrap样式

### 3. 正则校验 + 钩子方法
```python
mobile = forms.CharField(
    validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
)

def clean_mobile(self):
    # 额外业务校验：查数据库去重
    ...
```

### 4. ORM模糊搜索 + 动态传参
```python
data_dict = {}
if search_data:
    data_dict["mobile__contains"] = search_data
queryset = models.PrettyNum.objects.filter(**data_dict)
```

### 5. 通用分页组件
- QuerySet切片实现分页
- 保留搜索条件翻页
- 封装为Pagination类，各模块复用

### 6. choices字段
- 数据库存数字，页面显示中文
- 模板用 `{{ obj.get_field_display }}` 获取中文值

---

## 截图

（运行项目后可截图补充）

---

## License

MIT
