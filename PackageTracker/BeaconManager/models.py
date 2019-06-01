from django.db import models

# Create your models here.

class Tag(models.Model):
    """Model representing a Tag (BLE Beacon)"""
    tagID = models.CharField(max_length=12, help_text="Tag's Unique MAC Address")
    name = models.CharField(max_length=100, help_text="Tag's given name")
    description = models.TextField(max_length=256, null=True, blank=True, help_text="Description of objects associated with this Tag")
    
    TAG_STATUS = (
        ('p', 'Pending'),
        ('r', 'Received'),
        ('s', 'Sent'),
        )
    
    status = models.CharField(max_length=1, choices=TAG_STATUS, default='p', help_text="Tag's status")
    location = models.CharField(max_length=200, null=True, blank=True, help_text="Tag's location")

    class Meta:
        ordering = ['status']

    def get_absolute_url(self):
        """Name the url to access the details of a particular tag instance"""
        return reverse('tag-detail',args=[str(self.tagID)])
    
    def __str__(self):
        """Name for representing this Tag object"""
        return f'{self.tagID} ({self.name})'