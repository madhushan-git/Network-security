# Make drirectory
mkdir -p src/components
mkdir -p src/entity
mkdir -p src/constants/training_pipeline
mkdir -p src/exceptions
mkdir -p src/loggings
mkdir -p src/pipeline
mkdir -p src/clouds
mkdir -p src/utils

mkdir -p Network_Data

mkdir -p .github/workflows

mkdir -p Notebooks

# Creating files
touch src/__init__.py
touch src/components/__init__.py
touch src/components/data_ingestion.py
touch src/entity/__init__.py
touch src/entity/config_entity.py
touch src/entity/artifact_entity.py
touch src/constants/__init__.py
touch src/constants/training_pipeline/__init__.py
touch src/exceptions/__init__.py
touch src/exceptions/exceptions.py
touch src/loggings/__init__.py
touch src/loggings/logger.py
touch src/pipeline/__init__.py
touch src/clouds/__init__.py
touch src/utils/__init__.py

touch .github/workflows/main.yml

touch Dockerfile
touch .env
touch setup.py
touch app.py
touch requirements.txt
touch push_data.py

echo "Directry and files created successfuly"