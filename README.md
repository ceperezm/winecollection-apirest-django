# WineCollection API

WineCol is a RESTful API designed for the oenophile community. It allows client applications to explore wine catalogs, interact with providers, manage personal collections, view other clients' profiles, and access their public collections.

## Technologies

- **Backend:** Django, Django REST Framework (DRF), SQLite (Development)
- **Filters & Search:** Django Filter, custom DRF integrations.

## Key Features

- **Community Directory:** Endpoints to discover other clients, view their profiles, and explore their collections. Includes support for dynamic searches without forced pagination.
- **Wine Catalog:** Advanced filtering for wines (year, variety, chemical characteristics).
- **Collection Management:** Strict privacy and ownership logic. Users can only manage their own collections, while having read-only access to others'.
- **Providers:** Detailed directory of providers and wineries with dynamic sorting and search capabilities.

## Project Structure

- `/users`: Django app managing authentication, permissions, and Client views (Directory).
- `/coltns`: Django app for managing wine Collections.
- `/wines`: Django app for the main wine catalog.
- `/comments`: Rating and commenting system.
- `/locations`: Geographical locations management.

## Development Setup

### Prerequisites
- Python 3.10+

### Quick Start
1. Create your virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the environment and install dependencies:
   ```bash
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
