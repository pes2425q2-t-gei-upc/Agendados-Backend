# Agendados Backend

# Instruccions per a inicialitzar el projecte

## 1. Crear .env
En el fitxer .env.example es troben totes les variables que s'han d'incloure en el .env del projecte per a que funcioni correctament.

## 2. Creació de la imatge de Docker
Correr la següent comanda per a crear la imatge:
```bash
    docker build -t django-docker .
    docker compose up --build -d
```

## 3. Shell de Docker
Per a obrir una shell de docker i per tant tenir accés a la consola del conteidor, hem d'executar: 
```bash
    make shell
```

## 4. Execució de les migracions
Des de la shell de docker que hem creat previament, executar:
```bash
    python manage.py migrate
```

## 5. Importació de les dades
Per a importar les dades de la generalitat, primerament s'ha de descarregar el csv des de la url:
https://analisi.transparenciacatalunya.cat/Cultura-oci/Agenda-cultural-de-Catalunya-per-localitzacions-/rhpv-yr4f/about_data
A continuació hem de copiar el fitxer a la carpeta /apps/importer/data i renombrar-lo a events.csv  
Finalment, per a importar les dades ja podem correr la comanda:
```bash
    python manage.py importer
```
    
# Scripts del projecte
## Correr el formatter
Per al projecte fem servir el formatter black, per a executar-lo simplement entrem al contenidor de docker i executem:
```bash
    black .
```

## Buidar les taules de la DB
```bash
    python manage.py flush
```

## Fer correr els tests tot aixo al docker
## Tests unitaris
```bash
    python manage.py test
```
## Tests e22
```bash
    pytest e2e_tests
```
