import django.utils.timezone as timezone
import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
############################################################################################################################################################
class UserModel(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(default="example@example.com")

class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }
############################################################################################################################################################
#改进建议提取
class NameModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要")
    detail = models.CharField(max_length=5000, verbose_name="详细描述")
    current_process = models.CharField(max_length=5000, verbose_name="处理进展",default="##由改进实施人填写##")
    #viewer_advice = models.CharField(max_length=5000, verbose_name="评审人意见",default="##由评审人填写##")
    value = models.CharField(max_length=200, default="0", verbose_name="改进价值评估")
    reviewer = models.CharField(max_length=200, default="#提交人填写#", verbose_name="改进建议评审人")
    executor = models.CharField(max_length=200, default="#由建议评审人指派#", verbose_name="改进建议实施人")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class NameForm(ModelForm):
    class Meta:
        model = NameModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':79}),
            'value' : forms.TextInput(attrs={'cols': 80, 'rows': 1}),
            'current_process' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'detail' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
helpmsg_imprvmt = [
    '【主干流程说明】:',
    '##{{环节，责任人}}##',
    '##<触发条件>##',
    '{{提交建议,创建人}}',
    '<提交评审>',
    '{{改进建议价值评审,改进建议评审人}}',
    '<指定实施人>',
    '{{改进建议实施,改建建议实施人}}',
    '<实施结果提交评审>',
    '{{实施结果评审,改进建议评审人}}',
    '<落地关闭>',
    '{{关闭}}'
]
############################################################################################################################################################
#实验室设备使用
class DeviceCardModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="设备描述")
    device_info = models.CharField(max_length=2000, verbose_name="设备信息", default="【归属小组】:")
    current_process = models.CharField(max_length=200, verbose_name="当前使用状态",default="##闲置OR使用##")
    occupied_by = models.CharField(max_length=200, default="#使用人更新#", verbose_name="设备使用人")
    assigned_to   = models.CharField(max_length=200, default="anyone", verbose_name="分配给(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class DeviceCardForm(ModelForm):
    class Meta:
        model = DeviceCardModel
        fields = '__all__'
        exclude = []#['curent_state','created_by']
        widgets = {
            'summary' : forms.TextInput(attrs={'size':50}),
            'device_info':forms.Textarea(attrs={'cols': 52, 'rows': 5}),
            'current_process' : forms.TextInput(attrs={'readonly': True,'size':20}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
DeviceManageAuth = {
    '访问权限':'Visit',
    '使用权限':'Exec',
}
DeviceManageGrp = {
    '管理员群组':'AdminGrp',  #Must in this format:'中文名':'English name'
    '用户群组':'UserGrp',
    '注册用户群组':'RegisteredUserGrp'
}
############################################################################################################################################################
#捷安特售后保养
BYCLE_TYPES_CHOICES = (
    ('TCR',(
            ('TCR 圆点', 'TCR 圆点'),
            ('TCR 环意粉', 'TCR 环意粉'),
            ('TCR SL', 'TCR SL'),
            ('TCR Pro Disc', 'TCR Pro Disc'),
            ('TCR Pro Team', 'TCR Pro Team'),
            ('TCR Pro 0', 'TCR Pro 0'),
            ('TCR Pro 1', 'TCR Pro 1'),
            ('TCR ADV 1', 'TCR ADV 1'),
            ('TCR ADV 2', 'TCR ADV 2'),
            ('TCR ADV 3', 'TCR ADV 3'),
            ('TCR 6700', 'TCR 6700'),
            ('TCR 6300', 'TCR 6300'),
        )
    ),
    ('Propel', (
            ('Propel ADV 1', 'Propel ADV 1'),
            ('Propel ADV 2', 'Propel ADV 2'),
            ('Propel ADV 3', 'Propel ADV 3'),
        )
    ),
    ('XTC', (
            ('XTC ADV 1', 'XTC ADV 1'),
            ('XTC ADV 2', 'XTC ADV 2'),
            ('XTC ADV 3', 'XTC ADV 3'),
            ('XTC SLR', 'XTC SLR'),
            ('XTC 880', 'XTC 880'),
            ('XTC 860', 'XTC 860'),
            ('XTC 820', 'XTC 820'),
            ('XTC 800', 'XTC 800'),
        )
    ),
    ('ATX', (
            ('ATX 850', 'ATX 850'),
            ('ATX 700', 'ATX 700'),
            ('ATX 610', 'ATX 610'),
        )
    ),
)
CHOICE_ORDER_TYPES = (
    ('维修调试','维修调试'),
    ('例行保养','例行保养'),
)
class GiantMaintainModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="QQ昵称")
    weixin  = models.CharField(max_length=200, verbose_name="微信号")
    custom_name = models.CharField(max_length=200, verbose_name="真实姓名", default='##请在此输入真实姓名##')
    device_info = models.CharField(max_length=2000, verbose_name="车辆型号", choices=BYCLE_TYPES_CHOICES)
    order_type = models.CharField(max_length=2000, verbose_name="预约类型", choices=CHOICE_ORDER_TYPES)
    buy_date = models.DateField(max_length=2000, verbose_name="购买日期", default=timezone.now)
    order_date = models.DateField(max_length=2000, verbose_name="预约日期", default=timezone.now,help_text='填写预约的进行维保的日期')
    more_info = models.CharField(max_length=9000, verbose_name="备注",default="##简要描述需要处理的单车问题##")
    assigned_to   = models.CharField(max_length=200, default="anyone", verbose_name="分配给(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class GiantMaintainForm(ModelForm):
    class Meta:
        model = GiantMaintainModel
        fields = '__all__'
        exclude = []#['curent_state','created_by']
        widgets = {
            'summary' : forms.TextInput(attrs={'size':50}),
            'weixin' : forms.TextInput(attrs={'size':50}),
            'custom_name' : forms.TextInput(attrs={'size':50}),
            'more_info' : forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
GiantMaintainAuth = {
    'visit':{'role':['Creator','Administrator','Processor']},
}
GiantMaintainGrp = {
    '用户群组':'UserGrp',
    '注册用户群组':'RegisteredUserGrp'
}
############################################################################################################################################################
#上市保障问题跟踪
CHOICE_CUSTOMER_TYPE = (
    ('jinrong','金融'),
    ('dianli','电力'),
    ('nengyuan','能源'),
    ('guangdian','广电'),
    ('meizi','媒资'),
    ('tezhong','特种行业'),
    ('neibu','内部客户'),
    ('其他','其他'),
)

CHOICE_ISSUE_CLASS_1 = (
    ('软件','软件'),
    ('硬件','硬件'),
    ('结构','结构'),
    ('误操作','误操作'),
    ('配置','配置'),
    ('兼容性','兼容性'),
    ('沟通协作','沟通协作'),
)
CHOICE_ISSUE_LEVEL = (
    ('一级事故','一级事故'),
    ('二级事故','二级事故'),
    ('三级事故','三级事故'),
    ('一级ITR','一级ITR'),
    ('二级ITR','二级ITR'),
    ('三级ITR','三级ITR'),
    ('A级重大问题','A级重大问题'),
    ('B级重大问题','B级重大问题'),
    ('C级重大问题','C级重大问题'),
    ('一般问题','一般问题'),
)

CHOICE_ISSUE_CLASS_2 = (
    ('软件', (
            ('FC', 'FC'),
            ('SAS', 'SAS'),
            ('固件', '固件'),
            ('压缩', '压缩'),
        )
    ),
    ('硬件', (
            ('内存', '内存'),
            ('板卡', '板卡'),
            ('线缆', '线缆'),
        )
    ),
    ('误操作', '误操作'),
    ('结构', '结构'),
    ('配置', '配置'),
    ('兼容性','兼容性'),
    ('沟通协作', '沟通协作'),
)


RESPONSE_FIELD_CHOICES = (
    ('软件', (
            ('FC', 'FC'),
            ('SAS', 'SAS'),
            ('固件', '固件'),
            ('压缩', '压缩'),
        )
    ),
    ('硬件', (
            ('内存', '内存'),
            ('板卡', '板卡'),
            ('线缆', '线缆'),
        )
    ),
)
class IssueTrackModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要", default="【20170101】XX局点XX设备发生XX问题")
    detail = models.CharField(max_length=5000, verbose_name="详细描述")
    current_process = models.CharField(max_length=5000, verbose_name="处理进展",default="##由维护处理人填写##")
    issue_level = models.CharField(max_length=200, verbose_name="问题级别", choices= CHOICE_ISSUE_LEVEL)
    #viewer_advice = models.CharField(max_length=5000, verbose_name="评审人意见",default="##由评审人填写##")
    customer_type = models.CharField(max_length=200,  verbose_name="客户类别", choices=CHOICE_CUSTOMER_TYPE)  #default="#金融/电力/能源/广电/媒资#", verbose_name="客户类别")
    class_1 = models.CharField(max_length=200, verbose_name="问题大类", choices= CHOICE_ISSUE_CLASS_1)
    class_2 = models.CharField(max_length=200, verbose_name="问题小类", choices= CHOICE_ISSUE_CLASS_2)
    class_3 = models.CharField(max_length=200, verbose_name="责任领域", choices= RESPONSE_FIELD_CHOICES)
    buglist_url = models.CharField(max_length=200, default="#Buglist单链接(若有)#", verbose_name="Buglist链接(URL)")
    improvement_url = models.CharField(max_length=200, default="#改进单链接(若有)#", verbose_name="改进项链接(URL)")
    issue_processor = models.CharField(max_length=200, default="#提交人填写#", verbose_name="维护处理人")
    issue_checkor = models.CharField(max_length=200, default="#维护处理人指定#", verbose_name="维护代表")
    issue_se = models.CharField(max_length=200, default="#维护代表指定#", verbose_name="改进提取SE")
    attachedfile = models.FileField(upload_to='djangofile/', verbose_name="附件", null=True, blank=True)
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class IssueTrackForm(ModelForm):
    class Meta:
        model = IssueTrackModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':79}),
            'current_process' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'detail' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'buglist_url' : forms.TextInput(attrs={'size':79}),
            'improvement_url' : forms.TextInput(attrs={'size':79}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }

IssueTrackAuth = {
    '访问权限':'IssueTrackVisit',
    '使用权限':'IssueTrackExec',
}
IssueTrackGrp = {
    '管理员群组':'AdminGrp',  #Must in this format:'中文名':'English name'
    '用户群组':'UserGrp',
    '注册用户群组':'RegisteredUserGrp'
}
############################################################################################################################################################
#OAK_ESS早期支持策略_订单支持
#项目	主要工作内容	客户名称	订单数量	软件版本	负责人	转维负责人	完成日期	当前进展

class ESS_OrderSupportModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="项目")
    content = models.CharField(max_length=5000, verbose_name="主要工作内容")
    customer = models.CharField(max_length=200, verbose_name="客户名称")
    order_number = models.CharField(max_length=200, default="0", verbose_name="订单数量")
    software_ver = models.CharField(max_length=200, default="0", verbose_name="软件版本")
    responser = models.CharField(max_length=200, default="0", verbose_name="负责人")
    responser_to_maitain = models.CharField(max_length=200, default="0", verbose_name="转维负责人")
    deadline = models.CharField(max_length=200, default="0", verbose_name="完成日期")
    current_process = models.CharField(max_length=5000, verbose_name="当前进展",default="##在此更新进展##")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class ESS_OrderSupportForm(ModelForm):
    class Meta:
        model = ESS_OrderSupportModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':78}),
            'customer' : forms.TextInput(attrs={'size':78}),
            'current_process' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            'content' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
############################################################################################################################################################
#OAK_ESS早期支持策略_客诉问题
class ESS_CustomerIssueModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="项目")
    content = models.CharField(max_length=5000, verbose_name="主要工作内容")
    customer = models.CharField(max_length=200, verbose_name="客户名称")
    order_number = models.CharField(max_length=200, default="0", verbose_name="订单数量")
    software_ver = models.CharField(max_length=200, default="0", verbose_name="软件版本")
    responser = models.CharField(max_length=200, default="0", verbose_name="负责人")
    responser_to_maitain = models.CharField(max_length=200, default="0", verbose_name="转维负责人")
    deadline = models.CharField(max_length=200, default="0", verbose_name="完成日期")
    current_process = models.CharField(max_length=5000, verbose_name="当前进展",default="##在此更新进展##")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class ESS_CustomerIssueForm(ModelForm):
    class Meta:
        model = ESS_CustomerIssueModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':78}),
            'customer' : forms.TextInput(attrs={'size':78}),
            'current_process' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            'content' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
############################################################################################################################################################
#OAK_ESS早期支持策略_供货支撑协调
class ESS_SupplySpportModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="项目")
    content = models.CharField(max_length=5000, verbose_name="主要工作内容")
    customer = models.CharField(max_length=200, verbose_name="客户名称")
    order_number = models.CharField(max_length=200, default="0", verbose_name="订单数量")
    software_ver = models.CharField(max_length=200, default="0", verbose_name="软件版本")
    responser = models.CharField(max_length=200, default="0", verbose_name="负责人")
    responser_to_maitain = models.CharField(max_length=200, default="0", verbose_name="转维负责人")
    deadline = models.CharField(max_length=200, default="0", verbose_name="完成日期")
    current_process = models.CharField(max_length=5000, verbose_name="当前进展",default="##在此更新进展##")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class ESS_SupplySpportForm(ModelForm):
    class Meta:
        model = ESS_SupplySpportModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':78}),
            'customer' : forms.TextInput(attrs={'size':78}),
            'current_process' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            'content' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
############################################################################################################################################################
#OAK_ESS版本控制策略_主线同步
class ESS_MasterBranchSyncModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="项目")
    content = models.CharField(max_length=5000, verbose_name="主要工作内容")
    responser = models.CharField(max_length=200, default="0", verbose_name="负责人")
    responser_to_maitain = models.CharField(max_length=200, default="0", verbose_name="转维负责人")
    deadline = models.CharField(max_length=200, default="0", verbose_name="完成日期")
    current_process = models.CharField(max_length=5000, verbose_name="当前进展",default="##在此更新进展##")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class ESS_MasterBranchSyncForm(ModelForm):
    class Meta:
        model = ESS_MasterBranchSyncModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':78}),
            'current_process' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            'content' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
############################################################################################################################################################
#OAK_ESS版本控制策略_遗留BUG解决
class ESS_LeftBugSolveModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="项目")
    content = models.CharField(max_length=5000, verbose_name="主要工作内容")
    responser = models.CharField(max_length=200, default="0", verbose_name="负责人")
    responser_to_maitain = models.CharField(max_length=200, default="0", verbose_name="转维负责人")
    deadline = models.CharField(max_length=200, default="0", verbose_name="完成日期")
    current_process = models.CharField(max_length=5000, verbose_name="当前进展",default="##在此更新进展##")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class ESS_LeftBugSolveForm(ModelForm):
    class Meta:
        model = ESS_LeftBugSolveModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':78}),
            'current_process' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            'content' : forms.Textarea(attrs={'cols': 66, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
help_msg = ['帮助信息：','段落一','段落二','段落三']
############################################################################################################################################################
#OAK_ESS早期支持策略_供货支撑协调
############################################################################################################################################################
#OAK_版本发布
release_note_msg="##此处按小组填写版本release notes##\n【Driver】:\n1.xxx\n2.xxx\n【EN】:\n1.xxx\n2.xxx\n"
fw_ver_info="【BIOS】:\n【8733】:\n【8796】:\n【BMC】:\n【NODE_CPLD】:\n【CMC】:\n【CMC_CPLD】:\n"
VER_PRJ_CHOICE = (
    ('OAK','OAK'),
    ('Bamboo','Bamboo')
)

class VerReleaseModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="版本号")
    commit_id = models.CharField(max_length=200, verbose_name="git_commit_id")
    release_date = models.DateField(max_length=2000, verbose_name="发布日期", default=timezone.now)
    prj_name = models.CharField(max_length=100, verbose_name="项目", choices=VER_PRJ_CHOICE)
    build_info = models.CharField(max_length=9000, verbose_name="构建信息",default="##此处填写构建信息，可从上一个版本拷贝进行修改##")
    release_notes = models.CharField(max_length=9000, verbose_name="release_notes",default=release_note_msg)
    fw_info = models.CharField(max_length=900, verbose_name="固件信息",default=fw_ver_info)
    assigned_to   = models.CharField(max_length=200, default="anyone", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class VerReleaseForm(ModelForm):
    class Meta:
        model = VerReleaseModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':68}),
            'commit_id' : forms.TextInput(attrs={'size':68}),
            'build_info' : forms.Textarea(attrs={'cols': 77, 'rows':15}),
            'release_notes' : forms.Textarea(attrs={'cols': 77, 'rows':15}),
            'fw_info' : forms.Textarea(attrs={'cols': 77, 'rows':8}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
VerReleaseHelpMsg = ['发布前点击\'更新信息\'按钮更新版本信息，发布后点击\'发布\'按钮，随后信息归档，不可更改']

############################################################################################################################################################
#待办事项
class TodolistModel(models.Model):
    summary = models.CharField(max_length=200, verbose_name="概要")
    detail = models.CharField(max_length=5000, verbose_name="详细描述")
    current_process = models.CharField(max_length=5000, verbose_name="处理进展",default="##此处填写进展##")
    assigned_to   = models.CharField(max_length=200, default="", verbose_name="当前处理人(只读)")
    created_by = models.CharField(max_length=200, default="", verbose_name="创建人(只读)")
    curent_state = models.CharField(max_length=200, verbose_name="当前状态(只读)")

class TodolistForm(ModelForm):
    class Meta:
        model = TodolistModel
        fields = '__all__'
        widgets = {
            'summary' : forms.TextInput(attrs={'size':79}),
            'current_process' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            #'viewer_advice' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'detail' : forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'assigned_to': forms.TextInput(attrs={'readonly': True,'size':20}),
            'created_by': forms.TextInput(attrs={'readonly': True}),
            'curent_state': forms.TextInput(attrs={'readonly': True}),
        }
helpmsg_totolist = [
    '【主干流程说明】:',
    '##{{环节，责任人}}##',
    '##<触发条件>##',
    '{{打开,创建人}}',
    '<提交评审>',
    '{{改进建议价值评审,改进建议评审人}}',
    '<指定实施人>',
    '{{改进建议实施,改建建议实施人}}',
    '<实施结果提交评审>',
    '{{实施结果评审,改进建议评审人}}',
    '<落地关闭>',
    '{{关闭}}'
]



############################################################################################################################################################
PRJ_NAME_LIST = [
     'improvement', 'device_card', 'giant_maintain', 'issue_track', 'ESS_OrderSupport',
     'ESS_CustomerIssue', 'ESS_SupplySpport', 'ESS_MasterBranchSync', 'ESS_LeftBugSolve',
     'VerRelease','Todolist'
]
FormAndModelDict = {
    'improvement':{'PrjNameZh':'改进建议','PrjModelClass':NameModel,'PrjFormClass':NameForm,'help_msg':helpmsg_imprvmt},
    'device_card':{'PrjNameZh':'设备管理','PrjModelClass':DeviceCardModel,'PrjFormClass':DeviceCardForm,'PrjAuth':DeviceManageAuth,'PrjGrp':DeviceManageGrp},
    'giant_maintain':{'PrjNameZh':'Giant维保预约','PrjModelClass':GiantMaintainModel,'PrjFormClass':GiantMaintainForm,'PrjAuth':GiantMaintainAuth,'PrjGrp':GiantMaintainGrp},
    'issue_track':{'PrjNameZh':'网上问题处理','PrjModelClass':IssueTrackModel,'PrjFormClass':IssueTrackForm,'PrjAuth':IssueTrackAuth,'PrjGrp':IssueTrackGrp},
    'ESS_OrderSupport':{'PrjNameZh':'OAK_ESS订单支持','PrjModelClass':ESS_OrderSupportModel,'PrjFormClass':ESS_OrderSupportForm},
    'ESS_CustomerIssue':{'PrjNameZh':'OAK_ESS客诉问题','PrjModelClass':ESS_CustomerIssueModel,'PrjFormClass':ESS_CustomerIssueForm},
    'ESS_SupplySpport':{'PrjNameZh':'OAK_ESS供货支持','PrjModelClass':ESS_SupplySpportModel,'PrjFormClass':ESS_SupplySpportForm},
    'ESS_MasterBranchSync':{'PrjNameZh':'OAK_ESS主线同步','PrjModelClass':ESS_MasterBranchSyncModel,'PrjFormClass':ESS_MasterBranchSyncForm},
    'ESS_LeftBugSolve':{'PrjNameZh':'OAK_ESS遗留BUG解决','PrjModelClass':ESS_LeftBugSolveModel,'PrjFormClass':ESS_LeftBugSolveForm,'help_msg':help_msg},
    'VerRelease':{'PrjNameZh':'转测版本记录','PrjModelClass':VerReleaseModel,'PrjFormClass':VerReleaseForm, 'help_msg':VerReleaseHelpMsg},
    'Todolist':{'PrjNameZh':'待办事项处理','PrjModelClass':TodolistModel,'PrjFormClass':TodolistForm} #, 'help_msg':VerReleaseHelpMsg}
}
