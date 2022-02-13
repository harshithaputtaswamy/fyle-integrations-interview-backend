from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment
from rest_framework.response import Response
from rest_framework import generics, status

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Student Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def create(self, validated_data):
        return Assignment.objects.create(**validated_data)

    def validate(self, attrs):
        
        if 'content' in attrs and attrs['content']:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        
        if self.initial_data['assignment'].state == 'DRAFT':
            raise serializers.ValidationError('SUBMITTED assignments can only be graded')
        if self.initial_data['assignment'].state == 'GRADED':
            raise serializers.ValidationError('GRADED assignments cannot be graded again')
        if self.initial_data['assignment'].state == 'SUBMITTED':
            self.initial_data['assignment'].state = 'GRADED'
        if self.initial_data['assignment'].teacher.id != self.initial_data['teacher']:
            raise serializers.ValidationError('Teacher cannot grade for other teachers assignment')
        if 'grade' in attrs and attrs['grade'] not in ["A", "B", "C", "D"]:
            raise serializers.ValidationError('Invalid Grade')
                
        if 'student' in attrs:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')

        if self.partial:
            return attrs

        return super().validate(attrs)

