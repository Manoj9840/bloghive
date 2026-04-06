from rest_framework import permissions

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object or admins to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow any safe methods (GET, HEAD, OPTIONS) if we want bit-global read
        # But this class is specifically for object-level write protection
        
        # Check if the user is a staff member (Admin)
        if request.user and request.user.is_staff:
            return True
            
        # Check if the user is the author of the blog
        # Assumes the object has an 'author' attribute
        return obj.author == request.user
