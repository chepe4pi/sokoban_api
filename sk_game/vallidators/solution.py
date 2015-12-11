from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from sk_map.serializers.map import MapDetailSerializer
from sk_map.models import Map
from collections import OrderedDict
import numpy as np


class GameSolutionValidator(object):
    def __init__(self, map, solution):
        self.map = MapDetailSerializer(Map.objects.get(id=map)).data
        self.solution = solution
        if not self.map['wall_set'] or not self.map['box_set'] or not self.map['men'] or not self.map['point_set']:
            raise ValidationError(_('Invalid map'))

    def create_matrix(self, data):
        if isinstance(data, list):
            dicts = [dict(ord_dict) for ord_dict in data]
            result = [np.array([item['x'], item['y']]) for item in dicts]
        elif isinstance(data, OrderedDict) or isinstance(data, dict):
            result = np.array([data['x'], data['y']])
        else:
            raise ValidationError(_('Invalid data'))
        return result

    def __call__(self):
        walls = self.create_matrix(self.map['wall_set'])
        boxes = self.create_matrix(self.map['box_set'])
        men = self.create_matrix(self.map['men'])
        points = self.create_matrix(self.map['point_set'])
        steps = self.create_matrix(self.solution)
        step_cases = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]
        if not np.array_equal(steps[0], men) or np.array_equal(boxes, points):
            return
        for step_index, step in enumerate(steps):
            if any((step == wall).all() for wall in walls):
                return
            if step_index != 0:
                diff = step - steps[step_index - 1]
                if not any((diff == step_case).all() for step_case in step_cases):
                    return
                for box_index, box in enumerate(boxes):
                    if np.array_equal(step, box):
                        box = boxes.pop(box_index) + diff
                        boxes.append(box)
                    if any((box == wall).all() for wall in walls):
                        return
        covered = 0
        for point_index, point in enumerate(points):
            for box_index, box in enumerate(boxes):
                if np.array_equal(point, box):
                    covered += 1
        if covered == len(points):
            return True
        else:
            return

    def is_valid(self):
        return self.__call__()