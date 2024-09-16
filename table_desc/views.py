from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from . import forms
from table_desc.models import Bordro, WageParameters
from .taxes._pipeLine import data_Pipeline
from time import time
from random import randint
from hashlib import md5




def index(request):
    month_data = get_month_data()
    select_listesi  = forms.SalaryForm()
    context = {
        'month_names': month_data,
        'select_listesi': select_listesi,
    }
    return render(request, 'desc/index.html', context)

################################################################# FORMS ########################################################################

# Checkbox değerlerini almak için
def get_checkbox_value(request, field_name):
    """Checkbox değerini alır ve True/False döner"""
    return request.POST.get(field_name) == 'on'

# Formdan gelen verileri almak için
def get_post_value(request, field_name, default=None):
    """Form verilerini alır, eğer boş ise varsayılan değeri döner"""
    return request.POST.get(field_name, default)

# Tek seferde hem listeyi, hem sözlüğü, hem de backend için format dönen fonksiyon
def get_form_data_as_list_and_dict(request, prefix):
    """Veriyi hem liste hem de sözlük olarak döner"""
    form_list = [request.POST.get(f'{prefix}_{i}', '') for i in range(1, 13)]
    form_dict = {i + 1: value for i, value in enumerate(form_list)}
    pipeline  = [convert_to_numeric(request.POST.get(f'{prefix}_{i}', '')) for i in range(1, 13)] 
    return form_list, form_dict, pipeline

# disabled durumları  
def get_disabled_list(request, prefix):
    """disabled durumlarını alır liste döner"""
    return [request.POST.get(f'{prefix}_{i}_disabled') == 'on' for i in range(1, 13)]

# geri döndürülen form
def prepare_context(request):
    """Tüm form verilerini toplayıp context için hazırlar"""

    ucret_listesi_forms_list, ucret_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'salary')
    prim_listesi_forms_list, prim_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'bonus')
    fm_listesi_forms_list, fm_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'shift')
    ubgt_listesi_forms_list, ubgt_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'UBGT')
    sgkgun_listesi_forms_list, sgkgun_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'day')
    argegun_listesi_forms_list, argegun_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'arge_day')
    KGVM_listesi_forms_list, KGVM_listesi_forms_dict, _ = get_form_data_as_list_and_dict(request, 'gecmis_KGVM')

    month_data = get_month_data()
    select_listesi  = forms.SalaryForm(request.POST)
    
    return {
        'month_names': month_data, # aylar ve index
        'year': get_post_value(request, 'year'), # select seçili
        'ucretType': get_post_value(request, 'ucretType'), # select seçili
        'statu': get_post_value(request, 'statu'), # select seçili
        'kanun': get_post_value(request, 'kanun'), # select seçili
        'engelli_durumu': get_post_value(request, 'engelli_durumu'), # select seçili
        'egitim_durumu': get_post_value(request, 'egitim_durumu'), # select seçili
        'AGI_durumu' :get_post_value(request, 'AGI_durumu'), # select seçili

        'agi_dahil': get_checkbox_value(request, 'agi_dahil'), # checbox durum
        'net_sabit': get_checkbox_value(request, 'net_sabit'), # checbox durum
        'linyit': get_checkbox_value(request, 'linyit'), # checbox durum
        'vergi_yok': get_checkbox_value(request, 'vergi_yok'), # checbox durum
        
        'ucret_listesi_forms': ucret_listesi_forms_dict, # input x 12
        'prim_listesi_forms': prim_listesi_forms_dict, # input x 12
        'fm_listesi_forms': fm_listesi_forms_dict, # input x 12
        'ubgt_listesi_forms': ubgt_listesi_forms_dict, # input x 12
        'sgkgun_listesi_forms': sgkgun_listesi_forms_dict, # input x 12
        'argegun_listesi_forms': argegun_listesi_forms_dict, # input x 12
        'KGVM_listesi_forms': KGVM_listesi_forms_dict, # input x 12

        # Disable listeleri
        'shift_disabled_list': get_disabled_list(request, 'shift'),
        'UBGT_disabled_list': get_disabled_list(request, 'UBGT'),
        'arge_day_disabled_list': get_disabled_list(request, 'arge_day'),

        'select_listesi': select_listesi, # default listeler

        'ucret_listesi_forms_list': ucret_listesi_forms_list,
        'prim_listesi_forms_list': prim_listesi_forms_list,
        'fm_listesi_forms_list': fm_listesi_forms_list,
        'ubgt_listesi_forms_list': ubgt_listesi_forms_list,
        'sgkgun_listesi_forms_list': sgkgun_listesi_forms_list,
        'argegun_listesi_forms_list': argegun_listesi_forms_list,
        'KGVM_listesi_forms_list': KGVM_listesi_forms_list,
    }

# render
def process_salary_form(request):
    input_context = prepare_context(request)
    
    if request.method == 'POST':
        ucret_listesi = convert_to_numeric(input_context['ucret_listesi_forms_list'])
        prim_listesi= convert_to_numeric(input_context['prim_listesi_forms_list'])
        fm_listesi = convert_to_numeric(input_context['fm_listesi_forms_list'])
        ubgt_listesi = convert_to_numeric(input_context['ubgt_listesi_forms_list'])
        sgkgun_listesi = convert_to_numeric(input_context['sgkgun_listesi_forms_list']) # 0 değilse float olmalı
        argegun_listesi = convert_to_numeric(input_context['argegun_listesi_forms_list']) # 0 değilse float olmalı
        KGVM_listesi = convert_to_numeric(input_context['KGVM_listesi_forms_list'])

        # Oturum işlemleri
        if not request.session.session_key:
            request.session.create()
        
        time_stamp_id = generate_unique_id()

        session_id = request.session.session_key
        engelli_derece, engelli_durumu = get_engelli_derece(input_context['engelli_durumu'])
        AGI_durumu = get_agi_durumu(input_context['AGI_durumu'])
        combo_list = [
            input_context['kanun'],
            input_context['ucretType'],
            input_context['statu'],
            engelli_durumu,
            engelli_derece,
            input_context['net_sabit'],
            AGI_durumu,
            input_context['year'],
            input_context['agi_dahil'],
            input_context['linyit'],
            input_context['vergi_yok'],
            input_context['egitim_durumu'],
            session_id,
            time_stamp_id
        ]

        data_lists = [ucret_listesi, prim_listesi, fm_listesi, ubgt_listesi, sgkgun_listesi, argegun_listesi, KGVM_listesi]
        data_Pipeline(*data_lists, combo_list)

        output_bordro = Bordro.objects.filter(session_key=session_id, time_stamp_key=time_stamp_id)
        bordro_list = list(output_bordro.values())

        combined_list = zip(input_context['month_names'], bordro_list)
        # Context birleştirme
        context = {**input_context, 'combined_list': combined_list}

        delete_table(session_id, time_stamp_id) # tabloyu sil, veri tabanı temiz

        return render(request, 'desc/process_salary_form.html', context)
        
    else:
        return render(request, 'desc/index.html', input_context) # burada mevcut select verileri DB'den geliyor.

########################################################### data preparing #####################################################################

# Engelli derecesi haritasını oluşturmak için
def get_engelli_derece(engelli_durumu):
    """Engelli derecesini alır ve haritadan değer döner"""
    engelli_derece_map = {
        'Hayır': 4,
        '1. Derece': 0,
        '2. Derece': 1,
        '3. Derece': 2
    }
    durumu = 'Hayır' if engelli_durumu == 'Hayır' else 'Evet'

    return engelli_derece_map.get(engelli_durumu, 0), durumu

# AGI durumunu almak için
def get_agi_durumu(AGI_durumu):
    """AGI durumu için evli, eş çalışıyor mu ve çocuk sayısını döner"""
    agi_durum_map = {
        'BEKAR': (False, False, 0),
        'EVLİ EŞİ ÇALIŞMAYAN': (True, True, 0),
        'EVLİ EŞİ ÇALIŞMAYAN 1 ÇOCUKLU': (True, True, 1),
        'EVLİ EŞİ ÇALIŞMAYAN 2 ÇOCUKLU': (True, True, 2),
        'EVLİ EŞİ ÇALIŞMAYAN 3 ÇOCUKLU': (True, True, 3),
        'EVLİ EŞİ ÇALIŞMAYAN 4 ÇOCUKLU': (True, True, 4),
        'EVLİ EŞİ ÇALIŞMAYAN 5 ÇOCUKLU': (True, True, 5),
        'EVLİ EŞİ ÇALIŞAN': (True, False, 0),
        'EVLİ EŞİ ÇALIŞAN 1 ÇOCUKLU': (True, False, 1),
        'EVLİ EŞİ ÇALIŞAN 2 ÇOCUKLU': (True, False, 2),
        'EVLİ EŞİ ÇALIŞAN 3 ÇOCUKLU': (True, False, 3),
        'EVLİ EŞİ ÇALIŞAN 4 ÇOCUKLU': (True, False, 4),
        'EVLİ EŞİ ÇALIŞAN 5 ÇOCUKLU': (True, False, 5),
    }
    return list(agi_durum_map.get(AGI_durumu, (False, False, 0)))

def convert_to_numeric(values):
    """Sayısal değerlerin ondalık durumlarını ve binlik ayrıcılarını düzenler"""
    def convert_single_value(value):
        if value:
            value = value.strip().replace('.', '').replace(',', '.')
            if '.' in value:
                try:
                    return float(value)
                except ValueError:
                    return 0.0
            else:
                try:
                    return int(value)
                except ValueError:
                    return 0
        return 0

    # Liste içerisindeki her bir öğeyi dönüştür
    if isinstance(values, list):
        return [convert_single_value(value) for value in values]
    else:
        return convert_single_value(values)

def generate_unique_id():
    """Ziyaretçilerin hesaplamalarında karışıklık olmaması için benzersizlik ayrımı"""
    # Anlık zamanın alınması
    current_time = str(time()).encode('utf-8')
    
    # Rastgele bir sayının üretilmesi
    random_number = str(randint(0, 1_000_000)).encode('utf-8')
    
    # Zaman ve rastgele sayının birleştirilmesi
    combined = current_time + random_number
    
    # MD5 hash fonksiyonu ile birleşik değerin hash'lenmesi
    unique_id = md5(combined).hexdigest()
    
    return unique_id

def get_month_data():
    """Form verileri için render durumunda input iskeleti"""
    months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    return [(month, index + 1) for index, month in enumerate(months)]

################################################################ DB-JS ########################################################################

def get_wage_params(request, year):
    """Form verileri için yıllara göre parametre bilgileri"""
    try:
        wage_params = WageParameters.objects.get(year=year)
        
        data = {
            "year": wage_params.year,
            "Birinci_Donem_Net_Asgari_Ucret": wage_params.Birinci_Donem_Net_Asgari_Ucret,
            "Birinci_Donem_Brut_Ucret_Taban": wage_params.Birinci_Donem_Brut_Ucret_Taban,
            "Birinci_Donem_Birinci_Vergi_Dilimi": wage_params.Birinci_Donem_Birinci_Vergi_Dilimi,
            "Birinci_Donem_Ikinci_Vergi_Dilimi": wage_params.Birinci_Donem_Ikinci_Vergi_Dilimi,
            "Birinci_Donem_Ucuncu_Vergi_Dilimi": wage_params.Birinci_Donem_Ucuncu_Vergi_Dilimi,
            "Birinci_Donem_Dorduncu_Vergi_Dilimi": wage_params.Birinci_Donem_Dorduncu_Vergi_Dilimi,
            "Birinci_Donem_Besinci_Vergi_Dilimi": wage_params.Birinci_Donem_Besinci_Vergi_Dilimi,
            "Birinci_Donem_Birinci_Derece_Engelli_Indirimi": wage_params.Birinci_Donem_Birinci_Derece_Engelli_Indirimi,
            "Birinci_Donem_Ikinci_Derece_Engelli_Indirimi": wage_params.Birinci_Donem_Ikinci_Derece_Engelli_Indirimi,
            "Birinci_Donem_Ucuncu_Derece_Engelli_Indirimi": wage_params.Birinci_Donem_Ucuncu_Derece_Engelli_Indirimi,
            "Birinci_Donem_Brut_Ucret_Tavan": wage_params.Birinci_Donem_Brut_Ucret_Tavan,

            "Ikinci_Donem_Net_Asgari_Ucret": wage_params.Ikinci_Donem_Net_Asgari_Ucret,
            "Ikinci_Donem_Brut_Ucret_Taban": wage_params.Ikinci_Donem_Brut_Ucret_Taban,
            "Ikinci_Donem_Birinci_Vergi_Dilimi": wage_params.Ikinci_Donem_Birinci_Vergi_Dilimi,
            "Ikinci_Donem_Ikinci_Vergi_Dilimi": wage_params.Ikinci_Donem_Ikinci_Vergi_Dilimi,
            "Ikinci_Donem_Ucuncu_Vergi_Dilimi": wage_params.Ikinci_Donem_Ucuncu_Vergi_Dilimi,
            "Ikinci_Donem_Dorduncu_Vergi_Dilimi": wage_params.Ikinci_Donem_Dorduncu_Vergi_Dilimi,
            "Ikinci_Donem_Besinci_Vergi_Dilimi": wage_params.Ikinci_Donem_Besinci_Vergi_Dilimi,
            "Ikinci_Donem_Birinci_Derece_Engelli_Indirimi": wage_params.Ikinci_Donem_Birinci_Derece_Engelli_Indirimi,
            "Ikinci_Donem_Ikinci_Derece_Engelli_Indirimi": wage_params.Ikinci_Donem_Ikinci_Derece_Engelli_Indirimi,
            "Ikinci_Donem_Ucuncu_Derece_Engelli_Indirimi": wage_params.Ikinci_Donem_Ucuncu_Derece_Engelli_Indirimi,
            "Ikinci_Donem_Brut_Ucret_Tavan": wage_params.Ikinci_Donem_Brut_Ucret_Tavan,
        }
        return JsonResponse(data)
    except WageParameters.DoesNotExist:
        return JsonResponse({"error": "Veri bulunamadı"}, status=404)

################################################################# DB ##########################################################################

def delete_table(session_id, time_stamp_id):
    """Ziyaretçiler tarafından veri tabanında bulundurulan benzersiz tablonun silinmesi"""
    # for bordro in Bordro.objects.filter(session_key=session_id, time_stamp_key=time_stamp_id):
    #     bordro.delete()
    
    Bordro.objects.filter(session_key=session_id, time_stamp_key=time_stamp_id).delete()

def save_bordro_data(session_id, time_stamp_id, ay, Donem_Brut_Toplam, Gunluk_Brut_Ucret, SGK_matrah, Isci_SGK, Isci_Issizlik, GVM, KGVM, gelir_vergisi, damga_vergisi, Net_Ucret, Maas, Isveren_SGK, Isveren_Issizlik, Normal_Maliyet, Hazine_yardimi, Hazine_Indirimi_Sonrasi_Maliyet, Vergi_Odenecek, Normal_SGK_Odenecek, Hazine_Indirimi_Sonrasi_SGK_Odenecek, agi, GV_Istisna, DV_Istisna, Asg_GVM, Kum_Asg_GV, _2Ay_Onceki_Devir, _1Ay_Onceki_Devir):
    """Ziyaretçiler tarafından hazırlanan benzersiz tablonun veri tabanına kaydedilmesi"""
    # Yeni kayıt oluştur
    Bordro.objects.create(
        session_key=session_id,
        time_stamp_key=time_stamp_id,
        ay=ay,
        Donem_Brut_Toplam=Donem_Brut_Toplam,
        Gunluk_Brut_Ucret=Gunluk_Brut_Ucret,
        SGK_matrah=SGK_matrah,
        Isci_SGK=Isci_SGK,
        Isci_Issizlik=Isci_Issizlik,
        GVM=GVM,
        KGVM=KGVM,
        gelir_vergisi=gelir_vergisi,
        damga_vergisi=damga_vergisi,
        Net_Ucret=Net_Ucret,
        Maas=Maas,
        Isveren_SGK=Isveren_SGK,
        Isveren_Issizlik=Isveren_Issizlik,
        Normal_Maliyet=Normal_Maliyet,
        Hazine_yardimi=Hazine_yardimi,
        Hazine_Indirimi_Sonrasi_Maliyet=Hazine_Indirimi_Sonrasi_Maliyet,
        Vergi_Odenecek=Vergi_Odenecek,
        Normal_SGK_Odenecek=Normal_SGK_Odenecek,
        Hazine_Indirimi_Sonrasi_SGK_Odenecek=Hazine_Indirimi_Sonrasi_SGK_Odenecek,
        agi=agi,
        GV_Istisna=GV_Istisna,
        DV_Istisna=DV_Istisna,
        Asg_GVM=Asg_GVM,
        Kum_Asg_GV=Kum_Asg_GV,
        IkiAyOncekiDevir=_2Ay_Onceki_Devir,
        BirAyOncekiDevir=_1Ay_Onceki_Devir
    )

    return "yeni kayıt oluşturuldu"

def get_kvm_cumulative(GVM, sql, session_id, time_stamp_id):
    """Kümülatif verilerin toplamı"""
    kvm_sum = Bordro.objects.filter(session_key=session_id, time_stamp_key=time_stamp_id).aggregate(Sum(sql))
    kvm_total = kvm_sum[f'{sql}__sum'] if kvm_sum[f'{sql}__sum'] else 0
    KGVM = kvm_total + GVM

    return KGVM