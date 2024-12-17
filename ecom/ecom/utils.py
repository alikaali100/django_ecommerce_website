from django.contrib.auth.models import User, Group


def assign_user_to_group(username, group_name):
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        if group not in user.groups.all():
            user.groups.add(group)
            user.save()
            return f"User '{username}' has been successfully added to group '{group_name}'."
        else:
            return f"User '{username}' is already in group '{group_name}'."
    except User.DoesNotExist:
        return f"User '{username}' does not exist."
    except Group.DoesNotExist:
        return f"Group '{group_name}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"
