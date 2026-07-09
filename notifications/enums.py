# enums.py
from django.db import models

class NotificationType(models.TextChoices):
    # Social
    POST_LIKED = 'POST_LIKED', 'Post Liked'
    POST_COMMENTED = 'POST_COMMENTED', 'Post Commented'
    COMMENT_REPLIED = 'COMMENT_REPLIED', 'Comment Replied'
    NEW_FOLLOWER = 'NEW_FOLLOWER', 'New Follower'
    
    # Application
    APPLICATION_SUBMITTED = 'APPLICATION_SUBMITTED', 'Application Submitted'
    APPLICATION_APPROVED = 'APPLICATION_APPROVED', 'Application Approved'
    APPLICATION_REJECTED = 'APPLICATION_REJECTED', 'Application Rejected'
    
    # Payments
    PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', 'Payment Success'
    PAYMENT_FAILED = 'PAYMENT_FAILED', 'Payment Failed'
    
    # System
    SYSTEM = 'SYSTEM', 'System'
    WARNING = 'WARNING', 'Warning'
    SUCCESS = 'SUCCESS', 'Success'
    INFO = 'INFO', 'Info'
    ERROR = 'ERROR', 'Error'
    
