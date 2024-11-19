from django.shortcuts import get_object_or_404, render
from news.templatetags.thai_date import getdate
from news.models import New
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import NewSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

def home(req):
    news = New.objects.all()
    return render(req,'news/home.html',{'news':news})

class NewHtmlAPI(APIView):
    # GET method รับข้อมูลข่าวทั้งหมด
    @swagger_auto_schema(
        operation_summary="Get all news",
        responses={200: openapi.Response("HTML rendered successfully",schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "html": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="HTML content for the list news page",
                            example=f"\n\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n..."
                        )}
                    ))}
                    )
    def get(self, request, *args, **kwargs):
        news = New.objects.all()
        html = render_to_string('news/home.html', {'news': news})
        return Response({'html': html}, status=status.HTTP_200_OK)
    # POST method 
    @swagger_auto_schema(
        operation_summary="Create a new",
        request_body =openapi.Schema(
        # responses={200: openapi.Response("Create new successfully", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title","description","post_by","category"],
            properties={
                "title":openapi.Schema(type=openapi.TYPE_STRING,description="title of new"),
                "description":openapi.Schema(type=openapi.TYPE_STRING,description="description of new"),
                "post_by":openapi.Schema(type=openapi.TYPE_STRING,description="who are create a new"),
                "category":openapi.Schema(type=openapi.TYPE_STRING,description="category of new"),},
            ),
            responses={200: openapi.Response("Create new successfully", openapi.Schema(type=openapi.TYPE_OBJECT,
                    example={
                "title":"เปิดตัวเทคโนโลยี AI ใหม่ พลิกโฉมวงการสุขภาพ",
                "description":"วันนี้ บริษัทเทคโนโลยีชั้นนำของไทยได้ประกาศเปิดตัวระบบปัญญาประดิษฐ์ (AI) ใหม่ล่าสุด...",
                "post_by":"ผู่เขียนข่าว 1 ",
                "category":"2"}
                ))}
    )
    def post(self, request, *args, **kwargs):
        serializer = NewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReadNewAPI(APIView):
    # GET method รับข้อมูลข่าวที่เลือก
    @swagger_auto_schema(
        operation_summary="Get new data with id",
        responses={200: openapi.Response("HTML rendered successfully"
                 , openapi.Schema(type=openapi.TYPE_OBJECT,
                properties={
                        "html": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="HTML content for a news page",
                            example=f"\n\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n...")
                }),
             )})
    def get(self, request, *args, **kwargs):
        new = get_object_or_404(New, id=kwargs.get('id'))
        print(new)
        description_parts = new.description.split('\r\n\r\n') 
        parts = []
        if len(description_parts) > 1:
            for d in description_parts:
                parts.append(d)
        else:
            for d in description_parts:
                parts.append(d)
        html = render_to_string('news/new_page.html',{'new':new,'parts':parts})
        return Response({'html': html}, status=status.HTTP_200_OK)

    # PUT method (Update)
    @swagger_auto_schema(
        operation_summary="Update a new",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="Can Update only a few fields",
            properties={
                "title":openapi.Schema(type=openapi.TYPE_STRING,description="title of new"),
                "description":openapi.Schema(type=openapi.TYPE_STRING,description="description of new"),
                "post_by":openapi.Schema(type=openapi.TYPE_STRING,description="who are create a new"),
                "count_view":openapi.Schema(type=openapi.TYPE_NUMBER,description="view of this new"),
                "category":openapi.Schema(type=openapi.TYPE_STRING,description="category of new"),},
        ),
        responses={200: openapi.Response("Update new successfully", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            example={
                    "title":"เปิดตัวเทคโนโลยี AI ใหม่ พลิกโฉมวงการสุขภาพ",
                    "description":"วันนี้ บริษัทเทคโนโลยีชั้นนำของไทยได้ประกาศเปิดตัวระบบปัญญาประดิษฐ์ (AI) ใหม่ล่าสุด...",
                    "post_by":"ผู่เขียนข่าว 1 ",
                    "count_view":2,
                    "category":"2"}
            ))}
    )
    def put(self, request, *args, **kwargs):
        new = get_object_or_404(New, id=kwargs.get('id'))
        print(new)
        serializer = NewSerializer(new, data=request.data,partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method
    @swagger_auto_schema(
        operation_summary="Delete a new",
        responses={200: openapi.Response("Delete new successfully", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message":openapi.Schema(type=openapi.TYPE_STRING,description="Successfully deleted.",example="Successfully deleted")})
            )},
    )
    def delete(self, request, *args, **kwargs):
        new = get_object_or_404(New, id=kwargs.get('id'))
        new.delete()
        return Response({"message": "Successfully deleted."},status=status.HTTP_200_OK)

 # แสดงหน้า อ่านข้อมูลข่าว   
def new_page(req,id):
    print(id)
    new = get_object_or_404(New, id=id)
    # new.count_view += 1
    # new.save()
    description_parts = new.description.split('\r\n\r\n') 
    parts = []
    if len(description_parts) > 1:
        for d in description_parts:
            parts.append(d)
    else:
        for d in description_parts:
            parts.append(d)
    return render(req,'news/new_page.html',{'new':new,'parts':parts})

#ใช้ทดสอบรับค่า api เพื่อแสดงผลหน้า html
def test(req):
    return render(req,'news/test.html',{})