from django.db.models import Avg


def calculate_title_rating(title):
    '''Вычисляет рейтинг произведения.'''
    if not hasattr(title, 'reviews'):
        return None

    reviews = title.reviews.all()
    if not reviews.exists():
        return None

    avg = reviews.aggregate(Avg('score'))['score__avg']
    return int(round(avg)) if avg else None