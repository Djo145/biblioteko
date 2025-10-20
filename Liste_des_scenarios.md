# Liste des scénarios

## Installer l’application
    Description : Décrit le processus d’installation de l’application sur différents médias
  
    Acteurs : L’utilisateur, le serveur de mis à disposition de l’application.
	
    Précondition : Le téléchargement de l’application doit être possible depuis le média (ordinateur ou smartphone)  de l’utilisateur
	
    Étapes :
        1. Le futur utilisateur ouvre son navigateur ou le market store de son système d’exploitation.
        2. Le futur utilisateur saisit le nom de l’application.
        3. La page de sélection affiche la description de l’application et ses informations légales, notamment celles correspondant aux partages des œuvres et à leurs droits d’auteurs.
        4. Le futur utilisateur sélectionne l’application et l’installe.

## Devenir Membre
	
    Description : Un anonyme
	
    Acteurs : un utilisateur Anonyme, FranceConnect, les différents mandataires de FranceConnecte.
	
    Prérequis : le scénario « Installer l’application » a été exécuté sans erreur.
	
    Étapes :
    1. L’utilisateur anonyme lance l’application.
    2. L’application détecte que c’est son premier lancement sur le média.
    3. L’application affiche une page d’information.
    4. L’application propose à l’utilisateur de se connecter via FranceConnect.
    5. L’application propose de créer un compte ne pouvant déposer ou louer des œuvres.
    6. L’utilisateur choisit de se connecter via FranceConnect.
    7. L’application propose les différents sites d’identification.
    8. L’utilisateur choisit l’un des sites.
    9. L’utilisateur s’authentifie.
    10. L’application reçoit les informations de connexion.
    11. L’application affiche toutes les actions, dont celles de dépôt.

    Scénario alternatif:
	(branchement à l’étape 6)
    1. L’utilisateur choisit de créer un nouvel identifiant.
    2. L’application demande le nom , prénom et date de naissance de l’utilisateur.
    3. L’utilisateur saisit les informations.
    4. À partir de ces informations, l’application crée
    • un identifiant unique garantissant l’anonymat,
    • une paire de clés, publique et privée, pour enregistrer les opérations qui seront faites.
    5. L’application transmet l’identifiant et la clé publique au serveur de l’association.
    6. L’application affiche les actions permises.
    7. L’application affiche la liste des œuvres dans le domaine public.

	Documents :
		Page d’information affichée :  pour expliquer l’objectif de l’application, ses possibilités et précise que l’utilisateur devra utiliser un compte FranceConnect s’il veut pouvoir louer des œuvres sous droits ou déposer des œuvres.


## Devenir Bibliothécaire

	Description : Un membre demande à devenir bibliothécaire.
	
    Acteurs : Membre, Bibliothécaire
	
    Prérequis : Il existe au moins un Bibliothécaire actif.
	
    Étapes :
    1. Un membre demande à l’application à devenir bibliothécaires.
    2. L’application enregistre la demande et soumet la demande aux bibliothécaires.
    3. L’application sur le média d’un autre bibliothécaire transmet à son utilisateur la demande pour modération.
    4. L’application demande au bibliothécaire s’il :
    • accepte,
    • rejette,
    • n’a pas d’avis,
    • ou souhaite ignorer la candidature.
    5. Le bibliothécaire indique à l’application quel est son choix.
    6. L’application partage de façon anonyme et unique ce choix avec les autres applications sur les médias des autres Bibliothécaires.
    7. Le Bibliothécaire peut modifier son choix tant que le délai imparti n’est pas écoulé.
    8. Une fois le délai écoulé, les applications des bibliothécaires propagent aux autres applications la décision automatique prise ainsi :
    • Si la majorité des bibliothécaires ont accepté la candidature du membre alors celui-ci devient bibliothécaire.
    9. Le membre consulte la décision depuis l’application sur son média.
    10. Si l’application du futur bibliothécaire constate qu’il est promu bibliothécaire alors il reçoit les droits lui permettant d’accéder à l’ensemble des contenus et de pouvoir accepter ou refuser les modérations.
    11. Sinon l’application indique le refus de sa promotion.
    
    Scénarios alternatifs :
    La majorité des bibliothécaires refuse la promotion.

	Scénarios erreurs :
	Données, documents, écrans :


## Se connecter à la bibliothèque

    Description : Authentifie un utilisateur pour accéder à son espace personnel.

    Acteurs : Utilisateur, serveur d’authentification.

    Préconditions : Le compte utilisateur doit exister et être activé.

    Étapes :
    1. L’utilisateur ouvre l’application.
    2. Il saisit ses identifiants.
    3. Le serveur vérifie les informations et génère un jeton d’accès (JWT).
    4. L’utilisateur est redirigé vers son tableau de bord.

## Accéder à la liste des œuvres
    Description : Permet de naviguer et rechercher des œuvres dans la bibliothèque.
    
    Acteurs : Utilisateur.
    
    Préconditions : L’utilisateur est connecté et la 
    
    bibliothèque contient des œuvres publiées.
    
    Étapes :
    1. L’utilisateur accède à la section “Catalogue”.
    2. Il peut filtrer par type (livres, musique, vidéo, articles), par catégorie, ou par mots-clés.
    3. L’application affiche la liste des œuvres disponibles.
    4. L’utilisateur sélectionne une œuvre pour consulter sa fiche détaillée (titre, auteur, description, droits, format, disponibilité).


## Déposer une œuvre numérisée
    Description : Un membre a numérisé une œuvre et souhaite la partager avec la bibliothèque pour enrichir son fond.
	
    Acteurs : Membre authentifié
	
    Prérequis : Le membre est authentifié sur l’application par FranceConnect
	
    Étapes :
    1. Le membre authentifié demande à l’application à partager une œuvre.
    2. L’application affiche un formulaire de saisie d’information concernant l’œuvre.
    3. Le membre authentifié saisit les informations, et joint le fichier de l’œuvre numérisée.
    4. L’application demande confirmation de l’envoi.
    5. Le membre authentifié confirme l’envoi.
    6. L’application enregistre le  fichier dans le répertoire « à modérer ».
    7. L’application crée un numéro de transaction et l’enregistre dans le fichier journal local.
    8. L’application transmet le fichier, ses informations et les numéros de transaction au dépôt sur le serveur de l’association.
    9. Les serveurs de l’association notifient les bibliothécaires qu’une nouvelle œuvre est en attente de modération.
    10. L’application indique au membre que son partage est en attente de modération.

    Scénarios alternatifs :

    Scénarios erreurs :
		Erreur de connexion avec le serveur.

    Données, documents, écrans :


## Modérer une œuvre numérisée
	Description : Les bibliothécaires sont avertis des numérisations d’œuvres à modérer.

	Acteurs : Bibliothécaire, serveur de la Bibliothèque Nationale de France

	Prérequis :Le fichier d’une œuvre numérisée doit avoir été déposé et soumis en modération

	Étapes :
    1. L’un des bibliothécaires se connecte à l’application.
    2. L’application lui affiche la liste des fichiers d’œuvres numérisées soumises.
    3. Le bibliothécaire positionne ses filtres pour ne voir que les œuvres susceptibles de l’intéresser.
    4. L’application n’affiche que les résultats correspondant aux filtres.
    5. Le bibliothécaire positionne les tris pour les afficher dans l’ordre voulu.
    6. L’application affiche les résultats dans l’ordre souhaité.
    7. Le bibliothécaire sélectionne un fichier d’une œuvre.
    8. L’application affiche les informations saisies par le membre ayant soumis l’œuvre.
    9. L’application affiche un lecteur spécifique au type de fichier.
    10. Le bibliothécaire parcourt l’œuvre.
    11. Le bibliothécaire complète les informations sur l’œuvre.
    12. Le bibliothécaire accepte l’œuvre en précisant sa nature.
    13. @TODO
	Scénarios alternatifs :
	Scénarios erreurs :
	Données, documents, écrans :

## Consulter une œuvre du domaine public
    Description : Permet à un utilisateur de visualiser et lire une œuvre appartenant au domaine public directement depuis la bibliothèque.
    Acteurs : Utilisateur, serveur de la bibliothèque.
    Préconditions :
        L’utilisateur est connecté à l’application (ou accède en invité si l’accès libre est autorisé).
        L’œuvre est classée comme « domaine public » et validée par un bibliothécaire.
    Étapes :
    1. L’utilisateur accède à la section « Catalogue » ou « Fond commun ».
    2. Il sélectionne une œuvre libre de droits.
    3. Le serveur affiche la fiche complète de l’œuvre (titre, auteur, date, résumé, format).
    4. L’utilisateur clique sur « Lire en ligne » ou « Télécharger ».
    5. Le fichier est affiché dans le lecteur intégré ou téléchargé localement.

## Remplir les informations concernant une œuvre

    Description : Permet à un membre qui dépose une œuvre de compléter les métadonnées nécessaires à sa classification.

    Acteurs : Membre (auteur du dépôt), serveur, dépôt Git.

    Préconditions :
        Le fichier de l’œuvre a été téléchargé dans la section « Proposer une œuvre ».
        L’utilisateur est authentifié.
    Étapes :
    1. Le membre accède au formulaire de dépôt.
    2. Il saisit les informations requises :
        Titre, auteur, année, catégorie, langue, type d’œuvre, statut des droits.
    3. Le serveur vérifie la cohérence des données (format, champs obligatoires).
    4. Les métadonnées sont sauvegardées dans metadata.yml associé à l’œuvre.
    5. Un message confirme la bonne prise en compte des informations.

## Consulter les informations concernant une œuvre
    Description : Permet de consulter les métadonnées et le statut d’une œuvre présente dans la bibliothèque.

    Acteurs : Utilisateur, serveur.

    Préconditions :
        L’œuvre existe dans la bibliothèque.
        L’utilisateur est connecté ou dispose d’un accès public.      
    Étapes :
    1. L’utilisateur recherche une œuvre via le moteur de recherche ou le catalogue.
    2. Il sélectionne l’œuvre désirée.
    3. Le serveur affiche la fiche détaillée (titre, auteur, catégories, description, disponibilité, type de droits, date de dépôt).
    4. L’utilisateur peut également consulter le lien vers le fichier Markdown ou le texte OCR.

## Modifier les informations concernant une œuvre
    Description : Permet à un bibliothécaire ou à un administrateur d’éditer les métadonnées d’une œuvre après modération.
    
    Acteurs : Bibliothécaire, administrateur.
    
    Préconditions :
        L’utilisateur a les droits de modification.
        L’œuvre est déjà enregistrée dans le dépôt Git.
    Étapes :
    1. Le bibliothécaire accède à la fiche de l’œuvre.
    2. Il clique sur « Modifier les informations ».
    3. Il met à jour un ou plusieurs champs du fichier metadata.yml.
    4. Le serveur valide les changements (format, cohérence des droits).
    5. Une nouvelle version est enregistrée dans le dépôt Git (commit).
    6. L’historique des modifications est mis à jour et consultable.


## Louer une œuvre sous droits d’auteur
    Description : Permet à un membre d’emprunter temporairement une œuvre protégée par le droit d’auteur.
    
    Acteurs : Membre, serveur d’application, service de chiffrement, dépôt Git.
    
    Préconditions :
        L’utilisateur est connecté et possède un compte valide.
        L’œuvre est disponible à la location.
    Étapes :
    1. L’utilisateur sélectionne une œuvre sous droits d’auteur.
    2. Il clique sur « Louer cette œuvre ».
    3. Le serveur crée une clé de chiffrement spécifique et chiffre le fichier.
    4. La clé est chiffrée avec la clé publique du membre (création de key.enc).
    5. Le fichier est ajouté dans emprunts/<user-id>/<work-id>/.
    6. La durée de location (14 jours) est enregistrée dans la base de métadonnées.
    7. À l’expiration du délai, le fichier devient inaccessible et l’accès est révoqué.


## Passage d’une œuvre dans le domaine public
    Description : Gère automatiquement la transition d’une œuvre protégée vers le domaine public lorsque les droits expirent.
    
    Acteurs : Système, bibliothécaire (validation finale).
    
    Préconditions :
        La date de fin de protection des droits est atteinte.
        Les métadonnées contiennent les informations de copyright.
    
    Étapes :
    1. Le système vérifie régulièrement les œuvres sous droits d’auteur.
    2. Il détecte les œuvres dont la période de protection est expirée.
    3. Un rapport automatique est généré pour le bibliothécaire.
    4. Le bibliothécaire confirme ou annule la mise à jour du statut.
    5. L’œuvre est déplacée vers le répertoire fond_commun/.
    6. Une notification est envoyée aux membres.


## Diffusion d’une œuvre libre de droits

    Description : Permet au système de propager automatiquement une œuvre devenue libre à tous les membres disposant d’espace partagé.
    
    Acteurs : Serveur, membres abonnés.
    
    Préconditions :
        L’œuvre est classée comme “libre de droits” ou vient de passer dans le domaine public.
        Les membres ont activé la synchronisation automatique.
    Étapes :
    1. Le système détecte une nouvelle œuvre libre.
    2. Il crée une copie dans fond_commun/.
    3. Le serveur synchronise cette œuvre sur les espaces partagés des membres.
    4. Une notification informe les utilisateurs de la disponibilité.
    5. L’œuvre devient consultable et téléchargeable depuis leur interface.



public book

the book author could be able to transfer the not public book with the moderator

    Titre, auteur, année, catégorie, lan