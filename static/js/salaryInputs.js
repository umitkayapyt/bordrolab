import { formatNumber } from './utils.js';


export function autoCorrectSalaryInput(input) {
    if (input.value === "") {
        return;
    }

    const placeholderValue = parseFloat(input.placeholder.replace(/\./g, '').replace(',', '.'));
    const inputValue = parseFloat(input.value.replace(/\./g, '').replace(',', '.'));

    if (!isNaN(inputValue) && inputValue < placeholderValue) {
        input.value = formatNumber(placeholderValue);
    }
}

export function autoCorrectAllSalaryInputs() {
    const salaryInputs = document.querySelectorAll("input[data-salary]");
    salaryInputs.forEach(input => autoCorrectSalaryInput(input));
}

