from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from rest_framework.response import Response

from guildwar.models import GuildwarHistory


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getDefenseDec(request):

    res_data = {}

    param = request.GET
    print(param)

    ## 연결된 Postgresql의 guildwar_history 테이블에서 데이터를 가져 옴.
    guildwar_histories = GuildwarHistory.objects.all()

    data = []
    for history in guildwar_histories:
        history_data = {
            'atk_user_name': history.atk_user_name,
            'atk_hero1': history.atk_hero1,
            'atk_hero2': history.atk_hero2,
            # 나머지 필드들도 필요한 대로 추가
        }
        data.append(history_data)

    res_data['data'] = data

    return Response(data=res_data, status=status.HTTP_200_OK)