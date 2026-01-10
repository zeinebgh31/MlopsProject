FROM python:3.12-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# On force la mise à jour de pip
RUN pip install --upgrade pip

# On copie et on installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste du projet
COPY . .

EXPOSE 8000

# Utilisation de la commande recommandée pour FastAPI
CMD ["python", "-m", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]