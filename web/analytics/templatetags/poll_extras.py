from django import template

register = template.Library()


@register.simple_tag(name='indice')
def indice(dic,name, item):
    try:
        return dic[name][item]
    except:
        return None

@register.simple_tag(name='indice_sim')
def indice_sim(dic, item):
    try:
        return dic[item]
    except:
        return None


@register.simple_tag(name='rgb')
def rgb(num):
    if num<0 or num>11:
        num=11
    return {
        1: "255,102,102",
        2: "255,178,102",
        3: "255,255,102",
        5: "255,102,178",
        4:"102,102,255",
        6:"102,255,102",
        7: "192,192,192",
        8:"178,255,102",
        9:"102,255,178",
        10:"102,178,255",
        11:"178,102,255",
    }[num]


@register.simple_tag(name='rgb_border')
def rgb_border(num):
    if num<0 or num>11:
        num=11
    return {
        1:"255,51,51",
        2: "255,153,51",
        3:"255,255,51",
        5:"255,51,153",
        4:"51,51,255",
        6:"51,255,51",
        7: "160,160,160",
        8:"153,255,51",
        9:"51,255,153",
        10:"51,153,255",
        11:"153,51,255",
    }[num]