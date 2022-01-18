from django import template

register = template.Library()

@register.simple_tag
def get_value(dict, key):
    return dict[key]

@register.filter(name='times') 
def times(number):
    return range(number)

@register.simple_tag
def shoe_decide_ball_color(number):
    base = "custom_scoring_balls_"
    if(number < 3):
        return base + "red"
    elif(number == 3):
        return base + "orange"
    else:
        return base + "green"