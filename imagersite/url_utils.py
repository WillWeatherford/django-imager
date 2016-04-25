"""A few small helpers to create urls."""

from django.contrib.auth.decorators import login_required, permission_required

ADD, EDIT, DELETE = 'add', 'change', 'delete'


def log_perm_required(model, perm, view):
    """Shortcut to wrap a view in both login_ and permission_required."""
    perm_name = model.format(perm)
    return login_required(
        permission_required(
            perm_name, raise_exception=True)(view))
