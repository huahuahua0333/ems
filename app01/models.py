from django.db import models

# 部门表
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name="部门名称")

    def __str__(self):
        return self.title

# 员工表
class UserInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name="姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="账户")
    create_time = models.DateField(verbose_name="创建时间")
    # 外键：关联Depart，on_delete=SET_NULL 部门删除时 depart_id置空
    depart = models.ForeignKey(
        to="Department",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name="所属部门"
    )
    # gender 1男，2女
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name="性别")

    def __str__(self):
        return self.name


# 靓号表
class PrettyNum(models.Model):
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    price = models.IntegerField(default=0, verbose_name="价格")

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="级别")

    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(choices=status_choices, default=2, verbose_name="状态")

    def __str__(self):
        return self.mobile
