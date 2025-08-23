# Make drirectory
mkdir -p src/components
mkdir -p src/entity
mkdir -p src/constants/training_pipeline
mkdir -p src/exceptions
mkdir -p src/loggings
mkdir -p src/pipeline
mkdir -p src/clouds
mkdir -p src/utils/main_utils
mkdir -p src/utils/ml_utils
mkdir -p src/utils/ml_utils/metric
mkdir -p src/utils/ml_utils/model

mkdir -p data_schema

mkdir -p Network_Data

mkdir -p .github/workflows

mkdir -p Notebooks

# Creating files
touch src/__init__.py
touch src/components/__init__.py
touch src/components/data_ingestion.py
touch src/components/data_validation.py
touch src/components/data_transformation.py
touch src/components/model_trainer.py
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
touch src/utils/main_utils/__init__.py
touch src/utils/main_utils/utils.py
touch src/utils/ml_utils/__init__.py
touch src/utils/ml_utils/metric/__init__.py
touch src/utils/ml_utils/metric/metric.py
touch src/utils/ml_utils/model/__init__.py
touch src/utils/ml_utils/model/model.py

touch data_schema/schema.yaml

touch .github/workflows/main.yml

touch Dockerfile
touch .env
touch setup.py
touch app.py
touch requirements.txt
touch push_data.py

echo "Directry and files created successfuly"