from django.db.models import Q
from django.http import JsonResponse
from rest_framework import serializers

from core.models import Dictonary


class DictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictonary
        fields = ('title', 'description')


def get_dict(request):
    search_data = request.GET.get('search')
    if not search_data:
        return JsonResponse([], safe=False)
    search_data_list = search_data.split(' ')
    final_list = []
    for search_word in search_data_list:
        if len(search_word) < 4:
            continue
        else:
            final_list.append(search_word)

    q = Q(title__icontains=final_list[0])
    for search_word in final_list[1:]:
        if len(search_word) < 4:
            continue
        q = q | Q(title__icontains=search_word)
    qs = Dictonary.objects.filter(q)
    return JsonResponse(DictSerializer(qs, many=True).data, safe=False)
