from django import template
register = template.Library()
@register.filter
def getComments(value):
    # write your code...
    return True # Later you can pass the comment data
