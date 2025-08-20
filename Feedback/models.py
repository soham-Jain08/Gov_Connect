from django.db import models
import random, string

class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('department', 'Department Representative'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # We will store raw password for now; ideally hash
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Feedback(models.Model):
    subject = models.CharField(max_length=200)
    description = models.TextField()
    department_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    media = models.FileField(upload_to='feedback_media/', blank=True, null=True)
    feedback_id = models.CharField(max_length=10, unique=True, editable=False)
    abusive = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")

    def save(self, *args, **kwargs):
        if not self.feedback_id:
            dept_codes = {
                "Ministry of Education": "ED",
                "Ministry of Power": "PO",
                "Ministry of Railways": "RA",
                "Ministry of Roads and Highways": "RH",
                "Ministry of Women and Child Development": "WC",
                "Ministry of Water Resources": "WR",
            }

            dept_initials = dept_codes.get(self.department_name, "XX")

            # Keep generating until unique
            while True:
                new_id = f"{random.randint(10,99)}{dept_initials}{''.join(random.choices(string.digits, k=4))}"
                if not Feedback.objects.filter(feedback_id=new_id).exists():
                    self.feedback_id = new_id
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.feedback_id} - {self.subject}"