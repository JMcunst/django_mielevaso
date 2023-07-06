from itertools import groupby

from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from rest_framework.response import Response

from guildwar.models import GuildwarHistory


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getDefenseDec(request):
    def sort_and_group_raw_data(raw_data):
        sorted_data = sorted(raw_data, key=lambda x: sorted(x['def']))
        print('LENGTH:',len(sorted_data))
        grouped_data = []
        for key, group in groupby(sorted_data, key=lambda x: x['def']):
            print('KEY:', key, 'GROUP:', group)
            atk_list = [{'atk': item['atk'], 'def_win': item['def_win'],'def_death': item['def_death']} for item in group]
            print('ATK_LIST:', atk_list)

            def_win_count = sum(item['def_win'] for item in atk_list)
            def_win_rate = round(def_win_count / len(atk_list) * 100, 2)

            def_strong_total = len(atk_list) * 3
            def_no_death = sum(1 for item in atk_list for value in item['def_death'] if not value)
            def_strong_point = round((def_no_death / def_strong_total) * 100, 2)

            grouped_data.append({'combined_def': key, 'atk_list': atk_list, 'def_win_rate': def_win_rate, 'def_strong_point': def_strong_point})
        return grouped_data

    res_data = dict()

    param = request.GET
    print(param)

    ## 연결된 Postgresql의 guildwar_history 테이블에서 데이터를 가져 옴.
    guildwar_histories = GuildwarHistory.objects.all()
    # guildwar_histories = GuildwarHistory.objects.order_by('-id')[:200]

    raw_data = []
    for history in guildwar_histories:
        his_data = dict()
        atk_heros, def_heros, def_death = [], [], []
        atk_heros.append(history.atk_hero1)
        atk_heros.append(history.atk_hero2)
        atk_heros.append(history.atk_hero3)
        def_heros.append(history.def_hero1)
        def_heros.append(history.def_hero2)
        def_heros.append(history.def_hero3)
        def_death.append(history.def_hero1_death)
        def_death.append(history.def_hero2_death)
        def_death.append(history.def_hero3_death)
        his_data['atk'] = atk_heros
        his_data['def'] = def_heros
        his_data['def_win'] = history.is_def_victory
        his_data['def_death'] = def_death

        raw_data.append(his_data)

    sorted_data = sort_and_group_raw_data(raw_data)

    res_data['data'] = sorted_data

    return Response(data=res_data, status=status.HTTP_200_OK)
