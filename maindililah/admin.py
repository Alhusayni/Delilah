from django.contrib import admin
from maindililah import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Neighborhood)
admin.site.register(models.UsersReview)
admin.site.register(models.ReplyReview)
admin.site.register(models.ReportReview)
admin.site.register(models.ReportReply)