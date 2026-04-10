# Blog Django MICDA

Projet d'examen realise avec Django pour le Master 2 MICDA.

## Fonctionnalites livrees

- affichage de la liste des articles sur la page d'accueil
- affichage detaille d'un article
- CRUD complet des articles avec Class-Based Views
- interface d'administration Django personnalisee
- gestion des fichiers statiques
- ajout et affichage d'images sur les articles
- deconnexion depuis la page d'accueil

## Environnement recommande

- Python 3.12+
- pip

## Installation rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_blog_demo
python3 manage.py runserver
```

## Acces a l'application

- Blog: `http://127.0.0.1:8000/`
- Administration Django: `http://127.0.0.1:8000/admin/`

## Identifiants de test

Apres execution de la commande `python3 manage.py seed_blog_demo`:

- nom d'utilisateur: `admin`
- mot de passe: `AdminMicda2026!`

## Donnees de demonstration creees automatiquement

La commande `seed_blog_demo` cree ou remet a jour:

- 1 compte administrateur
- 1 article publie: `Bienvenue sur le blog MICDA`
- 1 article brouillon: `Article en preparation`

## Procedure de test pour le correcteur

### 1. Verifications automatiques

```bash
python3 manage.py check
python3 manage.py makemigrations --check
python3 manage.py test
```

### 2. Tests manuels cote visiteur

1. Ouvrir `http://127.0.0.1:8000/`
2. Verifier que la page d'accueil s'affiche correctement avec le CSS
3. Verifier que l'article publie apparait dans la liste
4. Verifier que le brouillon n'apparait pas pour un visiteur
5. Ouvrir le detail de l'article publie
6. Verifier l'affichage du contenu complet et de l'image par defaut

### 3. Tests manuels cote administrateur

1. Ouvrir `http://127.0.0.1:8000/admin/`
2. Se connecter avec:
   - `admin`
   - `AdminMicda2026!`
3. Verifier que le modele `Article` est disponible dans l'administration
4. Creer un nouvel article avec un titre, un contenu, un statut et une image
5. Modifier un article existant
6. Supprimer un article
7. Revenir sur `http://127.0.0.1:8000/` et verifier l'impact sur la liste

### 4. Tests manuels depuis l'interface publique

Une fois connecte en administrateur:

1. Cliquer sur `Nouvel article` depuis la page d'accueil
2. Creer un article via le formulaire public
3. Modifier un article via le bouton `Modifier`
4. Supprimer un article via le bouton `Supprimer`
5. Tester le bouton `Deconnexion` dans l'en-tete

## Commandes utiles

### Lancer le serveur

```bash
python3 manage.py runserver
```

### Creer ou recreer les donnees de demonstration

```bash
python3 manage.py seed_blog_demo
```

### Creer un autre superutilisateur si besoin

```bash
python3 manage.py createsuperuser
```

## Structure principale

- `blog/models.py` : modele `Article`
- `blog/views.py` : vues CBV `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`
- `blog/admin.py` : personnalisation de l'administration
- `blog/templates/` : templates HTML
- `static/css/style.css` : style du blog

## Remarque

Les identifiants ci-dessus sont des identifiants de demonstration pour faciliter la correction du projet.
