from django.db import models
from django.core.exceptions import ValidationError


class TreeModel(models.Model):
    """
    An abstract base class for tree-like models.
    """

    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_child"
    )

    class Meta:
        abstract = True

    def xclean(self):
        """
        Check objects descendant to prevent loops in the tree structure.
        """
        if self.parent in self.decendant():
            raise ValidationError('Loop is not allowed.')

    def children(self):
        """
        Return a list of objects that have the current object as their parent.
        """
        if self.id:
            return self.__class__.objects.filter(parent=self)
        else:
            return list()

    def decendant(self):
        """
        Return a list of objects that are descendants of the current object.
        """
        from functools import reduce
        children = self.children()
        return reduce(lambda x, y: x | y, list(c.decendant() for c in children), children)

    def ancestry(self):
        """
        Return a list of ancestors (parent and its parent, and so on) of the current object.
        """
        ancestor = [self.parent]
        while ancestor[-1]:
            ancestor.append(ancestor[-1].parent)
        ancestor.pop()
        return ancestor
