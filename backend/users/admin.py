from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class CustomUserAdmin(admin.ModelAdmin):
    # 1) 리스트 페이지에 보여줄 컬럼
    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )
    # 2) 사이드바 필터
    list_filter = ("is_active", "is_staff")
    # 3) 검색 박스에 적용할 필드
    search_fields = ("email", "username")
    # 4) 기본 정렬 순서
    ordering = ("-created_at",)

    # 5) 상세 페이지에서 읽기 전용으로 처리할 필드
    readonly_fields = ("created_at", "updated_at")

    # 6) 상세 페이지에서 보여줄 필드 그룹
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Personal Info",
            {
                "fields": ("username",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
