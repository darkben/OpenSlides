from ..utils.access_permissions import BaseAccessPermissions
from ..utils.auth import has_perm
from ..utils.collection import Collection


class AssignmentAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for Assignment and AssignmentViewSet.
    """
    def check_permissions(self, user):
        """
        Returns True if the user has read access model instances.
        """
        return has_perm(user, 'assignments.can_see')

    def get_serializer_class(self, user=None):
        """
        Returns different serializer classes according to users permissions.
        """
        from .serializers import AssignmentFullSerializer, AssignmentShortSerializer

        if user is None or (has_perm(user, 'assignments.can_see') and has_perm(user, 'assignments.can_manage')):
            serializer_class = AssignmentFullSerializer
        else:
            serializer_class = AssignmentShortSerializer
        return serializer_class

    def get_restricted_data(self, container, user):
        """
        Returns the restricted serialized data for the instance prepared
        for the user. Removes unpublished polls for non admins so that they
        only get a result like the AssignmentShortSerializer would give them.
        """
        # Expand full_data to a list if it is not one.
        full_data = container.get_full_data() if isinstance(container, Collection) else [container.get_full_data()]

        # Parse data.
        if has_perm(user, 'assignments.can_see') and has_perm(user, 'assignments.can_manage'):
            data = full_data
        elif has_perm(user, 'assignments.can_see'):
            # Exclude unpublished polls.
            data = []
            for full in full_data:
                full_copy = full.copy()
                full_copy['polls'] = [poll for poll in full['polls'] if poll['published']]
                data.append(full_copy)
        else:
            data = []

        # Reduce result to a single item or None if it was not a collection at
        # the beginning of the method.
        if isinstance(container, Collection):
            restricted_data = data
        elif data:
            restricted_data = data[0]
        else:
            restricted_data = None

        return restricted_data

    def get_projector_data(self, container):
        """
        Returns the restricted serialized data for the instance prepared
        for the projector. Removes unpublished polls.
        """
        # Expand full_data to a list if it is not one.
        full_data = container.get_full_data() if isinstance(container, Collection) else [container.get_full_data()]

        # Parse data. Exclude unpublished polls.
        data = []
        for full in full_data:
            full_copy = full.copy()
            full_copy['polls'] = [poll for poll in full['polls'] if poll['published']]
            data.append(full_copy)

        # Reduce result to a single item or None if it was not a collection at
        # the beginning of the method.
        if isinstance(container, Collection):
            projector_data = data
        elif data:
            projector_data = data[0]
        else:
            projector_data = None

        return projector_data
