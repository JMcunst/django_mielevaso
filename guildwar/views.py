from itertools import groupby, product

from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from rest_framework.response import Response

from guildwar.models import GuildwarHistory


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getDefenseDec(request):
    def calculate_picked_rate(combined_def, raw_data):
        total_data = len(raw_data)
        picked_data = sum(combined_def == item['combined_def'] for item in raw_data)
        picked_rate = (picked_data / total_data) * 100
        return picked_rate

    def process_raw_data(raw_data):
        sorted_data = sorted(raw_data, key=lambda x: sorted(x['def']))
        grouped_data = []

        for item in sorted_data:
            print('ITEM:', item)
            combined_def = item['def']
            atk_list = [{'atk': item['atk'], 'def_win': item['def_win']}]

            combined_atk_list = []
            combined_atk_win_count = sum(atk['def_win'] for atk in atk_list)
            combined_atk_win_rate = (combined_atk_win_count / len(atk_list)) * 100
            combined_atk_list.append({'atk': item['atk'], 'def_win': item['def_win']})

            def_win_rate = item['def_win_rate']
            picked_rate = calculate_picked_rate(combined_def, sorted_data)

            grouped_data.append({
                'combined_def': combined_def,
                'atk_list': combined_atk_list,
                'def_win_rate': def_win_rate,
                'picked_rate': picked_rate
            })

        return grouped_data
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
    def sort_and_group_by_atk(raw_data):
        grouped_data = []
        for item in raw_data:
            combined_def = item['combined_def']
            atk_list = item['atk_list']

            combined_atk_list = []
            for atk_combination in product(*[atk['atk'] for atk in atk_list]):
                combined_atk_win_count = sum(atk['def_win'] for atk in atk_list if atk['atk'] == list(atk_combination))
                combined_atk_win_rate = combined_atk_win_count / len(atk_list) * 100
                combined_atk_list.append(
                    {'combined_atk': list(atk_combination), 'combined_atk_win_rate': combined_atk_win_rate})

            def_win_rate = item['def_win_rate']
            grouped_data.append(
                {'combined_def': combined_def, 'atk_list': combined_atk_list, 'def_win_rate': def_win_rate})
        return grouped_data

    res_data = dict()

    param = request.GET
    print(param)

    ## 연결된 Postgresql의 guildwar_history 테이블에서 데이터를 가져 옴.
    # guildwar_histories = GuildwarHistory.objects.all()
    guildwar_histories = GuildwarHistory.objects.order_by('-id')[:50]

    data = []
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

    print('RAW DATA:', raw_data)
    sorted_data = sort_and_group_raw_data(raw_data)
    print('SUCCESS')
    print('RESULT:',sorted_data)
    # grouped_atk = sort_and_group_by_atk(sorted_data)
    # for dt in grouped_atk:
    #     print(dt)
    res_data['data'] = sorted_data

    return Response(data=res_data, status=status.HTTP_200_OK)
