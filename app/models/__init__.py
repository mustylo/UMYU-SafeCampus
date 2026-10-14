# Wannan file yana haɗa models ɗin project ɗinmu.
# Ta haka application zai iya gano User model.

from app.models.user import (AuditLog, CampusCase, CaseCategory, CaseComment,
                             CaseStatusHistory, Department, LostFoundItem,
                             Notification, SafetyAlert, User)

__all__ = ["User", "Department", "CaseCategory", "CampusCase", "CaseStatusHistory", "CaseComment", "Notification", "AuditLog", "LostFoundItem", "SafetyAlert"]
