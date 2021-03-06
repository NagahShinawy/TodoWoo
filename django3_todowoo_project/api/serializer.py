from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    # custom implementation for create & datecompleted) to be read only
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ["id", "title", "memo", "created", "datecompleted", "important"]


class TodoCompleteSerializer(serializers.ModelSerializer):
    todo_id = serializers.ReadOnlyField(source='todo.id')   # read only ( can not update id for _todo)

    class Meta:
        model = Todo
        fields = ["todo_id", "title", "memo", "important"]
        # read_only_fields = ["todo_id", "title", "memo", "important"]  # readOnlyFields

