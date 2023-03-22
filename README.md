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
il faut une url absolue car je suis sur Stripe à ce moment-là
        success_url=request.build_absolute_uri(reverse('checkout-success')),

28. installer Stripe Cli<br>
https://youtu.be/jJu8vQH7hLY
doc stripe create your event handler

29. ajouter webhook stripe<br>
https://stripe.com/docs/cli/listen
Créer vue stripe webhook
stripe listen --forward-to 127.0.0.1:8000/stripe-webhook/
https://stripe.com/docs/payments/checkout/fulfill-orders

30. compléter la transaction <br>
Dans la vue stripe_webhook on veut récupérer l'évènement checkout.session.completed

31. renseigner l'adresse webhook stripe
stripe - developers - webhook

32. utiliser email comme user
champ utilisé pour se connecter : (il est automatiquement considéré comme requis)
USERNAME_FIELD = "email"
champs obligatoires pour la création d'un compte / je laisse vide pour le moment
REQUIRED_FIELDS = []

33. créer un gestionnaire d'utilisateurs personnalisé
le manager, du coup on doit le modifier
34. Ajouter un modele adresse de livraison <br>
on va le rajouter dans le models.Py de accounts

35. ajouter le champ pour le pays avec iso3166<br>
compréhension de liste dans un choices

36. vue de profil et formulaire d'édition<br>
forms.py on passe par un modelform qui utilise Shopper
un html profil.html
les valeurs initiales, utiliser model_to_dict()
afficher msg d'erreur on passe par django.contrib messages

37. ajouter info client stripe <br>
vue create session checkout
utiliser la doc stripe. pour l'email c'est customer_email
https://stripe.com/docs/api/checkout/sessions/object
On va modifier modele shopper pour récupérer l'identifiant stripe

38. sauvegarder l'id et l'adresse de livraison <br>
on passe par une clé customer de stripe. Il faut rajouter un champ stripe_id dans le modele shopper
voir store views.

39. afficher les adresses dans la vue de profil <br>
accounts/views.py
Et dans la foreign keys de shippingadresses mettre un related_name
passer au context de profil.html

40. modifier affichage de l'adresse <br>
méthode str à modif, accounts/models.py
on créer une constante, on applique .format, en utilisant une copie de l'attribut self.__str__
puis unpack

41. autre méthode pour afficher dans le html<br>
je préfère utiliser un fichier html pour afficher les addresses plutôt qu'un fichier py
en gabarit il existe include pour intégrér un fichier html dans un autre

42. envoyer l'user enregistré à Stripe <br>
cette fois si j'ai déjà un user.stripe_id on va l'envoyer à stripe
créer une struc conditionnelle dans create_checkout_session

43. changer l'adresse par dft stripe <br>
dans le modele shipping address on va ajouter une méthode set_default pour indiquer l'adresse par def
annotation de type :
 user: Shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE, related_name="addresses")
https://stripe.com/docs/api/customers/update

44. changer l'adresse par defaut dans la BDD <br>
créer un chanp default dans notre modele
récupérer toutes les adresses et attribuer False
Et notre instance en cours True puis on save

45. modifier l'adresse par défaut dans la vue <br>
address.html on va ajouter des indications pour dire si def ou non
puis créer une vue avec pk pour modifier l'adresse par def

46. modifier les quantités d'articles dans le panier <br>
on va utiliser le modele form set, utiliser plusieurs formulaires
store forms.py
et vue cart on va créer le modelformset_factory()
puis cart.html on affiche nos forms en gabarit
pour traiter la requete je pourrais le faire dans ma vue cart directement. Mais je vais créer une autre vue
donc créer un chemin d'url et views update_quantities
pour lier le formulaire à la vue dans le html on mets après method action="{% url 'update-quantities' %}"