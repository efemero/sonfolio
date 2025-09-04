# Sonfolio — Contexte Projet (minimal)

- Objectif: convertir des images de partitions en code LilyPond.
- Portée: lire uniquement la musique et les indications textuelles musicales dans la portée (ex: "meno mosso", "tacet 1×"). Ignorer titres, compositeur, copyright, instrument, en-têtes/pieds de page.
- Multi‑voix: pour toute portée multi‑voix, produire une partition (un fichier LilyPond) par voix. L’ordre des voix est de haut vers bas.
- Nommage des sorties multi‑voix: `voice1`, `voice2`, … (où `voice1` = voix du haut).
- Canon LilyPond: utiliser une représentation canonique (espaces/ordre stables, sans commentaires) pour l’entraînement et la sortie.
- Données existantes: ~50 partitions déjà tapées à la main pour entraînement/validation.

## Modules
- data-gen (Python): générer paires image ↔ LilyPond (avec variations et déformations), en respectant « une partition par voix ».
- training (Python): entraîner le modèle image → LilyPond sur le sous-ensemble canonique; valider.
- inference (Rust): outil CLI qui lit une image et sort le(s) fichier(s) LilyPond (un par voix si applicable).

## Étapes immédiates
- Démarrer par le module data-gen (structure et conventions), guidé pas à pas.
