# backend/django/chat/models.py
from django.db import models


class KnowledgeBaseEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Entry"
        verbose_name_plural = "Knowledge Base"

    def __str__(self):
        return self.question[:60]


class ConversationMessage(models.Model):
    ROLE_CHOICES = (("user", "User"), ("assistant", "Assistant"))
    session_id = models.CharField(max_length=64, db_index=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["session_id", "created_at"]),
        ]

    def __str__(self):
        return f"{self.role}: {self.text[:40]}"
