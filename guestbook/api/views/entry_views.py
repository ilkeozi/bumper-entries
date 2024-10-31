# guestbook/api/views/entry_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from guestbook.api.serializers import EntryDTOSerializer, CreateEntryDTOSerializer, UpdateEntryDTOSerializer
from guestbook.services.entry_service import get_entries, get_entry_by_id, create_entry, update_entry, delete_entry
from pydantic import ValidationError
from guestbook.api.schemas import error_response

class EntryPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class EntryViewSet(viewsets.ViewSet):
    pagination_class = EntryPagination

    @swagger_auto_schema(
        operation_description="Retrieve a list of all entries.",
        responses={200: EntryDTOSerializer(many=True)}
    )
    def list(self, request):
        entries = get_entries()
        paginator = self.pagination_class()
        paginated_entries = paginator.paginate_queryset(entries, request)
        serializer = EntryDTOSerializer(paginated_entries, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new entry",
        request_body=CreateEntryDTOSerializer,
        responses={
            201: EntryDTOSerializer,
            400: error_response
        }
    )
    def create(self, request):
        try:
            entry = create_entry(request.data)
            serializer = EntryDTOSerializer(entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_details = [{"field": err['loc'][0], "message": err['msg']} for err in e.errors()]
            return Response({"errors": error_details}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve an entry by ID",
        responses={200: EntryDTOSerializer, 404: "Entry not found"}
    )
    def retrieve(self, request, pk=None):
        entry = get_entry_by_id(pk)
        if entry is None:
            return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EntryDTOSerializer(entry)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an entry by ID",
        request_body=UpdateEntryDTOSerializer,
        responses={
            200: EntryDTOSerializer,
            404: openapi.Response(description="Entry not found"),
            400: error_response
        }
    )
    def update(self, request, pk=None):
        try:
            entry = update_entry(pk, request.data)
            if entry is None:
                return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = EntryDTOSerializer(entry)
            return Response(serializer.data)
        except ValidationError as e:
            error_details = [{"field": err['loc'][0], "message": err['msg']} for err in e.errors()]
            return Response({"errors": error_details}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an entry by ID",
        responses={204: "Entry deleted successfully", 404: "Entry not found"}
    )
    def destroy(self, request, pk=None):
        success = delete_entry(pk)
        if not success:
            return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
