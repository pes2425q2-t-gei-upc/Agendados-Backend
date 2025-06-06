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

# NOT LIST

## IN SCOPE

- Localitzar en un mapa els esdeveniments.
- Geolocalització de l'usuari en el mapa.
- Cercador d'esdeveniments, es podrà filtrar per un camp de text lliure i per paràmetres (data, localització, preu i categoria).
- Filtrador d'esdeveniments per diferents camps (data, localització, preu...).
- Reportar/bloquejar usuaris (només té accés a aquesta funcionalitat l'usuari administrador).
- Algorisme de recomancions d'esdeveniments segons les preferències de l'usuari.
- Xat de text grupal per als esdeveniments.
- Pàgina d'administració de l'aplicació.
- Multi idioma (català, castellà i anglès).
- Opció per a guardar esdeveniments i consultar-los a posteriori, junt amb l'opció de consultar l'històric d'esdeveniments.
- Calendari intern d'esdeveniments i opció per a guardar un esdeveniment en un calendari extern (integració amb google calendar).
- Notificacions relacionades amb els esdeveniments.
- Gestió d'usuari (registrar-se, login, edició de l'idioma, informació de perfil, preferències, contrasenya...).
- Sistema d'amistat entre usuaris (unidireccional, no es un sistema de seguiment).
- Valoració dels esdeveniments als que s'ha assistit.
- Diferents assoliments al arribar a una fita de esdeveniments guardats/assistits (gamificació)

## OUT OF SCOPE

- Compra d'entrades dels esdeveniments que es mostren a l'aplicació.
- Xats privats entre usuaris.
- Diversos xats grupals per a un mateix esdeveniment.
- Creació d'esdeveniments des de l'aplicació per empreses d'esdeveniments.
- Edició d'esdeveniments des de l'aplicació per empreses d'esdeveniments.
- Report/bloqueig d'usuaris.
- Sistema de subscripció o "prèmium" de pagament per a obtenir avantatges a l'aplicació.
- Possibilitat d'enviar qualsevol fitxer que no sigui text per al xat grupal (fotografies, àudios, vídeos...).
- Opció de m'agrada a un esdeveniment i que altres usuaris puguin veure-ho.
- Moderació automàtica dels xats dels esdeveniments amb sistema automàtic de banejos.

## UNRESOLVED

- Imatge de perfil configurable per l'usuari.
- Possibilitat d'enviar invitacions a altres usuaris d'esdeveniments a través de l'aplicació.
- Possibilitat de l'usuari d'ajustar prioritats des del perfil per al sistema de recomancions (p.e prioritzar esdeveniments propers, barats...).
- Ús de model d'intel·ligència artificial per a les recomancions d'esdeveniments.
- Sistema de sales privades entre usuaris per a decidir a quin esdeveniment volen acudir. Bàsicament, un usuari podrà crear una sala i convidar a diversos amics, quan es dona inici a la sala a cada un dels usuaris els aniran apareixent esdeveniments amb el format del scroll de Tinder fins que es doni un "match". Aquest "match" es donarà quan tots els usuaris de la sala indiquin que estan interessats en el mateix esdeveniment.
