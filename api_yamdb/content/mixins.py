from django.utils.text import slugify


class SlugAutoFillMixin:
    """Миксин для автоматического заполнения slug."""

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Используем self.__class__ чтобы работало для любых моделей
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
