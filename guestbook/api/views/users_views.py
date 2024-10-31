from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from guestbook.api.serializers import UserDTOSerializer, CreateUserDTOSerializer
from guestbook.services.user_service import get_users, get_user_by_id, create_user, delete_user
from guestbook.api.schemas import error_response  
from pydantic import ValidationError

class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Retrieve a list of users with their message count and latest entry details.",
        responses={200: UserDTOSerializer(many=True)}
    )
    def list(self, request):
        users = get_users()
        serializer = UserDTOSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=CreateUserDTOSerializer,
        responses={
            201: UserDTOSerializer,
            400: error_response
        }
    )
    def create(self, request):
        try:
            user = create_user(request.data)
            serializer = UserDTOSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_details = [{"field": err['loc'][0], "message": err['msg']} for err in e.errors()]
            return Response({"errors": error_details}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve a user by ID",
        responses={
            200: UserDTOSerializer,
            404: openapi.Response(description="User not found")
        }
    )
    def retrieve(self, request, pk=None):
        user = get_user_by_id(pk)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDTOSerializer(user)
        return Response(serializer.data)

    

    @swagger_auto_schema(
        operation_description="Delete a user by ID",
        responses={
            204: openapi.Response(description="User deleted successfully"),
            404: openapi.Response(description="User not found")
        }
    )
    def destroy(self, request, pk=None):
        success = delete_user(pk)
        if not success:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
