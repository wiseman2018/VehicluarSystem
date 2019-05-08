# VehicluarSystem

### How to run the app

#### Step 1: ```source venv/Scripts/activate
#### Step 2:  ´export APP_SETTINGS="config.DevelopmentConfig"´
#### Step 3:  ´export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/vehicle"´

#### Step 4: ´python app.py´

### access the database with: psql vehicle


## Running Migration
``` python manage.py db migrate -m "added exclusive table" 

