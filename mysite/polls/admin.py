from django.contrib import admin
from .models import Question
from .models import NameModel
from .models import DeviceCardModel
from .models import IssueTrackModel
# Register your models here.
admin.site.register(Question)
admin.site.register(NameModel)
admin.site.register(DeviceCardModel)
admin.site.register(IssueTrackModel)
