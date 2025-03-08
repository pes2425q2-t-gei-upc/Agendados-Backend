# Agendados Backend

# Instruccions per a inicialitzar el projecte

## 1. Crear .env
En el fitxer .env.example es troben totes les variables que s'han d'incloure en el .env del projecte per a que funcioni correctament.

## 2. Creació de la imatge de Docker
Correr la següent comanda per a crear la imatge:
```bash
    docker build -t django-docker .
    docker compose up --build
```

## 3. Execució de la imatge de Docker
A partir d'aquesta comanda ja podrem correr el nostre projecte en el contenidor virtual de Docker:
```bash
    docker compose up -d
```

## 4. Shell de Docker
En cas de voler tenir accés a la shell del contenidor de Django des de la nostra pròpia terminal podem executar la següent comanda: 
```bash
    make shell
```

# Scripts del projecte
## Correr el formatter
Per al projecte fem servir el formatter black, per a executar-lo simplement entrem al contenidor de docker i executem:
```bash
    black .
```
