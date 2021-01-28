from django.contrib import admin
from .models import HistoryDrop, Quality, Item, RegItem, Case, UserProfile, Category, SiteConstructor
from .forms import QualityForm


class QualityAdmin(admin.ModelAdmin):
    form = QualityForm


admin.site.register(HistoryDrop)
admin.site.register(Quality,QualityAdmin)
admin.site.register(Item)
admin.site.register(RegItem)
admin.site.register(Case)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(SiteConstructor)