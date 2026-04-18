from django.db import models
from users.models import Client
from wines.models import Wine
from coltns.models import ClientCollection

class WineComment(models.Model): # For clients comments any wine
    """Model to store comments for wines."""
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    wine = models.ForeignKey(
        Wine, on_delete=models.CASCADE
    )

    comment = models.TextField(max_length=250)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.client.username} on {self.wine.name}"

class ClientCollectionComment(models.Model): # For clients comments Other client collections
    """Model to store comments for collections."""
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    collection = models.ForeignKey(
        ClientCollection, on_delete=models.CASCADE,
    )

    comment = models.TextField(max_length=250)
    comment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.client.username} on {self.collection.collection_name}"