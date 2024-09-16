// wageCache.js
import { getWageParams } from './wageParameters.js';

let wageParamsCache = {}; // Veriyi önbellekte tutmak için

export async function getWageParamsWithCache(year) {
    if (wageParamsCache[year]) {
        return wageParamsCache[year];
    } else {
        const wageParams = await getWageParams(year);
        wageParamsCache[year] = wageParams;
        return wageParams;
    }
}

export function clearCache() {
    wageParamsCache = {}; // Önbelleği temizleme fonksiyonu
}
