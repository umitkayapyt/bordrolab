from django.contrib import admin
from .models import SelectListeleri, WageParameters, Bordro


@admin.register(WageParameters)
class WageParametersAdmin(admin.ModelAdmin):
    list_display = ('year', 'Birinci_Donem_Net_Asgari_Ucret', 'Birinci_Donem_Brut_Ucret_Taban', 'Ikinci_Donem_Net_Asgari_Ucret', 'Ikinci_Donem_Brut_Ucret_Taban',)
    search_fields = ('year',)

@admin.register(SelectListeleri)
class SelectListeleriAdmin(admin.ModelAdmin):
    pass

@admin.register(Bordro)
class BordroAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'time_stamp_key',)