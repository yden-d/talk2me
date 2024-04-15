from rest_framework import serializers
from .models import Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    """
    Serializer for the Channel model.

    Attributes:
        Meta: A class containing metadata for the serializer.
    """

    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Server model with additional fields and representation customization.

    Attributes:
        num_members (SerializerMethodField): A method field to retrieve the number of members in the server.
        channel_server (ChannelSerializer): A nested serializer for the channels associated with the server.

        Meta: A class containing metadata for the serializer.
    """

    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ("member",)

    def get_num_members(self, obj):
        """
        Retrieve the number of members in the server.

        Args:
            obj (Server): The Server instance.

        Returns:
            int or None: The number of members if available, otherwise None.
        """
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """
        Customize the representation of the server data.

        Args:
            instance (Server): The Server instance.

        Returns:
            dict: The customized representation of the server data.
        """
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        data.pop("num_members") if not num_members else data
        return data
