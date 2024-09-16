export function getWageParams(year) {
    return fetch(`/get-wage-params/${year}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return null;
            } else {
                return data;  // Veriyi başarıyla döndür
            }
        })
        .catch(error => {
            console.error('Veri çekme hatası:', error);
            return null;
        });
}