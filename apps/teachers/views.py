from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Teacher
from .serializers import TeacherAssignmentSerializer
from apps.students.models import Assignment

class AssignmetsView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer
    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)
        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id

        data = request.data
        data['teacher'] = teacher.id
        assignment = Assignment.objects.get(pk=request.data['id'])
        data['teacher_assigned'] = assignment.teacher

        try:
            assignment = Assignment.objects.get(pk=request.data['id'])
            data['assignment'] = assignment
        except Assignment.DoesNotExist:
            return Response(
                data={'error': 'Assignment does not exist/permission denied'},
                status=400,
            )
        
        serializer = self.serializer_class(assignment, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

