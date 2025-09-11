from django.contrib import admin
from .models import KnowledgeBaseEntry, ConversationMessage
from django.contrib import admin  # already imported at top, but safe to repeat

admin.site.site_header = "AIME Admin"
admin.site.site_title = "AIME Admin"
admin.site.index_title = "Pengurusan AIME"

@admin.register(KnowledgeBaseEntry)
class KnowledgeBaseEntryAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("question", "answer", "tags")
    ordering = ("-updated_at",)

@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ("session_id","role","short_text","created_at")
    list_filter = ("role",)
    search_fields = ("session_id","text")
    ordering = ("-created_at",)

    def short_text(self, obj):
        return (obj.text[:60] + "...") if len(obj.text) > 60 else obj.text
