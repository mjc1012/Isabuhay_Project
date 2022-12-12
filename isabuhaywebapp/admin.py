from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(CBCTestResult)
admin.site.register(CBCTestResultImage)
admin.site.register(CBCTestResultPDF)
admin.site.register(CBCTestResultDocument)
admin.site.register(Promo)
admin.site.register(Payment)
admin.site.register(Room)
admin.site.register(Message)