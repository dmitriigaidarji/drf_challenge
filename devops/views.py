import sys
from hashlib import md5
from typing import Dict, List, Any, Union
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from devops.serializers import DevOpsSerializer


class DevOpsEngineers(APIView):
    def get_devops_response(self, de: int, dm_data_center: str) -> Dict[str, str]:
        return {'DE': de, 'DM_data_center': dm_data_center}

    def calc(self,
             index: int,
             dm_capacity: int,
             de_capacity: int,
             data_centers: List[Dict[str, Union[str, int]]]) -> Dict[str, str]:
        """
        Calculation function to get the amount of required DEs
        as well as the optimal data center name

        """
        result = 0
        for i in range(0, len(data_centers)):
            value = data_centers[i]['servers']
            if i == index:
                value = value - dm_capacity
            if value > 0:
                if value % de_capacity == 0:
                    result = result + int(value / de_capacity)
                else:
                    result = result + int(value / de_capacity) + 1
        return self.get_devops_response(result, data_centers[index]['name'])

    def smart_search(self,
                     dm_capacity: int,
                     de_capacity: int,
                     data_centers: List[Dict[str, Union[str, int]]]) -> Dict[str, str]:
        """
        Iterate through input to find the best match in one loop

        """
        max_remain = - sys.maxsize
        max_index = None
        for i in range(0, len(data_centers)):
            value = data_centers[i]['servers']
            while value > dm_capacity:
                value = value - de_capacity
            if value > max_remain:
                max_remain = value
                max_index = i
        return self.calc(max_index, dm_capacity, de_capacity, data_centers)

    def main_calc(self,
                  dm_capacity: int,
                  de_capacity: int,
                  data_centers: List[Dict[str, Union[str, int]]]) -> Dict[str, str]:
        """
        Verify if the result is already cached
        If yes - return the value from cache
        If not - perform calculations

        """
        cache_key = md5(
            '{}{}{}'.format(
                dm_capacity,
                de_capacity,
                sorted(data_centers, key=lambda x: x['name'].lower())
            ).encode('utf-8')
        ).hexdigest()
        value = cache.get(cache_key, None)
        if value is None:
            value = self.smart_search(dm_capacity, de_capacity, data_centers)
            cache.set(cache_key, value, 86400)
            return value
        else:
            return value

    def post(self, request: Any) -> Response:
        """
        Validate input and perform calculation call
        :param request: in format {DM_capacity: int, DE_capacity: int, data_centers: [{name:str, servers:int},]}
        :return: Calculation result in format {DE:int, DM_data_center:str}
        """
        serializer = DevOpsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(self.main_calc(
                serializer.validated_data.get('DM_capacity'),
                serializer.validated_data.get('DE_capacity'),
                serializer.validated_data.get('data_centers')
            ))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
