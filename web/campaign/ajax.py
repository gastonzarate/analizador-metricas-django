from django.http import JsonResponse

from campaign.models import Campaign


def delete_campaign(request):
    camp_id = request.GET.get('camp_id','')
    campaign = Campaign.objects.get(id=camp_id,user=request.user)
    response={}
    response["success"] = campaign.delete()
    return JsonResponse(response)

