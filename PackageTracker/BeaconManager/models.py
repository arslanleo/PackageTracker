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

class Layout(models.Model):
    """Model representing a Layout (Floor Plan)"""
    name = models.CharField(max_length=100, null=False, blank=False, help_text="Layout's name (e.g First Floor)")
    length = models.CharField(max_length=10, default='640', null=False, blank=False, help_text="Layout's length")
    width = models.CharField(max_length=10, default='360', null=False, blank=False, help_text="Layout's width)")
    image = models.ImageField(upload_to='layouts/', null=False, blank=False, help_text="Image of the layout")

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Name the url to access the details of a particular tag instance"""
        return reverse('layout-detail',args=[str(self.id)])
    
    def __str__(self):
        """Name for representing this Tag object"""
        return f'{self.name}'

class Node(models.Model):
    """Model representing a Node (BLE Receiver Device)"""
    node_id = models.CharField(max_length=12, null=False, blank=False, help_text="Node's Unique MAC Address")
    host_address = models.URLField(default='mqtt.bconimg.com', null=False, blank=False, help_text="Node's host address")
    port = models.CharField(default='1883', max_length=4, null=False, blank=False, help_text="Node's port number")
    topic = models.CharField(max_length=50, null=False, blank=False, help_text="Node's publish topic (as entered during configuration)")
    user_name = models.CharField(max_length=50, null=True, blank=True, help_text="Node's username (optional)")
    password = models.CharField(max_length=50, null=True, blank=True, help_text="Node's password (optional)")
    location = models.CharField(default='0,0', max_length=7, null=True, blank=True, help_text="Node's location (format: x,y)")
    layout = models.ForeignKey(Layout, on_delete=models.SET_NULL, null=True, help_text="Layout's name on which this node is used")

    class Meta:
        ordering = ['layout']

    def get_absolute_url(self):
        """Name the url to access the details of a particular tag instance"""
        return reverse('node-detail',args=[str(self.node_id)])
    
    def __str__(self):
        """Name for representing this Tag object"""
        return f'{self.node_id} ({self.layout.name})'

