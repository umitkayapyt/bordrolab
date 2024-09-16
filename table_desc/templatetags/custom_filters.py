from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return 


@register.filter
def intcomma_dot(value):
    try:
        value = float(value)  # Sayıyı ondalık hale getiriyoruz
    except (TypeError, ValueError):
        return value  # Sayı değilse orijinal değeri döndürüyoruz

    # Sayıyı binlik ayırıcı ile formatla ve ondalık ayırıcıyı virgül yap
    formatted_value = '{:,.2f}'.format(value)  # 1500000.00 => 1,500,000.00

    # Binlik ayırıcıyı nokta yap, ondalık ayırıcıyı virgül yap
    formatted_value = formatted_value.replace(',', 'X').replace('.', ',').replace('X', '.')

    return formatted_value
