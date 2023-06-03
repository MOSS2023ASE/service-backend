from functools import wraps

from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.years.models import Year
from service_backend.apps.utils.views import response_json
from service_backend.apps.years.serializers import YearSerializer
from service_backend.apps.utils.constants import YearErrorCode


# Create your views here.
def _find_year():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                year = Year.objects.get(id=args[1].data['year_id'])
            except Exception:
                return Response(response_json(
                    success=False,
                    code=YearErrorCode.YEAR_DOES_NOT_EXIST,
                    message="can't find year!"
                ), status=404)
            return func(*args, **kwargs, year=year)

        return wrapper

    return decorated


class YearList(APIView):
    def get(self, request):
        year = Year.objects.all()
        year_serializer = YearSerializer(year, many=True)
        data = {
            "year_list": year_serializer.data,
            "current_year_id": 0,
            "current_content": ""
        }

        current_year = Year.objects.filter(is_current=True)
        if current_year:
            data["current_year_id"] = current_year.first().id
            data['current_content'] = current_year.first().content

        return Response(response_json(
            success=True,
            data=data
        ))


class YearCreate(APIView):
    def post(self, request):
        year = Year(content=request.data['content'])
        try:
            year.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_SAVE_FAILED,
                message="can't save year!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="create year success!"
        ))


class YearUpdate(APIView):
    @_find_year()
    def post(self, request, year=None):
        year.content = request.data['content']
        try:
            year.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_SAVE_FAILED,
                message="can't update year!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="update year success!"
        ))


class YearDelete(APIView):
    @_find_year()
    def delete(self, request, year):
        try:
            year.delete()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_DELETE_FAILED,
                message="can't delete year!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="delete year success!"
        ))


class YearCurrentUpdate(APIView):
    @_find_year()
    def post(self, request, year):
        try:
            current_year = Year.objects.filter(is_current=True)
            if current_year:
                current_year.first().is_current = False
                current_year.first().save()
            year.is_current = True
            year.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_SAVE_FAILED,
                message="can't set this year as current_year"
            ))
        return Response(response_json(
            success=True,
            message="change current year success!"
        ))
