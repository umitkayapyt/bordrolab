import { formatNumber } from './utils.js';
import { getWageParamsWithCache } from './wageCache.js'; // Yeni modülü import ediyoruz

export async function updateSpanColor(salaryInputs, year) {
    const wageParams = await getWageParamsWithCache(year);  // Yıl bazında verileri önbellekten çekiyoruz

    if (!wageParams) {
        console.error("Veri bulunamadı");
        return;
    }

    const spans = document.querySelectorAll(".Gunluk_Brut_Ucrt");

    salaryInputs.forEach(input => {
        const period = input.getAttribute('data-period');
        const paramName = `${period}_Brut_Ucret_Taban`;
        const brutUcretTaban = wageParams[paramName];
        const threshold = brutUcretTaban / 30;
    
        // data-period ile span elementini seçme
        const spans = document.querySelectorAll(`.Gunluk_Brut_Ucrt[data-period="${period}"]`);
    
        spans.forEach(span => {
            const spanValue = parseFloat(span.textContent.replace(/\./g, '').replace(',', '.'));
            if (spanValue < threshold) {
                span.style.color = 'red';
            } else {
                span.style.color = '';
            }
        });
    });
}

export function updateInputs(year, ucretType, statu, wageParams, salaryInputs) {
    try {
        const showPlaceholders = (statu === "Normal" || statu === "Maden ve Yeraltı" || statu === "Emekli") || (statu === "Emekli" && (ucretType === "BRUT" || ucretType === "TOPLAM MALİYET"));
        if (showPlaceholders) {
            const params = wageParams;

            salaryInputs.forEach(input => {
                const month = parseInt(input.getAttribute('data-month'), 10);
                const period = getPeriod(month);
                let paramName;
                let value;

                if (ucretType === "NET") {
                    paramName = `${period}_Net_Asgari_Ucret`;
                } else if (ucretType === "BRUT") {
                    paramName = `${period}_Brut_Ucret_Taban`;
                } else if (ucretType === "TOPLAM MALİYET") {
                    paramName = `${period}_Brut_Ucret_Taban`;
                    value = params[paramName] * (statu === "Emekli" ? 1.245 : 1.225);
                }

                if (params[paramName] !== undefined) {
                    if (!value) {
                        value = params[paramName];
                    }
                    value = Number(value); // veri tabanından string gelen ifade
                    input.placeholder = formatNumber(value);
                } else {
                    input.placeholder = "";
                }
            });
        } else {
            salaryInputs.forEach(input => input.placeholder = "");
        }
    } catch (error) {
        console.error(error.message);
        salaryInputs.forEach(input => input.placeholder = "Hata: " + error.message);
    }
}

function getPeriod(month) {
    return month <= 6 ? 'Birinci_Donem' : 'Ikinci_Donem';
}
