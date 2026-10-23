# ============================================================
# 导入模块
# ============================================================
from django.utils.safestring import mark_safe    # 告诉Django这是安全HTML，不转义


# ============================================================
# 通用分页组件
# 用法：
#   queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-id")
#   page_object = Pagination(request, queryset)
#   context = {"queryset": page_object.page_queryset, "page_string": page_object.html()}
# ============================================================
class Pagination:
    """通用分页组件"""

    def __init__(self, request, queryset, page_size=10, plus=2):
        """
        参数说明：
            request:    HttpRequest对象，用来取URL中的page参数
            queryset:   全部数据（QuerySet），会自动切片
            page_size:  每页显示多少条，默认10条
            plus:       当前页前后显示几个页码，默认2个（显示 前2 当前 后2）
        """
        self.request = request
        self.page_size = page_size    # 每页条数
        self.plus = plus              # 页码前后显示范围

        # ---- 第1步：获取当前页码 ----
        try:
            # 从URL取?page=2，没传默认第1页
            self.page = int(request.GET.get("page", 1))
        except Exception:
            # 传了非数字（如?page=abc），默认第1页，不报错
            self.page = 1

        # 页码小于1时，强制为第1页
        if self.page < 1:
            self.page = 1

        # ---- 第2步：计算总条数和总页数 ----
        self.total_count = queryset.count()                              # 总记录数
        # 向上取整：(总数 + 每页条数 - 1) // 每页条数
        # 例如：25条数据，每页10条 → (25+10-1)//10 = 3页
        self.total_page_count = (self.total_count + self.page_size - 1) // self.page_size
        # 如果页码超过总页数，跳到最后一页
        if self.page > self.total_page_count:
            self.page = self.total_page_count if self.total_page_count >= 1 else 1

        # ---- 第3步：切片，只取当前页的数据 ----
        # 第1页：0~10条，第2页：10~20条
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size
        # Django QuerySet切片自动转成SQL的 LIMIT/OFFSET，不加载全部数据到内存
        self.page_queryset = queryset[self.start:self.end]

    def html(self):
        """生成分页按钮的HTML字符串（保留搜索条件）"""

        # ---- 保留搜索条件：复制当前URL的参数，去掉page ----
        # 例如当前URL是 ?q=138&page=2，去掉page后变成 q=138
        # 翻页时链接变成 ?q=138&page=3，搜索词不丢失
        query_dict = self.request.GET.copy()
        query_dict.pop("page", None)

        link_list = []   # 存所有分页按钮的HTML

        # ---- 首页 ----
        link_list.append(f'<li><a href="?{query_dict.urlencode()}&page=1">首页</a></li>')

        # ---- 上一页 ----
        if self.page > 1:
            prev = self.page - 1
            link_list.append(f'<li><a href="?{query_dict.urlencode()}&page={prev}">上一页</a></li>')
        else:
            # 已经是第一页，上一页按钮变灰不可点
            link_list.append('<li class="disabled"><a href="#">上一页</a></li>')

        # ---- 页码列表（只显示当前页前后plus个）----
        # 例如当前第5页，plus=2，显示 3 4 5 6 7
        start_page = max(1, self.page - self.plus)               # 最小不能小于1
        end_page = min(self.total_page_count, self.page + self.plus)  # 最大不能超过总页数

        for i in range(start_page, end_page + 1):
            if i == self.page:
                # 当前页高亮显示
                link_list.append(f'<li class="active"><a href="?{query_dict.urlencode()}&page={i}">{i}</a></li>')
            else:
                link_list.append(f'<li><a href="?{query_dict.urlencode()}&page={i}">{i}</a></li>')

        # ---- 下一页 ----
        if self.page < self.total_page_count:
            nxt = self.page + 1
            link_list.append(f'<li><a href="?{query_dict.urlencode()}&page={nxt}">下一页</a></li>')
        else:
            # 已经是最后一页，下一页按钮变灰
            link_list.append('<li class="disabled"><a href="#">下一页</a></li>')

        # ---- 尾页 ----
        link_list.append(f'<li><a href="?{query_dict.urlencode()}&page={self.total_page_count}">尾页</a></li>')

        # ---- 拼接成Bootstrap分页HTML，mark_safe告诉Django不转义 ----
        return mark_safe('<ul class="pagination">' + "".join(link_list) + "</ul>")
