from django import template
register = template.Library()

from main.models import Mobile,Category,Photo,Comments

@register.filter
def getComments(value):
    print(value)
    MCID = value[0:2]
    PDIDs = value[2:]
    # print(PDIDs,end="**")
    PDIDs = ", ".join(PDIDs)
    print(PDIDs,"pdisssssssssssssssssssssss")

    comments = []
    try:
        cmmt1 = Comments.objects.filter(mobile_id=MCID[0],category_id=MCID[1],compList__iexact = PDIDs).distinct()
        for i in cmmt1:
            comments.append(i.comment)
    except Exception as e:
        print(e)
    # print(comments)
    for i in comments:
        print(i)
    return comments
