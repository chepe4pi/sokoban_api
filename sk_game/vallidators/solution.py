from rest_framework.exceptions import ValidationError
from sk_map.serializers.map import MapDetailSerializer
from sk_map.models import Map
from collections import OrderedDict
import numpy as np


class GameSolutionValidator(object):
    """
    This class used for validate solution of game level
    """
    def __init__(self, map, solution):
        """
        :param map: is a Map instance
        :param solution: is a json - format: [{x: 1, y: 2}, {x: 3, y: 4}, etc]
        :return: init of class
        """
        self.map = MapDetailSerializer(Map.objects.get(id=map)).data
        self.solution = solution
        if not self.map['wall_set'] or not self.map['box_set'] or not self.map['men'] or not self.map['point_set']:
            raise ValidationError('Invalid map')

    def create_matrix(self, data):
        """
        :param data: dict, OrderedDict or list of dicts or OrderedDicts
        :return: np.array - matrix
        """
        if isinstance(data, list):
            dicts = [dict(ord_dict) for ord_dict in data]
            result = [np.array([item['x'], item['y']]) for item in dicts]
        elif isinstance(data, OrderedDict) or isinstance(data, dict):
            result = np.array([data['x'], data['y']])
        else:
            raise ValidationError('Invalid data')
        return result

    def __call__(self):

        # create matrix from serialized data
        walls = self.create_matrix(self.map['wall_set'])
        boxes = self.create_matrix(self.map['box_set'])
        men = self.create_matrix(self.map['men'])
        points = self.create_matrix(self.map['point_set'])
        steps = self.create_matrix(self.solution)

        # step_cases - player can move only one step, up, down, left, right
        step_cases = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]

        # solution is not valid if player start to move not from Men's position on Map
        if not np.array_equal(steps[0], men):
            return

        # wrong map - Boxes not equal with Points
        if np.array_equal(boxes, points):
            return

        # start to validate steps of solution
        for step_index, step in enumerate(steps):

            # wrong if step on wall
            if any((step == wall).all() for wall in walls):
                return

            if step_index != 0:
                diff = step - steps[step_index - 1]

                # wrong if jump more then one step
                if not any((diff == step_case).all() for step_case in step_cases):
                    return

                # if we step on box - we move the box
                for box_index, box in enumerate(boxes):
                    if np.array_equal(step, box):
                        box = boxes.pop(box_index) + diff
                        boxes.append(box)

        # stert to calculate covered points
        covered = 0
        for point_index, point in enumerate(points):
            for box_index, box in enumerate(boxes):
                if np.array_equal(point, box):
                    covered += 1

        # if we covered all the points by boxes - map is done
        if covered == len(points):
            return True
        else:
            return

    def is_valid(self):
        return self.__call__()