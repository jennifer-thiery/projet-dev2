# Guide d'utilisation de données utilisant la db

comment faire pour utiliser la base de données dans le projet. 

## 1. Si juste affichage de données

Pour aller chercher des données dans la base de données, il sufit juste d'aller appeller self.app.tournament qui est literalement la classe Tournament. après il sufit d'itérer dedans

## 2. Si on veut faire des modifications/suppresions dans la base de données

Pour modifications il faut faire la requete SQL avec les fonctions prévu et après faire reload_tournament() pour que la mise a jour s'affiche (attention elle est déjà faites dans la db) sur l'écran.

## 3. Schématique de la base de données
voici un schéma de la base de données :

```mermaid

tkt ça arrive je galere juste avec mermaid

```