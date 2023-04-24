from functools import wraps
from rest_framework.response import Response

from service_backend.apps.subjects.models import Subject
from service_backend.apps.chapters.models import Chapter
from rest_framework.views import APIView

from service_backend.apps.utils.constants import SubjectErrorCode, YearErrorCode
from service_backend.apps.utils.views import response_json
from service_backend.apps.subjects.serializers import SubjectSerializer
from service_backend.apps.years.models import Year


# Create your views here.
def _find_subject():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                subject = Subject.objects.get(id=args[1].data['subject_id'])
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                    message="can't find subject!"
                ), status=404)
            return func(*args, **kwargs, subject=subject)

        return wrapper

    return decorated


class SubjectList(APIView):
    def post(self, request):
        try:
            year = Year.objects.get(id=request.data['year_id'])
        except Exception as e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_DOES_NOT_EXIST,
                message="can't find year!"
            ), status=404)
        subject_serializer = SubjectSerializer(year.subjects, many=True)
        data = {'subject_list': subject_serializer.data}
        return Response(response_json(
            success=True,
            data=data
        ))


class SubjectCreate(APIView):
    def post(self, request):
        name = request.data['name']
        content = request.data['content']
        try:
            year = Year.objects.get(id=request.data['year_id'])
        except Exception as e:
            return Response(response_json(
                success=False,
                code=YearErrorCode.YEAR_DOES_NOT_EXIST,
                message="can't find year!"
            ), status=404)

        subject = Subject(name=name, content=content, year=year)
        try:
            subject.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_SAVE_FAILED,
                message="can't save subject!"
            ), status=404)
        chapter = Chapter(name='未分类', content='该目录下存放未分类章节的问题。', subject=subject)
        try:
            chapter.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_SAVE_FAILED,
                message="can't save chapter!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="create subject success!"
        ))


class SubjectUpdate(APIView):
    @_find_subject()
    def post(self, request, subject):
        subject.name = request.data['name']
        subject.content = request.data['content']
        try:
            subject.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_SAVE_FAILED,
                message="can't update subject!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="update subject success!"
        ))


class SubjectDelete(APIView):
    @_find_subject()
    def delete(self, request, subject):
        try:
            subject.delete()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DELETE_FAILED,
                message="can't delete subject!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="delete subject success!"
        ))
