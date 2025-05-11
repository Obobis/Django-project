from django import template

register = template.Library()

from ..models import Post

from django.db.models import Count

@register.simple_tag
def get_most_replied_posts(count=5):
    return Post.objects.filter(status="published")\
        .annotate(total_replies=Count('replies'))\
        .order_by('-total_replies')[:count]