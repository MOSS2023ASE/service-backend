from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.years.models import Year
from service_backend.apps.utils.views import response_json
from service_backend.apps.years.serializers import YearSerializer
from service_backend.apps.utils.constants import YearErrorCode


# Create your views here.
class YearList(APIView):
    def post(self, request):
        year = Year.objects.all()
        year_serializer = YearSerializer(year, many=True)
        return Response(response_json(
            success=True,
            data=year_serializer.data
        ))


class YearCreate(APIView):
    def post(self, request):
        year = Year(content=request.data['content'])
        try:
            year.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_SAVE_FAILED,
                message="can't save year!"
            ))

        return Response(response_json(
            success=True,
            message="create year success!"
        ))


class YearUpdate(APIView):
    def post(self, request):
        try:
            print(request.data['year_id'])
            year = Year.objects.get(id=request.data['year_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_DOES_NOT_EXIST,
                message="can't find year!"
            ))
        year.content = request.data['content']
        try:
            year.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_SAVE_FAILED,
                message="can't save year!"
            ))
        return Response(response_json(
            success=True,
            message="update year success!"
        ))


class YearDelete(APIView):
    def post(self, request):
        try:
            year = Year.objects.get(id=request.data['year_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_DOES_NOT_EXIST,
                message="can't find year!"
            ))
        try:
            year.delete()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_DELETE_FAILED,
                message="can't delete year!"
            ))
        return Response(response_json(
            success=True,
            message="delete year success!"
        ))
