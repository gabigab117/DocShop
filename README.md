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

10. Créer le modèle utilisateur (normalement début de projet)<br>
nouvelle app car en général les users on gère dans une app dédiée
On créer un abstractuser avec un pass. Puis ds setting AUTH_USER_MODEL = "accounts.Shopper"

11. formulaire d'inscription <br>
Dans le html on gère le lien inscription avec un if not user.is_authenticated

TOUJOURS Y PENSER : request.POST est un Dictionnaire
request.POST("username), clé username car dans el html input avec name="username"

on récupère notre modele d'utilisateur avec get_user_model
get_user_model va chercher dans settings.AUTH_USER_MODEL

12. Afficher l'utilisateur connecté et afficher la vue de log out<br>
déjà dans le admin.py
ensuite base.html is authenticated on affiche le username
Aussi afficher un logout.

13. Views logout_user<br>

14. connexion<br>
si POST, authenticate, si user login

15. la gestion du panier <br>
1 modèle articles, 1 modèle panier
modele order : on utilise l'utilisateur et product en foreign key
modele cart : panier

16. ajouter un article dans le panier<br>
Créer une vue def add_to_cart et on utilise le template detail.html
'''
get_or_create retourne deux choses : l'objet en question qu'il ai été créé ou qu'il existe déjà et aussi
une autre variable pour savoir si l'objet a été créé ou non.
'''

17. afficher le panier <br>
url

18. le lien vers le panier<br>
Je peux faire if user.cart et afficher le nombre d'articles {{ user.cart.orders.count }}

19. supprimer le panier<br>
récupérer le panier, supprimer ce qu'il y a dedans et supprimer le panier

20. modifier les modèles order et cart<br>
ordered date on déplace vers le modèle order

21. modifier le delete cart<br>
la logique de la vue on va la mettre dans le modele Cart en surchargeant la méthode delete
et il faut modifier la vue add to cart car Order.objects.get_or_create(user=user, ordered=False, product=product) afin
de ne pas modifier les Order déjà en True.

22. package stripe<br>
créer un compte et installer. pip install --upgrade stripe
Pour authentifier les requêtes i lfaut une clé api avec stripe (onglet dev et clé api)
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / "shop/.env")
STRIPE_API_KEY = env("STRIPE_API_KEY")

23. vue session de paiement<br>
ds vue importer stripe et 
stripe.api_key = settings.STRIPE_API_KEY
doc https://stripe.com/docs/payments/accept-a-payment
copier coller du code de session à return
penser à locale="fr"

24. champ pour l'id stripe<br>
modifier le modele du produit por add champ qui stock l'identifiant de stripe
fera le lien entre bdd et stripe

25. créer les produits sur stripe<br>
stripe onglet produits. On prend la clé price

26. intégrer le checkout stripe<br>
dans la vue checkout avec compréhension de liste et line_items

27. ajouter la vue de succès<br>
Créer vue qui retourne un template. Et on modifie success_url du checkout
  # il faut une url absolue car je suis sur Stripe à ce moment-là
        success_url=request.build_absolute_uri(reverse('checkout-success')),

28. installer Stripe Cli<br>
https://youtu.be/jJu8vQH7hLY
doc stripe create your event handler

29. ajouter webhook stripe<br>
https://stripe.com/docs/cli/listen
Créer vue stripe webhook
stripe listen --forward-to 127.0.0.1:8000/stripe-webhook/