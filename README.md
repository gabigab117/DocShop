# DocShop
 tuto e commerce
1. mettre en place l'environnement<br>
créer le projet django (env virtuel)
créer l'application store

2. création du modèle Product<br>
Qui contient les informations de notre produit.
   (penser à Pillow pour les ImageFields)
Appliquer les migrations pour la BDD

3. Enregistrer les modèles dans l'interface d'admin<br>
dans l'app, admin.py

4. Création du super utilisateur<br>

5. Connexion à l'admin<br>
methode str du modele

6. templates de base<br>
créer template de base. templates/base.html
créer templates/store/index.html dans l'app (extends)

7. Créer les routes de base<br>
page index vue render url ''

8. Afficher les produits sur la page d'accueil<br>
dans l'index<br>
Pour les images product.thumbnail.url. Mais penser à créer ds setting MEDIA_URL et MEDIA_ROOT <br>
Puis spécifier dans l'url la fonction static<br>
Je déplace le dossier products (images) dans media (ne pas rechercher les ref)<br>
MEDIA_URL = url et MEDIA_ROOT c'est le dossier avec les images

9. Afficher la page de détail du produit
ds le modèle je rajoute le slug que j'ai oublié
Je rajoute une url product product/<str:slug>/
on va utiliser get_object_or_404 (attribué à une variable qu'on utilisera dans le contxt)
puis on lie notre index au détail
On peut accéder au détail avec {{ product.get_absolute_url }}