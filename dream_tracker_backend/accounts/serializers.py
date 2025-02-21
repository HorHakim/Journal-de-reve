from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return value

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("L'email n'est pas valide.")
        return value



    def create(self, validated_data):
        # Utilisation de la méthode create_user pour gérer le hash du mot de passe
        user = User.objects.create_user(**validated_data)
        return user
