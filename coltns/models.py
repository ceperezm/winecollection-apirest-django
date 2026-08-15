from django.db import models
from users.models import User
from wines.models import Wine

# Create your models here.
# Define the models for the collections app


class ProviderCollection(models.Model):
    collection_name = models.CharField(max_length=100)
    description = models.TextField()
    registration_date = models.DateField(auto_now_add=True) # Date when the collection was created
    provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'provider__isnull': False}, null=True, blank=True) # Foreign key relationship to User model with provider role
    type = models.ForeignKey('Type', on_delete=models.CASCADE, null=True, blank=True) # Foreign key relationship to Type model
    
    def __str__(self):
        return self.collection_name # Return the collection name as the string representation of the ProviderCollection model
    
    
class ClientCollection(models.Model):
    collection_name = models.CharField(max_length=100)
    description = models.TextField()
    registration_date = models.DateField(auto_now_add=True) # Date when the collection was created
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'client__isnull': False}, null=True, blank=True) # Foreign key relationship to User model with client role
    
    def __str__(self):
        return self.collection_name # Return the collection name as the string representation of the ClientCollection model    
    
    
class Type(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.id} - {self.type_name}" # Return the type name as the string representation of the Type model
    

class ClientCollectionWine(models.Model):
    client_collection = models.ForeignKey(ClientCollection, on_delete=models.CASCADE) # Foreign key relationship to ClientCollection model
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE) # Foreign key relationship to Wine model
    added_date = models.DateField(auto_now_add=True) # Date when the wine was added to the client's collection
    
    
class ProviderCollectionWine(models.Model):
    provider_collection = models.ForeignKey(ProviderCollection, on_delete=models.CASCADE) # Foreign key relationship to ProviderCollection model
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE) # Foreign key relationship to Wine model
    added_date = models.DateField(auto_now_add=True) # Date when the wine was added to the provider's collection
    
    
    
                