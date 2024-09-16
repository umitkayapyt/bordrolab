import { updateSpanColor, updateInputs } from './selectOptions.js';
import { autoCorrectAllSalaryInputs } from './salaryInputs.js';
import { restrictAndFormatInput, handleCheckboxChange } from './utils.js';
import { getWageParamsWithCache } from './wageCache.js'; // Yeni modülü import ediyoruz

// Olay dinleyicilerini başlatan ana fonksiyon
export function setupEventListeners() {
    const statuSelect = document.getElementById('dynamic-select-statu');
    const kanunSelect = document.getElementById('dynamic-select-kanun');
    const yilSelect = document.getElementById('dynamic-select-yil');
    const selectUcretElement = document.getElementById('dynamic-select-ucret');
    const salaryInputs = document.querySelectorAll("input[data-salary]");
    const flexSwitchCheckCheckedElement = document.getElementById("flexSwitchCheckChecked_linyit");

    if (statuSelect && kanunSelect && yilSelect) {
        // Yıl seçildiğinde veriyi veritabanından çek
        yilSelect.addEventListener('change', async () => {
            const year = yilSelect.value;
            const wageParams = await getWageParamsWithCache(year);

            if (wageParams) {
                handleDataChange(wageParams, salaryInputs, selectUcretElement, statuSelect, yilSelect);
                setupLinyitTasKomuruKontrolu(statuSelect, flexSwitchCheckCheckedElement);
                // Yıl değişiminde sadece maaş ve linyit kontrolleri yapılır,
                setupArgeInputGuncelleme(kanunSelect, statuSelect);
            } else {
                console.error(`Yıla ait veri bulunamadı: ${year}`);
            }
        });

        // Diğer seçimlerde onChange fonksiyonunu çalıştır
        statuSelect.addEventListener('change', () => {
            getWageParamsWithCache(yilSelect.value).then(wageParams => {
                if (wageParams) {
                    handleDataChange(wageParams, salaryInputs, selectUcretElement, statuSelect, yilSelect);
                    setupLinyitTasKomuruKontrolu(statuSelect, flexSwitchCheckCheckedElement);
                }
            });
        });

        kanunSelect.addEventListener('change', () => {
            getWageParamsWithCache(yilSelect.value).then(wageParams => {
                if (wageParams) {
                    setupArgeInputGuncelleme(kanunSelect, statuSelect);
                    handleDataChange(wageParams, salaryInputs, selectUcretElement, statuSelect, yilSelect);
                }
            });
        });

        selectUcretElement.addEventListener('change', () => {
            getWageParamsWithCache(yilSelect.value).then(wageParams => {
                if (wageParams) {
                    handleDataChange(wageParams, salaryInputs, selectUcretElement, statuSelect, yilSelect);
                }
            });
        });
    } else {
        console.error("One or more elements not found for event listeners.");
    }

    // Maaş girişleri için blur event'i ekleme
    salaryInputs.forEach(input => {
        input.addEventListener('blur', autoCorrectAllSalaryInputs);
    });
}

// Sayfa yüklendiğinde yapılacak işlemler
export function initializePage() {
    const statuSelect = document.getElementById('dynamic-select-statu');
    const kanunSelect = document.getElementById('dynamic-select-kanun');
    const yilSelect = document.getElementById('dynamic-select-yil');
    const selectUcretElement = document.getElementById('dynamic-select-ucret');
    const salaryInputs = document.querySelectorAll("input[data-salary]");
    const flexSwitchCheckCheckedElement = document.getElementById("flexSwitchCheckChecked_linyit");

    if (statuSelect && kanunSelect && yilSelect) {
        const year = yilSelect.value;
        getWageParamsWithCache(year).then(wageParams => {
            if (wageParams) {
                setupLinyitTasKomuruKontrolu(statuSelect, flexSwitchCheckCheckedElement);
                handleDataChange(wageParams, salaryInputs, selectUcretElement, statuSelect, yilSelect);
                setupArgeInputGuncelleme(kanunSelect, statuSelect);
            } else {
                console.error(`Yıla ait veri bulunamadı: ${year}`);
            }
        });
    }
}

// onChange işlemleri için yeni fonksiyon
function handleDataChange(wageParams, salaryInputs, selectUcretElement, statuSelect, yilSelect) {
    updateInputs(yilSelect.value, selectUcretElement.value, statuSelect.value, wageParams, salaryInputs);
    updateSpanColor(salaryInputs, yilSelect.value, wageParams);
    autoCorrectAllSalaryInputs();
}

// Linyit ve taş kömürü kontrol fonksiyonu
function setupLinyitTasKomuruKontrolu(statuSelect, flexSwitchCheckCheckedElement) {
    if (statuSelect && flexSwitchCheckCheckedElement) {
        const isMadenYeraltı = (statuSelect.value === "Maden ve Yeraltı");

        toggleInput(flexSwitchCheckCheckedElement, !isMadenYeraltı);

        for (let i = 1; i <= 12; i++) {
            const shiftInput = document.querySelector(`input[name="shift_${i}"]`);
            const ubgtInput = document.querySelector(`input[name="UBGT_${i}"]`);
            const YeraltiGun = document.querySelector(`input[name="arge_day_${i}"]`);
            const gun = document.querySelector(`input[name="day_${i}"]`);
            
            toggleInput(shiftInput, isMadenYeraltı);
            toggleInput(ubgtInput, isMadenYeraltı);
            
            if (YeraltiGun && gun) {
                if (isMadenYeraltı) {
                    YeraltiGun.removeAttribute("disabled");
                    let gunValue = parseInt(gun.value) || 0;
                    let defaultYeraltiValue = 30;
                    YeraltiGun.value = (gunValue < defaultYeraltiValue) ? gunValue : defaultYeraltiValue;
                } else {
                    toggleInput(YeraltiGun, true);
                }
            }
        }

        const spanElement = document.getElementById('yearalti_arge');
        if (spanElement) {
            spanElement.textContent = isMadenYeraltı ? "Yer Altı" : "ARGE";
        }
    }
}

function setupArgeInputGuncelleme(kanunSelect, statuSelect) {
    // Koşula göre Ar-Ge inputlarını aktif/pasif hale getirme
    const isArgeActive = (kanunSelect.value === "05746" || kanunSelect.value === "04691" || statuSelect.value === "Maden ve Yeraltı");

    for (let i = 1; i <= 12; i++) {
        const ArgeGun = document.querySelector(`input[name="arge_day_${i}"]`);
        const gun = document.querySelector(`input[name="day_${i}"]`);
        const defaultYeraltiElement = document.getElementById(`arge_day_${i}`); // Benzersiz ID'ye göre element alınması

        if (ArgeGun && gun && defaultYeraltiElement) {
            const defaultYeraltiValue = parseInt(defaultYeraltiElement.dataset.defaultYeralti) || 0;

            if (isArgeActive) {
                ArgeGun.removeAttribute("disabled");
                let gunValue = parseInt(gun.value) || 0;
                ArgeGun.value = (gunValue < defaultYeraltiValue) ? gunValue : defaultYeraltiValue;
            } else {
                toggleInput(ArgeGun, true);
            }

            // Default yeraltı değerini güncelle
            defaultYeraltiElement.dataset.defaultYeralti = gun.value;
        }
    }
}

// Inputları aktif/pasif hale getiren yardımcı fonksiyon
function toggleInput(input, isDisabled) {
    if (input) {
        if (isDisabled) {
            input.setAttribute("disabled", "disabled");
            input.value = ""; // İçeriği temizle
        } else {
            input.removeAttribute("disabled");
        }
    }
}

// Maaş ve bonus girişleri için dinleyicileri ekler
document.addEventListener('DOMContentLoaded', function() {
    setupSalaryAndBonusListeners();
});

function setupSalaryAndBonusListeners() {
    restrictAndFormatInput('.input_salary', true); // .input_salary sınıfı için kısıtlamalar
    restrictAndFormatInput('.bonus', false); // .bonus sınıfı için kısıtlamalar
    restrictAndFormatInput('input[name^="gecmis_KGVM_"]', true); // gecmis_KGVM_ inputları
}
