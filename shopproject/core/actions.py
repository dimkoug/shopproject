def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


def make_draft(modeladmin, request, queryset):
    queryset.update(is_published=False)


make_published.short_description = "Mark selected items as published"
make_draft.short_description = "Mark selected items as draft"
