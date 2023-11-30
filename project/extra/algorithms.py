import re, uuid
from collections import deque

from django.contrib.auth import get_user_model

User = get_user_model()

def quicksort_users(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2].username
    left = [user for user in arr if user.username < pivot]
    middle = [user for user in arr if user.username == pivot]
    right = [user for user in arr if user.username > pivot]

    return quicksort_users(left) + middle + quicksort_users(right)

def binary_search_first(sorted_users, pattern):
    left, right = 0, len(sorted_users) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        mid_username = sorted_users[mid].username

        if re.match("^{0}".format(pattern), mid_username):
            result = mid
            right = mid - 1
        elif mid_username < pattern:
            left = mid + 1
        else:
            right = mid - 1

    return result

def binary_search_last(sorted_users, pattern):
    left, right = 0, len(sorted_users) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        mid_username = sorted_users[mid].username

        if re.match("^{0}".format(pattern), mid_username):
            result = mid
            left = mid + 1
        elif mid_username < pattern:
            left = mid + 1
        else:
            right = mid - 1

    return result

def bfs_traversal(user_id, degrees):
    visited = set()
    queue = deque([(user_id, 0)])

    while queue:
        current, degree = queue.popleft()
        if degree > degrees:
            break

        if isinstance(current, str):
            current = uuid.UUID(current)

        if current not in visited:
            visited.add(current)
            yield current, degree

            user_profile = User.objects.get(id=current)
            friends_list = user_profile.friends

            for friend_id in friends_list:
                queue.append((friend_id, degree + 1))

def find_intersection(user1_id, user2_id, degrees):
    user1_friends = set(bfs_traversal(user1_id, degrees))
    user2_friends = set(bfs_traversal(user2_id, degrees))
    
    #intersection = user1_friends.intersection(user2_friends)
    intersection = {}
    intersection["targets"] = []
    intersection["distance"] = -1
    for user_path in user1_friends:
        for friend_path in user2_friends:
            if user_path[0] == friend_path[0]:
                if intersection["distance"] == -1 or intersection["distance"] > (user_path[1] + friend_path[1]):
                    intersection["targets"].clear()
                    intersection["distance"] = (user_path[1] + friend_path[1])
                    intersection["targets"].append(user_path[0])
                elif intersection["distance"] == (user_path[1] + friend_path[1]):
                    intersection["targets"].append(user_path[0])
    return intersection
