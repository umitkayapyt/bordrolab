from django.db import models


class SelectListeleri(models.Model):
    dynamic_select_kanun = models.JSONField(default=list, blank=True)
    dynamic_select_ucret = models.JSONField(default=list, blank=True)
    dynamic_select_yil = models.JSONField(default=list, blank=True)
    dynamic_select_statu = models.JSONField(default=list, blank=True)
    dynamic_select_engelli = models.JSONField(default=list, blank=True)
    dynamic_select_egitim = models.JSONField(default=list, blank=True)
    dynamic_select_agi = models.JSONField(default=list, blank=True)

    def __str__(self):
        return "Select"


class WageParameters(models.Model):
    year = models.IntegerField(unique=True)
    
    # Birinci Dönem Verileri
    Birinci_Donem_Net_Asgari_Ucret = models.FloatField()
    Birinci_Donem_Brut_Ucret_Taban = models.FloatField() 
    Birinci_Donem_Birinci_Vergi_Dilimi = models.FloatField()
    Birinci_Donem_Ikinci_Vergi_Dilimi = models.FloatField()
    Birinci_Donem_Ucuncu_Vergi_Dilimi = models.FloatField()
    Birinci_Donem_Dorduncu_Vergi_Dilimi = models.FloatField()
    Birinci_Donem_Besinci_Vergi_Dilimi = models.FloatField()
    Birinci_Donem_Birinci_Derece_Engelli_Indirimi = models.FloatField()
    Birinci_Donem_Ikinci_Derece_Engelli_Indirimi = models.FloatField()
    Birinci_Donem_Ucuncu_Derece_Engelli_Indirimi = models.FloatField()
    Birinci_Donem_Brut_Ucret_Tavan = models.FloatField()
    
    # İkinci Dönem Verileri
    Ikinci_Donem_Net_Asgari_Ucret = models.FloatField()
    Ikinci_Donem_Brut_Ucret_Taban = models.FloatField()
    Ikinci_Donem_Birinci_Vergi_Dilimi = models.FloatField()
    Ikinci_Donem_Ikinci_Vergi_Dilimi = models.FloatField(2)
    Ikinci_Donem_Ucuncu_Vergi_Dilimi = models.FloatField()
    Ikinci_Donem_Dorduncu_Vergi_Dilimi = models.FloatField()
    Ikinci_Donem_Besinci_Vergi_Dilimi = models.FloatField()
    Ikinci_Donem_Birinci_Derece_Engelli_Indirimi = models.FloatField()
    Ikinci_Donem_Ikinci_Derece_Engelli_Indirimi = models.FloatField()
    Ikinci_Donem_Ucuncu_Derece_Engelli_Indirimi = models.FloatField(2)
    Ikinci_Donem_Brut_Ucret_Tavan = models.FloatField()

    def __str__(self):
        return f"{self.year}"
     

class Bordro(models.Model):
    session_key = models.CharField(max_length=255, db_index=True, default='default_session_key')
    time_stamp_key = models.CharField(max_length=255, db_index=True, default='default_time_stamp_key')
    ay = models.CharField(max_length=50)
    Donem_Brut_Toplam = models.FloatField()
    Gunluk_Brut_Ucret = models.FloatField()
    SGK_matrah = models.FloatField()
    Isci_SGK = models.FloatField()
    Isci_Issizlik = models.FloatField()
    GVM = models.FloatField()
    KGVM = models.FloatField()
    gelir_vergisi = models.FloatField()
    damga_vergisi = models.FloatField()
    Net_Ucret = models.FloatField()
    Maas = models.FloatField()
    Isveren_SGK = models.FloatField()
    Isveren_Issizlik = models.FloatField()
    Normal_Maliyet = models.FloatField()
    Hazine_yardimi = models.FloatField()
    Hazine_Indirimi_Sonrasi_Maliyet = models.FloatField()
    Vergi_Odenecek = models.FloatField()
    Normal_SGK_Odenecek = models.FloatField()
    Hazine_Indirimi_Sonrasi_SGK_Odenecek = models.FloatField()
    agi = models.FloatField()
    GV_Istisna = models.FloatField()
    DV_Istisna = models.FloatField()
    Asg_GVM = models.FloatField()
    Kum_Asg_GV = models.FloatField()
    IkiAyOncekiDevir = models.FloatField()
    BirAyOncekiDevir = models.FloatField()
