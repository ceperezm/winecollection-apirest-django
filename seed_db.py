import os
import django
from datetime import date

# Set up the Django environment to use the ORM in a standalone script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wine_collection_api.settings')
django.setup()

from locations.models import Country, City
from users.models import Provider, Client
from wines.models import Wine, Attribute
from coltns.models import Type, ProviderCollection, ClientCollection, ProviderCollectionWine, ClientCollectionWine
from comments.models import WineComment, ClientCollectionComment

def run_seed():
    print("Starting test data insertion...")

    # 1. Create Locations
    country_ar, _ = Country.objects.get_or_create(name="Argentina")
    country_cl, _ = Country.objects.get_or_create(name="Chile")
    
    city_mza, _ = City.objects.get_or_create(name="Mendoza", country_id=country_ar)
    city_scl, _ = City.objects.get_or_create(name="Santiago", country_id=country_cl)

    # 2. Create Users (Provider and Client)
    provider_username = "proveedor1"
    if not Provider.objects.filter(username=provider_username).exists():
        provider = Provider.objects.create_user(
            username=provider_username,
            password="password123", # Easy password for testing
            email="proveedor@example.com",
            first_name="Juan",
            last_name="Perez",
            name="Viñedos Perez",
            identifier_number=123456789,
            description="Productor de vinos de alta calidad",
            phone_number="+549111234567",
            city=city_mza
        )
    else:
        provider = Provider.objects.get(username=provider_username)

    client_username = "cliente1"
    if not Client.objects.filter(username=client_username).exists():
        client = Client.objects.create_user(
            username=client_username,
            password="password123", # Easy password for testing
            email="cliente@example.com",
            first_name="Maria",
            last_name="Gomez",
            birth_date=date(1990, 5, 15),
            city=city_scl
        )
    else:
        client = Client.objects.get(username=client_username)
        
    client_username_2 = "cliente2"
    if not Client.objects.filter(username=client_username_2).exists():
        client2 = Client.objects.create_user(
            username=client_username_2,
            password="password123",
            email="cliente2@example.com",
            first_name="Carlos",
            last_name="Lopez",
            birth_date=date(1985, 10, 20),
            city=city_mza
        )
    else:
        client2 = Client.objects.get(username=client_username_2)

    # 3. Create Collection Types
    type_premium, _ = Type.objects.get_or_create(type_name="Premium", description="Vinos de alta gama")
    type_reserva, _ = Type.objects.get_or_create(type_name="Reserva", description="Vinos reserva")

    # 4. Create Attributes and Wines
    if not Wine.objects.filter(name="Malbec Gran Reserva").exists():
        attr1 = Attribute.objects.create(
            total_sulfur_dioxide=50,
            fixed_acidity=7.5,
            volatile_acidity=0.3,
            free_sulfur_dioxide=15,
            citric_acid=0.4,
            residual_sugar=2.5,
            chlorides=0.04,
            density=0.9950,
            pH=3.5,
            sulphates=0.6,
            alcohol=14.0
        )
        wine1 = Wine.objects.create(
            provider=provider,
            name="Malbec Gran Reserva",
            description="Un malbec excelente de Mendoza con notas a ciruela.",
            harvest_year=2018,
            maker="Viñedos Perez",
            variety="Malbec",
            attribute=attr1,
            city=city_mza
        )
    else:
        wine1 = Wine.objects.get(name="Malbec Gran Reserva")

    if not Wine.objects.filter(name="Cabernet Sauvignon Classic").exists():
        attr2 = Attribute.objects.create(
            total_sulfur_dioxide=40,
            fixed_acidity=6.8,
            volatile_acidity=0.4,
            free_sulfur_dioxide=20,
            citric_acid=0.3,
            residual_sugar=3.0,
            chlorides=0.05,
            density=0.9960,
            pH=3.6,
            sulphates=0.5,
            alcohol=13.5
        )
        wine2 = Wine.objects.create(
            provider=provider,
            name="Cabernet Sauvignon Classic",
            description="Clásico Cabernet con cuerpo y taninos firmes.",
            harvest_year=2020,
            maker="Viñedos Perez",
            variety="Cabernet Sauvignon",
            attribute=attr2,
            city=city_scl
        )
    else:
        wine2 = Wine.objects.get(name="Cabernet Sauvignon Classic")

    # 5. Create Collections
    prov_coll, _ = ProviderCollection.objects.get_or_create(
        collection_name="Catálogo 2024 - Perez",
        description="Nuestros mejores vinos para este año.",
        provider=provider,
        type=type_premium
    )

    client_coll, _ = ClientCollection.objects.get_or_create(
        collection_name="Mis Favoritos",
        description="Los vinos que más me han gustado.",
        client=client
    )

    # 6. Add Wines to Collections
    ProviderCollectionWine.objects.get_or_create(provider_collection=prov_coll, wine=wine1)
    ProviderCollectionWine.objects.get_or_create(provider_collection=prov_coll, wine=wine2)
    
    ClientCollectionWine.objects.get_or_create(client_collection=client_coll, wine=wine1)

    # 7. Create Comments
    if not WineComment.objects.filter(client=client, wine=wine1).exists():
        WineComment.objects.create(
            client=client,
            wine=wine1,
            comment="Increíble malbec, muy recomendado."
        )

    if not ClientCollectionComment.objects.filter(client=client2, collection=client_coll).exists():
        ClientCollectionComment.objects.create(
            client=client2,
            collection=client_coll,
            comment="¡Excelente selección de vinos tienes aquí!"
        )

    print("Database seeded successfully!")

if __name__ == '__main__':
    run_seed()
