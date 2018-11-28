from django.contrib import admin
from donaciones import models


# Register your models here.
admin.site.register(models.Family)
admin.site.register(models.Donation)
admin.site.register(models.DetailsDonation)
admin.site.register(models.TypesDonation)
admin.site.register(models.Neighborhood)
admin.site.register(models.TypesProducts)
admin.site.register(models.SortProducts)
admin.site.register(models.FamilyEntry)
