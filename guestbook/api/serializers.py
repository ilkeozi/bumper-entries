# guestbook/api/serializers.py
from rest_framework import serializers
from guestbook.models import Entry, User

class EntrySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name")

    class Meta:
        model = Entry
        fields = ['id', 'user_name', 'subject', 'message', 'created_date']

class EntryDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_name = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()
    created_date = serializers.DateTimeField()

class CreateEntryDTOSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()

    def validate_user_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("User name should contain only alphanumeric characters")
        return value

    def validate_subject(self, value):
        prohibited_words = ["spam", "ad"]
        if any(word in value.lower() for word in prohibited_words):
            raise serializers.ValidationError("Subject contains prohibited words")
        return value

class UpdateEntryDTOSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()

    def validate_subject(self, value):
        prohibited_words = ["spam", "ad"]
        if any(word in value.lower() for word in prohibited_words):
            raise serializers.ValidationError("Subject contains prohibited words")
        return value

class UserDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    total_messages = serializers.IntegerField()
    last_entry = serializers.CharField()

class CreateUserDTOSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def validate_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Name should contain only alphanumeric characters")
        return value
