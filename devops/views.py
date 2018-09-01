from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from devops.serializers import DevOpsSerializer


class DevOpsEngineers(APIView):
    @staticmethod
    def calc(self, index, DM_capacity, DE_capacity, data_centers):
        result = 0
        for i in range(0, len(data_centers)):
            value = data_centers[i]['servers']
            if i == index:
                value = value - DM_capacity
            if value > 0:
                if value % DE_capacity == 0:
                    result = result + int(value / DE_capacity)
                else:
                    result = result + int(value / DE_capacity) + 1
        return {'DE': result, 'DM_data_center': data_centers[index]['name']}

    @staticmethod
    def full_search(self, DM_capacity, DE_capacity, data_centers):
        result = None
        for i in range(0, len(data_centers)):
            calc_result = self.calc(self, i, DM_capacity, DE_capacity, data_centers)
            if result is None or calc_result['DE'] < result['DE']:
                result = calc_result
        return result

    @staticmethod
    def smart_search(self, DM_capacity, DE_capacity, data_centers):
        remains = []
        for i in range(0, len(data_centers)):
            value = data_centers[i]['servers']
            while value > DM_capacity:
                value = value - DE_capacity
            remains.append(value)
        max_index = 0
        for i in range(0, len(remains)):
            if remains[i] > remains[max_index]:
                max_index = i
        return self.calc(self, max_index, DM_capacity, DE_capacity, data_centers)

    def post(self, request):
        serializer = DevOpsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(self.smart_search(self,
                                              serializer.validated_data.get('DM_capacity'),
                                              serializer.validated_data.get('DE_capacity'),
                                              serializer.validated_data.get('data_centers')))
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
