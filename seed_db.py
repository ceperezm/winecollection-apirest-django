"""
seed_db.py
Unified seed script for the wine collection API.

Usage:
    python seed_db.py            # runs basic seed by default
    python seed_db.py --basic    # inserts a small fixed dataset (2 providers, 1 client, 5 wines)
    python seed_db.py --massive  # inserts a large dataset (20 providers, 10 clients, 100 wines)
"""

import os
import sys
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wine_collection_api.settings')
django.setup()

from locations.models import Country, City
from users.models import Provider, Client
from wines.models import Wine, Attribute
from coltns.models import Type, ProviderCollection, ClientCollection, ProviderCollectionWine, ClientCollectionWine
from comments.models import WineComment, ClientCollectionComment


# ──────────────────────────────────────────────
# Shared reference data
# ──────────────────────────────────────────────

COUNTRIES_CITIES = {
    "Argentina":  ["Mendoza", "San Juan", "Salta", "Córdoba"],
    "Chile":      ["Santiago", "Colchagua", "Casablanca", "Maipo"],
    "España":     ["La Rioja", "Ribera del Duero", "Jerez", "Priorat"],
    "Francia":    ["Burdeos", "Borgoña", "Champagne", "Alsacia"],
    "Italia":     ["Toscana", "Piamonte", "Véneto", "Sicilia"],
}

VARIETIES = [
    "Malbec", "Cabernet Sauvignon", "Syrah", "Pinot Noir", "Merlot",
    "Tempranillo", "Garnacha", "Sangiovese", "Nebbiolo", "Barbera",
    "Sauvignon Blanc", "Chardonnay", "Riesling", "Viognier", "Albariño",
    "Torrontés", "Carménère", "Petit Verdot", "Zinfandel", "Monastrell",
]

WINE_ADJECTIVES = [
    "Nocturno", "Imperial", "Reserva", "Gran Reserva", "Clásico",
    "Salvaje", "Elegante", "Robusto", "Suave", "Intenso",
    "Artesanal", "Premium", "Exclusivo", "Auténtico", "Orgánico",
    "Brillante", "Oscuro", "Profundo", "Fresco", "Aromático",
]

WINE_DESCRIPTIONS = [
    "Intenso, con notas a mora y chocolate negro. Final largo y elegante.",
    "Fresco y cítrico, ideal para maridajes ligeros. Muy aromático.",
    "Estructurado con taninos firmes. Envejecimiento en barrica de roble francés.",
    "Elegante y equilibrado, con aromas a frutos rojos y especias.",
    "Suave y aterciopelado. Excelente relación calidad-precio.",
    "Potente y complejo, con reminiscencias minerales y florales.",
    "Ligero y afrutado. Perfecto para el aperitivo o días de verano.",
    "Profundo y oscuro. Desarrollado durante 18 meses en barrica.",
    "Terroso y especiado, con notas de pimienta negra y vainilla.",
    "Brillante y refrescante. Acidez equilibrada con final persistente.",
    "Gran cuerpo y estructura. Ideal para carnes rojas y caza.",
    "Notas florales delicadas, textura sedosa y retrogusto prolongado.",
    "Crianza artesanal en botella. Carácter único de terroir de altura.",
    "Maduro y goloso, con dátiles, higos y un toque de tabaco.",
    "Vivo y dinámico. Acidez vibrante que realza el bouquet frutal.",
]

COLLECTION_NAMES_PROVIDER = [
    "Selección Otoño", "Línea Orgánica", "Reserva de la Bodega", "Novedades 2024",
    "Edición Limitada", "Colección Terroir", "Serie Clásica", "Gran Añada",
    "Tinto Premium", "Blanco y Rosado",
]

COLLECTION_NAMES_CLIENT = [
    "Para el fin de semana", "Mis favoritos tintos", "Blancos de verano",
    "Descubrimientos 2024", "Especiales para regalar", "Maridajes perfectos",
    "Espumosos y rosados", "Guarda personal", "Vinos de terruño", "Top 10 del año",
]

COLLECTION_DESCRIPTIONS = [
    "Selección cuidadosa de los mejores vinos de la temporada.",
    "Nuestra apuesta por lo natural y sostenible en cada botella.",
    "Los clásicos que no pueden faltar en ninguna bodega.",
    "Las últimas incorporaciones a nuestra familia de vinos.",
    "Una edición única que no se repetirá. Corra a conseguirlos.",
    "Vinos que reflejan la esencia del suelo donde nacen.",
    "Añadas emblemáticas que han marcado décadas de historia.",
    "Blancos y rosados perfectos para climas cálidos.",
    "Tintos con carácter y personalidad propia.",
    "Una variedad que satisface tanto al experto como al aficionado.",
]

COMMENTS_TEXT = [
    "Espectacular! Lo probaré de nuevo sin duda.",
    "Muy buen balance entre acidez y taninos.",
    "Sorprendentemente suave para su graduación alcohólica.",
    "Ideal para acompañar una buena carne asada.",
    "La nariz es compleja, aunque el paladar podría ser más largo.",
    "Relación calidad-precio insuperable.",
    "Me recuerda a los vinos de la casa de mi abuela, nostálgico.",
    "Algo joven todavía, pero con potencial enorme en botella.",
    "Maridé con un queso manchego y fue maravilloso.",
    "El color rubí intenso ya dice mucho antes de probarlo.",
    "Final muy persistente, notas de cacao y café.",
    "Acidez perfecta, sin resultar demasiado agresiva.",
    "Ligero pero con carácter. Ideal para el aperitivo.",
    "La barrica se integra muy bien, sin dominar el conjunto.",
    "Podría ser un poco más complejo en boca, pero en general muy agradable.",
    "Increíble con pasta al ragú. Un 10 en maridaje.",
    "Los taninos son suaves y envolventes. Muy bien trabajado.",
    "Le falta un poco de profundidad, pero es fresco y fácil de beber.",
    "Fantástico con quesos curados. Repetiré seguro.",
    "Uno de los mejores vinos que he probado este año.",
]

TYPE_NAMES = [
    ("Tinto", "Vinos tintos de cuerpo medio y pleno."),
    ("Blanco", "Vinos blancos frescos y aromáticos."),
    ("Rosado", "Vinos rosados ligeros y afrutados."),
    ("Espumoso", "Vinos con gas, ideales para celebraciones."),
    ("Natural", "Vinos sin sulfitos añadidos, elaborados de forma artesanal."),
    ("Generoso", "Vinos de alta graduación con carácter propio."),
]

PROVIDER_NAMES = [
    ("Bodegas del Sol", "solares_bd"), ("Viñedos del Norte", "vinorte_bd"),
    ("Casa Vinicola Andina", "andina_wines"), ("Bodegas Cóndor", "condor_winery"),
    ("Terruño Patagónico", "terruno_pat"), ("Viñas del Mar", "vinas_mar_bd"),
    ("Bodega La Cumbre", "cumbre_wines"), ("Exportadora Sur", "vitivin_sur"),
    ("Gran Viñedo Colonial", "colonial_vino"), ("Cooperativa del Vino", "coop_vino"),
    ("Destilería Los Andes", "losandes_dist"), ("Casa Real de Vinos", "casareal_bd"),
    ("Vinos Artesanos García", "garcia_art"), ("Bodegas Horizonte", "horizonte_bd"),
    ("Monte Oscuro Winery", "monteoscuro"), ("La Vid Dorada", "viddorada_bd"),
    ("Sunset Cellar", "sunsetcellar"), ("Valle Sagrado Wines", "vallesagrado"),
    ("Rancho Viejo Vinos", "ranchoviejo"), ("Finca El Roble", "fincaelroble"),
]

CLIENT_NAMES = [
    ("María", "Gómez", "mgomez_cl"), ("Pedro", "Ramírez", "pramirez_cl"),
    ("Laura", "Torres", "ltorres_cl"), ("Carlos", "Mendez", "cmendez_cl"),
    ("Sofía", "Herrera", "sherrera_cl"), ("Diego", "Vargas", "dvargas_cl"),
    ("Ana", "Castro", "acastro_cl"), ("Javier", "Ortiz", "jortiz_cl"),
    ("Camila", "Reyes", "creyes_cl"), ("Roberto", "Ríos", "rrios_cl"),
]


# ──────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────

def make_attribute():
    """Create a Wine Attribute instance with randomized physicochemical values."""
    return Attribute.objects.create(
        total_sulfur_dioxide=random.randint(30, 200),
        fixed_acidity=round(random.uniform(5.0, 12.0), 2),
        volatile_acidity=round(random.uniform(0.1, 1.5), 2),
        free_sulfur_dioxide=random.randint(1, 70),
        citric_acid=round(random.uniform(0.0, 0.8), 3),
        residual_sugar=round(random.uniform(0.5, 14.0), 2),
        chlorides=round(random.uniform(0.02, 0.20), 4),
        density=round(random.uniform(0.9900, 1.0050), 5),
        pH=round(random.uniform(2.8, 4.0), 2),
        sulphates=round(random.uniform(0.3, 1.8), 2),
        alcohol=round(random.uniform(9.0, 16.0), 2),
    )


def create_types():
    """Create or retrieve all collection Type records."""
    types = []
    for tname, tdesc in TYPE_NAMES:
        t, _ = Type.objects.get_or_create(type_name=tname, defaults={"description": tdesc})
        types.append(t)
    return types


def print_summary():
    """Print a final count of all seeded records."""
    from wines.models import Wine as W
    from users.models import Provider as P, Client as C
    from coltns.models import ProviderCollection as PC, ClientCollection as CC
    from comments.models import WineComment as WC, ClientCollectionComment as CCC

    print("========================================")
    print("  RESUMEN FINAL")
    print("========================================")
    print(f"  Proveedores totales : {P.objects.count()}")
    print(f"  Clientes totales    : {C.objects.count()}")
    print(f"  Vinos totales       : {W.objects.count()}")
    print(f"  Col. proveedor      : {PC.objects.count()}")
    print(f"  Col. cliente        : {CC.objects.count()}")
    print(f"  Comentarios vino    : {WC.objects.count()}")
    print(f"  Comentarios col.    : {CCC.objects.count()}")
    print("\n  ¡Datos insertados exitosamente!")


# ──────────────────────────────────────────────
# Basic seed (small fixed dataset)
# ──────────────────────────────────────────────

def run_basic():
    """
    Insert a small, fixed dataset intended for quick local development:
    2 providers, 1 client, 5 wines, 2 provider collections, 1 client collection, 1 comment.
    """
    print("\n========================================")
    print("  SEED BÁSICO")
    print("========================================\n")

    # Create locations
    country_ar, _ = Country.objects.get_or_create(name="Argentina")
    country_cl, _ = Country.objects.get_or_create(name="Chile")
    country_es, _ = Country.objects.get_or_create(name="España")

    city_mza, _ = City.objects.get_or_create(name="Mendoza", country_id=country_ar)
    city_scl, _ = City.objects.get_or_create(name="Santiago", country_id=country_cl)
    City.objects.get_or_create(name="La Rioja", country_id=country_es)

    # Create providers
    provider1, _ = Provider.objects.get_or_create(
        username="bodegas_sol",
        defaults={
            "password": "password123",
            "email": "contacto@bodegassol.com",
            "first_name": "Carlos",
            "last_name": "Soler",
            "name": "Bodegas El Sol",
            "identifier_number": 100000001,
            "description": "Viñedos bañados por el sol de Mendoza, especialistas en tintos intensos.",
            "phone_number": "+549110000001",
            "city": city_mza,
        }
    )
    provider1.set_password("password123")
    provider1.save()

    provider2, _ = Provider.objects.get_or_create(
        username="vinedos_valle",
        defaults={
            "password": "password123",
            "email": "hola@vinedosvalle.cl",
            "first_name": "Andrea",
            "last_name": "Valle",
            "name": "Viñedos del Valle",
            "identifier_number": 100000002,
            "description": "Vinos orgánicos y naturales desde el corazón de Chile.",
            "phone_number": "+56980000002",
            "city": city_scl,
        }
    )
    provider2.set_password("password123")
    provider2.save()

    # Create client
    client1, _ = Client.objects.get_or_create(
        username="cliente1",
        defaults={
            "password": "password123",
            "email": "cliente1@example.com",
            "first_name": "María",
            "last_name": "Gómez",
            "birth_date": date(1990, 5, 15),
            "city": city_mza,
        }
    )
    client1.set_password("password123")
    client1.save()

    # Create collection types
    type_tinto, _ = Type.objects.get_or_create(type_name="Tinto", defaults={"description": "Vinos tintos clásicos"})
    type_natural, _ = Type.objects.get_or_create(type_name="Natural", defaults={"description": "Sin sulfitos añadidos"})
    Type.objects.get_or_create(type_name="Blanco", defaults={"description": "Vinos blancos frescos"})

    # Create wines
    wines_data = [
        (provider1, "Malbec Nocturno",      "Intenso, con notas a mora y chocolate negro.", 2021, "Malbec",            city_mza),
        (provider1, "Cabernet del Sol",      "Estructurado, taninos firmes y final largo.",  2020, "Cabernet Sauvignon", city_mza),
        (provider2, "Sauvignon Blanc Brisa", "Fresco, cítrico, ideal para tardes de verano.", 2023, "Sauvignon Blanc", city_scl),
        (provider2, "Pinot Noir Orgánico",   "Cereza brillante, terroso y elegante.",         2022, "Pinot Noir",       city_scl),
        (provider1, "Syrah Salvaje",         "Especiado, con toques de pimienta negra.",      2019, "Syrah",            city_mza),
    ]

    created_wines = []
    for p, name, desc, year, variety, city in wines_data:
        wine, _ = Wine.objects.get_or_create(
            name=name,
            defaults={
                "provider": p,
                "description": desc,
                "harvest_year": year,
                "maker": p.name,
                "variety": variety,
                "attribute": make_attribute(),
                "city": city,
            }
        )
        created_wines.append(wine)

    # Create collections
    prov_coll, _ = ProviderCollection.objects.get_or_create(
        collection_name="Novedades 2024",
        defaults={"description": "Las últimas añadas de Bodegas El Sol.", "provider": provider1, "type": type_tinto}
    )
    prov_coll2, _ = ProviderCollection.objects.get_or_create(
        collection_name="Línea Orgánica",
        defaults={"description": "Nuestros mejores vinos naturales.", "provider": provider2, "type": type_natural}
    )
    client_coll, _ = ClientCollection.objects.get_or_create(
        collection_name="Para el fin de semana",
        defaults={"description": "Selección personal de tintos y blancos.", "client": client1}
    )

    # Clear and reassign wines to collections
    ProviderCollectionWine.objects.all().delete()
    ClientCollectionWine.objects.all().delete()

    if len(created_wines) >= 5:
        ProviderCollectionWine.objects.create(provider_collection=prov_coll, wine=created_wines[0])
        ProviderCollectionWine.objects.create(provider_collection=prov_coll, wine=created_wines[1])
        ProviderCollectionWine.objects.create(provider_collection=prov_coll2, wine=created_wines[2])
        ProviderCollectionWine.objects.create(provider_collection=prov_coll2, wine=created_wines[3])
        ClientCollectionWine.objects.create(client_collection=client_coll, wine=created_wines[0])
        ClientCollectionWine.objects.create(client_collection=client_coll, wine=created_wines[2])

    # Create a sample wine comment
    if created_wines and not WineComment.objects.filter(client=client1, wine=created_wines[0]).exists():
        WineComment.objects.create(
            client=client1,
            wine=created_wines[0],
            comment="¡Espectacular! Lo probaré de nuevo.",
        )

    print_summary()


# ──────────────────────────────────────────────
# Massive seed helpers
# ──────────────────────────────────────────────

def create_cities():
    """Create all countries and cities from COUNTRIES_CITIES and return a flat list of City instances."""
    cities = {}
    for country_name, city_names in COUNTRIES_CITIES.items():
        country, _ = Country.objects.get_or_create(name=country_name)
        for city_name in city_names:
            city, _ = City.objects.get_or_create(name=city_name, country_id=country)
            cities[city_name] = city
    return list(cities.values())


def create_providers(cities):
    """Create or retrieve all providers from PROVIDER_NAMES."""
    providers = []
    for i, (name, username) in enumerate(PROVIDER_NAMES):
        prov, created = Provider.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@bodega.com",
                "first_name": name.split()[0] if " " in name else name,
                "last_name": "Wines",
                "name": name,
                "identifier_number": 200000000 + i,
                "description": "Productora especializada en vinos de alta calidad.",
                "phone_number": f"+5491140{str(i).zfill(6)}",
                "city": random.choice(cities),
            }
        )
        if created:
            prov.set_password("password123")
            prov.save()
        providers.append(prov)
        print(f"  Proveedor: {prov.name}")
    return providers


def create_clients(cities):
    """Create or retrieve all clients from CLIENT_NAMES."""
    clients = []
    for i, (first, last, username) in enumerate(CLIENT_NAMES):
        birth = date(random.randint(1975, 2000), random.randint(1, 12), random.randint(1, 28))
        cli, created = Client.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@email.com",
                "first_name": first,
                "last_name": last,
                "birth_date": birth,
                "city": random.choice(cities),
            }
        )
        if created:
            cli.set_password("password123")
            cli.save()
        clients.append(cli)
        print(f"  Cliente: {cli.first_name} {cli.last_name}")
    return clients


def create_wines(providers, cities, count=100):
    """
    Generate `count` unique wines assigned to random providers and cities.
    Uses a combination of variety + adjective to build wine names.
    """
    wines = []
    used_names = set(Wine.objects.values_list('name', flat=True))
    created = 0
    counter = 0
    while created < count:
        counter += 1
        variety = random.choice(VARIETIES)
        adj = random.choice(WINE_ADJECTIVES)
        name = f"{variety} {adj}"
        if name in used_names:
            name = f"{name} {counter}"   # ensure uniqueness with a numeric suffix
        if name in used_names:
            continue
        used_names.add(name)

        provider = random.choice(providers)
        city = random.choice(cities)
        wine = Wine.objects.create(
            provider=provider,
            name=name,
            description=random.choice(WINE_DESCRIPTIONS),
            harvest_year=random.randint(2012, 2024),
            maker=provider.name,
            variety=variety,
            attribute=make_attribute(),
            city=city,
        )
        wines.append(wine)
        created += 1
        if created % 10 == 0:
            print(f"  {created} vinos creados...")
    print(f"  Total vinos creados: {created}")
    return wines


def create_provider_collections(providers, types, wines, count=10):
    """Create provider collections and populate them with a random sample of wines."""
    collections = []
    for i in range(count):
        name = COLLECTION_NAMES_PROVIDER[i % len(COLLECTION_NAMES_PROVIDER)]
        full_name = f"{name} - {providers[i % len(providers)].name}"
        coll, _ = ProviderCollection.objects.get_or_create(
            collection_name=full_name,
            defaults={
                "description": COLLECTION_DESCRIPTIONS[i % len(COLLECTION_DESCRIPTIONS)],
                "provider": providers[i % len(providers)],
                "type": random.choice(types),
            }
        )
        collections.append(coll)
        sample_wines = random.sample(wines, min(random.randint(5, 10), len(wines)))
        for w in sample_wines:
            ProviderCollectionWine.objects.get_or_create(provider_collection=coll, wine=w)
        print(f"  Colección proveedor: {coll.collection_name} ({len(sample_wines)} vinos)")
    return collections


def create_client_collections(clients, wines, count=10):
    """Create client collections and populate them with a random sample of wines."""
    collections = []
    for i in range(count):
        name = COLLECTION_NAMES_CLIENT[i % len(COLLECTION_NAMES_CLIENT)]
        full_name = f"{name} ({clients[i % len(clients)].first_name})"
        coll, _ = ClientCollection.objects.get_or_create(
            collection_name=full_name,
            defaults={
                "description": COLLECTION_DESCRIPTIONS[i % len(COLLECTION_DESCRIPTIONS)],
                "client": clients[i % len(clients)],
            }
        )
        collections.append(coll)
        sample_wines = random.sample(wines, min(random.randint(3, 8), len(wines)))
        for w in sample_wines:
            ClientCollectionWine.objects.get_or_create(client_collection=coll, wine=w)
        print(f"  Colección cliente: {coll.collection_name} ({len(sample_wines)} vinos)")
    return collections


def create_comments(clients, wines, client_collections, total=30):
    """
    Create `total` comments split evenly between wine comments
    and client collection comments.
    """
    target_wine = total // 2
    target_colln = total - target_wine

    for _ in range(target_wine):
        WineComment.objects.create(
            client=random.choice(clients),
            wine=random.choice(wines),
            comment=random.choice(COMMENTS_TEXT),
        )

    for _ in range(target_colln):
        ClientCollectionComment.objects.create(
            client=random.choice(clients),
            collection=random.choice(client_collections),
            comment=random.choice(COMMENTS_TEXT),
        )

    print(f"  {target_wine} comentarios en vinos, {target_colln} en colecciones de cliente.")


# ──────────────────────────────────────────────
# Massive seed (large dataset)
# ──────────────────────────────────────────────

def run_massive():
    """
    Insert a large dataset intended for load testing and frontend development:
    20 providers, 10 clients, 100 wines, 10 provider collections,
    10 client collections, 30 comments.
    """
    print("\n========================================")
    print("  SEED MASIVO")
    print("========================================\n")

    print("► Creando países y ciudades...")
    cities = create_cities()
    print(f"  {len(cities)} ciudades listas.\n")

    print("► Creando 20 proveedores...")
    providers = create_providers(cities)
    print(f"  {len(providers)} proveedores.\n")

    print("► Creando 10 clientes...")
    clients = create_clients(cities)
    print(f"  {len(clients)} clientes.\n")

    print("► Creando 100 vinos...")
    wines = create_wines(providers, cities, count=100)
    print()

    print("► Creando tipos de colección...")
    types = create_types()
    print(f"  {len(types)} tipos.\n")

    print("► Creando 10 colecciones de proveedor...")
    prov_collections = create_provider_collections(providers, types, wines, count=10)
    print()

    print("► Creando 10 colecciones de cliente...")
    client_collections = create_client_collections(clients, wines, count=10)
    print()

    print("► Creando 30 comentarios...")
    create_comments(clients, wines, client_collections, total=30)
    print()

    print_summary()


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else '--basic'

    if mode == '--massive':
        run_massive()
    elif mode == '--basic':
        run_basic()
    else:
        print(f"Unknown mode '{mode}'. Use --basic or --massive.")
        sys.exit(1)
