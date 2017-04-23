from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import serializers

from LawBot.settings import DEFAULT_FROM_EMAIL
from core.models import Dictonary


class DictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictonary
        fields = ('title', 'description')


def get_dict(request):
    search_data = request.GET.get('search')
    if not search_data:
        return JsonResponse([], safe=False)

    qs = Dictonary.objects.filter(title=search_data.strip().upper())
    if len(qs) > 0:
        return JsonResponse(DictSerializer(qs, many=True).data, safe=False)

    qs = Dictonary.objects.filter(title__icontains=search_data)
    if len(qs) > 0:
        return JsonResponse(DictSerializer(qs, many=True).data, safe=False)

    search_data_list = search_data.split(' ')
    final_list = []
    for search_word in search_data_list:
        if len(search_word) < 4:
            continue
        else:
            final_list.append(search_word)
    if not final_list:
        final_list = search_data_list

    q = Q(title__icontains=final_list[0])
    for search_word in final_list[1:]:
        q = q | Q(title__icontains=search_word)
    qs = Dictonary.objects.filter(q)
    return JsonResponse(DictSerializer(qs, many=True).data, safe=False)


def send_email(request, email):
    try:
        send_mail(
            subject="LawBot from CourtHack 2017",
            message="Thanks for using LawBot!\nHave a nice day! ;)",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
        return JsonResponse({'status': 'ok'}, safe=False)
    except:
        return JsonResponse({'status': 'bad'}, safe=False)
