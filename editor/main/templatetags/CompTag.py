from django import template
register = template.Library()

from main.models import Mobile,Category,Photo,Comments

@register.filter
def getComments(value):
    print(value)
    MCID = value[0:2]
    PDIDs = value[2:]
    PDIDs = ", ".join(PDIDs)
    print(PDIDs)

    try:
        cmmt1 = Comments.objects.filter(mobile_id=MCID[0],category_id=MCID[1],compList__icontains = PDIDs).distinct()
        for i in cmmt1:
            return (i.comment)
    except Exception as e:
        print(e)

    return "No Comments" 
