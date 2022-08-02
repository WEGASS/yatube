from django import template

register = template.Library()

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def uglify(string):
    count = 0
    ugly_str = str()
    for verb in string:
        if count % 2 != 0:
            ugly_str += verb.upper()
        else:
            ugly_str += verb.lower()
        count += 1
    return ugly_str