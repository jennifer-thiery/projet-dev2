# Guide d'utilisation de données utilisant la db

comment faire pour utiliser la base de données dans le projet. 

## 1. Si juste affichage de données

Pour aller chercher des données dans la base de données, il sufit juste d'aller appeller self.app.tournament qui est literalement la classe Tournament. après il sufit d'itérer dedans

## 2. Si on veut faire des modifications/suppresions dans la base de données

Pour modifications il faut faire la requete SQL avec les fonctions prévu et après faire reload_tournament() pour que la mise a jour s'affiche (attention elle est déjà faites dans la db) sur l'écran.

## 3. Schématique de la base de données
voici un schéma de la base de données :

```mermaid
erDiagram
    brackets {
        text type PK
        text phase
    }
    pools {
        text bracket_type PK,FK
        integer number PK
    }
    pool_players {
        text bracket_type PK,FK
        integer pool_number PK,FK
        integer position UK
        text licence_number PK,FK
    }
    matches {
        text bracket_type PK,FK
        text label PK
        integer position
        integer pool_number FK
        text type
        text first_licence FK
        text second_licence FK
    }
    match_sets {
        text bracket_type PK,FK
        text match_label PK,FK
        integer position PK
        integer first_points
        integer second_points
    }
    bracket_players {
        text bracket_type PK,FK
        integer position UK
        text licence_number PK,FK
    }
    players {
        text licence_number PK
        integer position UK
        text firstname
        text lastname
        text birthdate
        text club
        text federation_ranking
        text email
        text phone_number
        integer second_bracket
    }
    brackets ||--o{ bracket_players : "bracket_type"
    players ||--o{ bracket_players : "licence_number"
    brackets ||--o{ pools : "bracket_type"
    pools ||--o{ pool_players : "bracket_type"
    bracket_players ||--o{ pool_players : "bracket_type"
    brackets ||--o{ matches : "bracket_type"
    pools ||--o{ matches : "bracket_type"
    bracket_players ||--o{ matches : "bracket_type"
    bracket_players ||--o{ matches : "bracket_type"
    matches ||--o{ match_sets : "bracket_type"

```