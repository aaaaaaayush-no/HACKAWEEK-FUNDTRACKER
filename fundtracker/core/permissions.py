from rest_framework import permissions


class IsGovernment(permissions.BasePermission):
    """
    Custom permission to only allow government users.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'GOVERNMENT'
        )


class IsContractor(permissions.BasePermission):
    """
    Custom permission to only allow contractor users.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'CONTRACTOR'
        )


class IsAuditor(permissions.BasePermission):
    """
    Custom permission to only allow auditor users.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'AUDITOR'
        )
