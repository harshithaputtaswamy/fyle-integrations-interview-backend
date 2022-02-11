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
        print(self.initial_data['teacher'], self.initial_data['assignment'].teacher.id, self.initial_data['teacher'], '---------',)
        if 'grade' in attrs and attrs['grade']:
            if self.initial_data['assignment'].teacher.id == self.initial_data['teacher']:
                if 'content' in attrs and attrs['content']:
                    raise serializers.ValidationError('Teacher cannot change the content of the assignment')
                if attrs['grade'] not in ["A", "B", "C", "D"]:
                    raise serializers.ValidationError('Invalid Grade')
                if self.initial_data['assignment'].state == 'DRAFT':
                    raise serializers.ValidationError('SUBMITTED assignments can only be graded')
                if self.initial_data['assignment'].state == 'GRADED':
                    raise serializers.ValidationError('GRADED assignments cannot be graded again')
            elif self.initial_data['assignment'].teacher.id != self.initial_data['teacher']:
                raise serializers.ValidationError('Teacher cannot grade for other teachers assignment')
            
        if 'student' in attrs:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')

        if self.partial:
            return attrs

        return super().validate(attrs)


        # if self.initial_data['assignment'].content != None:
        #                 return Response(
        #                     data=self.initial_data['assignment'].__dict__,
        #                     status=status.HTTP_200_OK
        #                 )