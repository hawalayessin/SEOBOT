# SEORobot

SEORobot est une application Django permettant d'automatiser la création et la gestion de pages et de catégories sur un site WordPress à partir de mots-clés et de métadonnées fournis dans un fichier CSV. L'application interagit avec l'API REST de WordPress et stocke les informations localement dans une base de données PostgreSQL.

## Fonctionnalités principales
- Interface web pour soumettre un mot-clé (metaTitle) et générer/créer une page WordPress associée.
- Création automatique de catégories si elles n'existent pas.
- Mise à jour ou création de pages sur WordPress via l'API REST.
- Stockage local des pages, catégories et métadonnées SEO.

## Structure du projet
```
SEORobot/
├── SEORobot/                # Configuration principale Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── SEORobotapp/             # Application principale
│   ├── models/              # Modèles Django (Page, Category, SEOMetadata)
│   ├── views/               # Vues (addPage)
│   ├── templates/           # Templates HTML (addPage.html)
│   ├── forms.py             # Formulaires Django
│   ├── data.csv             # Fichier de données d'exemple
│   └── ...
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── ...
```

## Modèles principaux
- **Page** : titre, URL, contenu, catégorie, date de mise à jour
- **Category** : titre de la catégorie
- **SEOMetadata** : clé/valeur de métadonnée SEO liée à une page

## Installation et utilisation
### Prérequis
- [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/)

### Lancer l'application avec Docker
1. Placez-vous dans le dossier `SEORobot`.
2. Construisez et démarrez les services :
   ```sh
   docker-compose up --build
   ```
3. L'application Django sera accessible sur [http://localhost:8000](http://localhost:8000)
4. Adminer (interface de gestion PostgreSQL) sera accessible sur [http://localhost:8080](http://localhost:8080)

### Utilisation de l'interface
- Accédez à `/addPage/` pour soumettre un mot-clé (metaTitle) présent dans le fichier `data.csv`.
- Le formulaire crée ou met à jour la page correspondante sur WordPress et enregistre les informations localement.

## Format du fichier CSV attendu
Le fichier `data.csv` doit être placé dans `SEORobotapp/` et suivre ce format :

```
categoryTitle;metaTitle;metadescription;content
Category1;metatitle1;metadescription1;content1
Category2;metatitle2;metadescription2;content2
```

## Variables importantes
- L'URL, le nom d'utilisateur et le mot de passe d'application WordPress sont définis en dur dans la vue `addPage`. Modifiez-les selon votre environnement.
- La base de données PostgreSQL est configurée dans `docker-compose.yml` et `settings.py`.

## Dépendances principales
- Django
- psycopg2-binary
- requests
- PostgreSQL

## Notes
- Pour ajouter d'autres champs ou logiques, modifiez les modèles et la vue principale dans `SEORobotapp/views/addPage.py`.
- Pensez à sécuriser les identifiants WordPress et la clé secrète Django pour un usage en production.
