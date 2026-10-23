# ============================================================
# 导入模块
# ============================================================
from django import forms                                     # Django表单基类
from django.core.validators import RegexValidator            # 正则校验器
from django.core.exceptions import ValidationError          # 校验错误异常
from app01 import models                                     # 导入数据库模型
from app01.utils.bootstrap import BootStrapModelForm        # Bootstrap样式基类


# ============================================================
# 用户管理的ModelForm（略）
# ============================================================
class UserModelForm(BootStrapModelForm):
    """新建用户ModelForm"""
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        widgets = {
            "create_time": forms.DateInput(attrs={"type": "text", "id": "dt"}),
        }


class UserEditModelForm(BootStrapModelForm):
    """编辑用户ModelForm"""
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        widgets = {
            "create_time": forms.DateInput(attrs={"type": "text", "id": "dt"}),
        }


# ============================================================
# 新建靓号ModelForm
# 作用：自动生成新建靓号的表单HTML + 校验数据格式 + 查重
# ============================================================
class PrettyModelForm(BootStrapModelForm):
    """新建靓号ModelForm：手机号正则 + 钩子校验重复"""

    # ---- 自定义mobile字段：加正则校验 ----
    mobile = forms.CharField(
        label="手机号",
        # 正则：1开头，第二位3-9，后面9个数字，共11位
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    # ---- Meta内部类：绑定模型和字段 ----
    class Meta:
        model = models.PrettyNum                       # 绑定PrettyNum表
        fields = ["mobile", "price", "level", "status"]  # 显示这4个字段

    # ---- 钩子方法：Django自动调用，校验手机号是否已存在 ----
    def clean_mobile(self):
        """钩子方法：验证手机号是否已存在"""
        txt_mobile = self.cleaned_data["mobile"]       # 取校验后的手机号
        # 查数据库：这个手机号是否已存在
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")     # 抛错误，页面显示
        return txt_mobile                              # 返回正确值


# ============================================================
# 编辑靓号ModelForm
# 和新建的区别：查重时要排除自己，不然不改手机号也会报"已存在"
# ============================================================
class PrettyEditModelForm(BootStrapModelForm):
    """编辑靓号ModelForm：手机号正则 + 钩子排除自身后校验重复"""

    # ---- 同样的正则校验 ----
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    # ---- 钩子方法：排除自己后再查重 ----
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # exclude(id=self.instance.pk)：排除当前正在编辑的这条记录
        # self.instance.pk = 正在编辑的那条靓号的ID
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile
