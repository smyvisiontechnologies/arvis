from django import template
import re

register = template.Library()


@register.filter
def format_volume(value):
    """
    Convert '1000 ML' to '1 Litre', '250 ML' to '250 ML'
    """
    if not value:
        return value
    
    value_str = str(value).strip().upper()
    
    # Extract number and unit
    match = re.match(r'(\d+(?:\.\d+)?)\s*(ML|LITRE|L)', value_str, re.IGNORECASE)
    
    if not match:
        return value
    
    num = float(match.group(1))
    unit = match.group(2).upper()
    
    # If it's already in Litres, keep as is
    if unit in ['LITRE', 'L']:
        return value
    
    # Convert ML to Litre if >= 1000
    if unit == 'ML' and num >= 1000:
        litres = num / 1000
        if litres.is_integer():
            return f"{int(litres)} Litre"
        else:
            litres_str = f"{litres:.3f}".rstrip('0').rstrip('.')
            return f"{litres_str} Litre"
    
    return value


@register.filter
def format_total_volume(value):
    """
    Convert 'Total 10000 ML' to 'Total 10 Litre'
    """
    if not value:
        return value
    
    value_str = str(value)
    
    # Pattern for "Total XXXX ML" or just "XXXX ML"
    pattern = r'(\d+(?:\.\d+)?)\s*ML'
    
    def replacer(match):
        num = float(match.group(1))
        if num >= 1000:
            litres = num / 1000
            if litres.is_integer():
                return f"{int(litres)} Litre"
            else:
                litres_str = f"{litres:.3f}".rstrip('0').rstrip('.')
                return f"{litres_str} Litre"
        return f"{int(num)} ML"
    
    return re.sub(pattern, replacer, value_str, flags=re.IGNORECASE)