"""
CLI (squelette) pour le module data-gen.

Exigences:
- Basé sur Tyro (sous-commande `tokenize`).
- Pas de logique réelle pour l’instant; uniquement des placeholders.

SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

import tyro


@dataclass
class Tokenize:
    """Sous-commande: tokenizer (squelette).

    Entrée attendue (ultérieurement): texte LilyPond au format
    `nederlands(a,b,c,d,e,f,g)` normalisé en amont; lecture prévue via python-ly.
    """

    text: Annotated[str, tyro.conf.Positional]  # texte LilyPond (nederlands)
    output: str | None = None  # placeholder: chemin de sortie (non utilisé)
    verbose: int = 0  # placeholder


@dataclass
class About:
    """Sous-commande: affiche des informations sur l'outil (squelette)."""

    verbose: int = 0  # placeholder


# Déclare une somme de sous-commandes; Tyro utilisera les noms de classes.
Command = Tokenize | About


def main() -> None:
    description = (
        "data-gen — outils de génération/traitement (squelette).\n\n" +
        "Sous-commandes: tokenize — squelette sans exécution réelle.\n" +
        "- Entrée cible: nederlands(a,b,c,d,e,f,g) via python-ly.\n" +
        "- Validation: modèles Pydantic dans data_gen.tokenizer.\n"
    )
    cmd = tyro.cli(Command, description=description)

    if isinstance(cmd, Tokenize):
        from .tokenizer import tokenize

        print("[tokenize] Début — impression debug brute de python-ly…")
        _ = tokenize(cmd.text)
        print("[tokenize] Fin — (structure interne encore vide).")
        return
    if isinstance(cmd, About):
        print(
            "data-gen (squelette) — Tyro + Pydantic.\n" +
            "Sous-commandes prévues: tokenize.\n" +
            "Entrée cible: nederlands(a,b,c,d,e,f,g) via python-ly."
        )
        return
