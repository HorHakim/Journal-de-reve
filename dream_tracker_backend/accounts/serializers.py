from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Utilisation de la méthode create_user pour gérer le hash du mot de passe
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user
