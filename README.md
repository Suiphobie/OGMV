# Description

"Où Garer Mon Vélo" est une application web Streamlit conçue pour aider les utilisateurs à trouver des emplacements de stationnement pour vélos dans la région Île-de-France. En utilisant les données de Data.gouv.fr, l'application fournit une interface facile à utiliser pour localiser les places de parking à proximité en fonction des adresses saisies par les utilisateurs.

# Fonctionnalités
 - Carte Interactive : Visualisez les emplacements de stationnement pour vélos sur une carte interactive.
 - Fonctionnalité de Recherche : Les utilisateurs peuvent entrer une adresse pour trouver des emplacements de stationnement pour vélos à proximité.
 - Rayon de Recherche Personnalisable : Ajustez le rayon de recherche pour affiner les résultats.
 - Options de Filtre : Filtrez les places de parking selon des attributs tels que la couverture, le type d'accès, l'exigence de paiement, la surveillance et le type.
 - Marqueur de Localisation de l'Utilisateur : Une épingle rouge pour indiquer l'adresse saisie par l'utilisateur.

# Comment Utiliser
1. Entrez une adresse dans la région Île-de-France.
2. Ajustez le rayon de recherche et le nombre maximum d'emplacements de stationnement à afficher.
3.Appliquez des filtres en fonction de vos préférences pour les attributs des places de stationnement.
4. Visualisez les résultats sur la carte interactive. Cliquez sur les marqueurs pour plus d'informations.

# Installation et Configuration
Pour exécuter cette application localement, suivez ces étapes :

1. Cloner le répertoire
git clone (https://github.com/Suiphobie/OGMV

2. Navigate to the app directory:
cd your-repo-name

3. Install the required Python packages:
pip install -r requirements.txt

4. Run the app:
streamlit run main.py


## Stack Techno utilisées
- Streamlit
- Python
- Pandas
- Folium
- Streamlit-Folium
- Geopy

## Source de données
La data utiliser dans ce projet provient de  [Data.gouv.fr](https://www.data.gouv.fr/fr/datasets/stationnement-velo-en-ile-de-france/#/resources).

## Auteurs
Coder par [Anoussone Simuong](https://www.linkedin.com/in/anousimuong/))
Design par [Jenny Lin](https://www.linkedin.com/in/jenny%2Dlin%2Dxin%2Dru/) 

## Remerciements
Merci à l'ESD pour l'opportunité et les ressources afin de crée cette app !

## Licence
Ce projet est sous la licence BSD - Voir [license.md] pour les détails. 
