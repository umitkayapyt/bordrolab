// Sayı formatlama fonksiyonu
export function formatNumber(number) {
  return number.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Inputları kısıtlayan ve formatlayan işlev
export function restrictAndFormatInput(selector, addDecimals) {
  const inputs = document.querySelectorAll(selector);
  inputs.forEach(input => {
    input.addEventListener('blur', function() {
      if (this.value.trim() !== '') {
        formatInput(this, addDecimals);
      }

      // day_ ve arge_day_ inputlarının senkronizasyonu
      if (this.name.startsWith('day_')) {
        updateAllArgeDayInputsFromDay(this); // Tüm arge_day_ inputlarını güncelle
      }

      if (this.name.startsWith('arge_day_')) {
        updateAllDayInputsFromArgeDay(this); // Tüm day_ inputlarını güncelle
      }
    });

    input.addEventListener('input', function() {
      processInput(this, addDecimals);
      this.value = this.value.replace(/[^0-9,]/g, ''); // Geçersiz karakterleri temizle
    });
  });
}

// day_ inputuna yapılan değişikliklerde tüm arge_day_ inputlarını güncelleyen işlev
function updateAllArgeDayInputsFromDay(dayInput) {
  const dayValue = parseFloat(dayInput.value.replace(/\./g, '').replace(',', '.')) || 0;

  for (let i = 1; i <= 12; i++) {
    const argeDayInput = document.querySelector(`input[name="arge_day_${i}"]`);
    if (argeDayInput) {
      let argeDayValue = parseFloat(argeDayInput.value.replace(/\./g, '').replace(',', '.')) || 0;

      // Eğer arge_day_ inputunun değeri day_ inputunun değerinden büyükse, arge_day_ inputunu day_ inputuna eşitle
      if (argeDayValue > dayValue) {
        argeDayInput.value = dayValue.toString();
      }
    }
  }
}

// arge_day_ inputuna yapılan değişikliklerde tüm day_ inputlarını güncelleyen işlev
function updateAllDayInputsFromArgeDay(argeDayInput) {
  const argeDayValue = parseFloat(argeDayInput.value.replace(/\./g, '').replace(',', '.')) || 0;

  for (let i = 1; i <= 12; i++) {
    const dayInput = document.querySelector(`input[name="day_${i}"]`);
    if (dayInput) {
      let dayValue = parseFloat(dayInput.value.replace(/\./g, '').replace(',', '.')) || 0;

      // Eğer day_ inputunun değeri arge_day_ inputunun değerinden küçükse, day_ inputunu arge_day_ inputuna eşitle
      if (dayValue < argeDayValue) {
        dayInput.value = argeDayValue.toString();
      }
    }
  }
}

// Inputu formatlayan işlev
function formatInput(target, addDecimals) {
  const value = parseAndValidateInput(target, target.value, addDecimals);
  target.value = formatNumberDec(value, addDecimals);
}

// Inputu işleyen işlev
function processInput(target, addDecimals) {
  const value = parseAndValidateInput(target, target.value, addDecimals);
  
  if (!target.name.startsWith('gecmis_KGVM_')) {
    updateInputsOthers(target, value, addDecimals); // Diğer inputları güncelle
  }
}

// Inputu doğrulayan işlev
export function parseAndValidateInput(target, value, addDecimals) {
  const [integerPart, decimalPart = '00'] = value.split(',');
  const cleanedValue = (addDecimals ? `${integerPart.replace(/\./g, '')}.${decimalPart.padEnd(2, '0')}` : integerPart);
  let parsedValue = parseFloat(cleanedValue) || 0;

  // Eğer arge_day inputuysa ve day_ inputunu geçiyorsa, sınırla
  if (target.name.startsWith('arge_day_')) {
    const dayInputName = target.name.replace('arge_day_', 'day_');
    const dayInput = document.querySelector(`input[name="${dayInputName}"]`);
    if (dayInput) {
      const dayValue = parseFloat(dayInput.value.replace(/\./g, '').replace(',', '.')) || 0;
      if (parsedValue > dayValue) {
        parsedValue = dayValue; // arge_day değeri day_ değerini geçmesin
      }
    }
  }

  // day_ inputunun değeri 30'u geçemez
  if (isDayInput(target) && parsedValue > 30) {
    parsedValue = 30;
  }

  return parsedValue;
}

// Günlük input olup olmadığını kontrol eden işlev
function isDayInput(target) {
  return target.name.startsWith('day_') && target.classList.contains('bonus');
}

// Sayıyı formatlayan işlev (binlik ve ondalık ayracı ekleme)
function formatNumberDec(number, addDecimals) {
  const [integerPart, decimalPart] = parseFloat(number).toFixed(addDecimals ? 2 : 0).split('.');
  return integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (decimalPart ? `,${decimalPart}` : '');
}

// Diğer inputları güncelleyen işlev
function updateInputsOthers(target, value, addDecimals) {
  const cellIndex = target.parentElement.cellIndex;
  const rowIndex = target.parentElement.parentElement.rowIndex;
  const table = target.closest('table');
  const rows = table.rows;
  const checkbox = document.getElementById('flexSwitchCheckChecked_aylar');

  if (checkbox && checkbox.checked) {
    for (let i = 1; i <= 11; i++) {
      const nextRow = rows[rowIndex + i];
      if (nextRow) {
        const nextInput = nextRow.cells[cellIndex]?.querySelector(`.${target.className}`);
        if (nextInput) {
          nextInput.value = target.value === '' ? '' : formatNumberDec(value, addDecimals);
        }
      } else {
        break;
      }
    }
  }
}

// Checkbox değişimi kontrolü
export function handleCheckboxChange() {
  const currentInput = document.querySelector('.input_salary:focus');
  if (currentInput) {
    processInput(currentInput, true);
  }
}
