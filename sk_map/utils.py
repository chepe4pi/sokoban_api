from sk_game.models import UserMapMembership
from sk_map.models import Map


# def is_map_done(map_obj, user):
#     return UserMapMembership.objects.filter(owner=user, map=map_obj, done=True).count()


def is_map_owner(map_id, user):
    return Map.objects.filter(id=map_id, owner=user).count()
