from django.http import JsonResponse

from campaign.models import Campaign


def get_campaign(request):
    user_id = request.GET.get("user_id","")
    options = '<option value="" selected="selected">-----------</option>'
    if request.user.is_staff:
        campaigns = Campaign.objects.filter(user=user_id)

        for camp in campaigns:
            options += '<option value="%s">%s</option>' % (camp.pk,camp)

    response = {}
    response['campaign'] = options

    return JsonResponse(response)