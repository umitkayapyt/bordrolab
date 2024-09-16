from django import forms
from .models import SelectListeleri

class SalaryForm(forms.Form):
    year = forms.ChoiceField(choices=[])
    kanun = forms.ChoiceField(choices=[])
    ucretType = forms.ChoiceField(choices=[])
    statu = forms.ChoiceField(choices=[])
    engelli_durumu = forms.ChoiceField(choices=[])
    egitim_durumu = forms.ChoiceField(choices=[])
    AGI_durumu = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
        
        # Veri tabanındaki ilk kaydı çekiyoruz
        secim_listesi = SelectListeleri.objects.first()

        # Seçim listelerini form alanlarına dolduruyoruz
        self.fields['year'].choices = [(yil, yil) for yil in secim_listesi.dynamic_select_yil]
        self.fields['kanun'].choices = [(kanun, kanun) for kanun in secim_listesi.dynamic_select_kanun]
        self.fields['ucretType'].choices = [(ucret, ucret) for ucret in secim_listesi.dynamic_select_ucret]
        self.fields['statu'].choices = [(statu, statu) for statu in secim_listesi.dynamic_select_statu]
        self.fields['engelli_durumu'].choices = [(engelli, engelli) for engelli in secim_listesi.dynamic_select_engelli]
        self.fields['egitim_durumu'].choices = [(egitim, egitim) for egitim in secim_listesi.dynamic_select_egitim]
        self.fields['AGI_durumu'].choices = [(agi, agi) for agi in secim_listesi.dynamic_select_agi]
