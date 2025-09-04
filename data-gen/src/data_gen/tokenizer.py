"""
Squelette du tokenizer basé sur Pydantic, avec intention de réutiliser
au maximum les structures de données music21 et d’utiliser python-ly pour
la lecture d’entrées normalisées de type `nederlands(a,b,c,d,e,f,g)`.

Aucune logique réelle n’est encore implémentée; uniquement des modèles et
des fonctions placeholders pour guider l’implémentation future.

SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PitchModel(BaseModel):
    """Hauteur musicale, pensée pour un mapping aisé vers music21.pitch.Pitch.

    - step: lettre de note (a–g) en néerlandais LilyPond (minuscule).
    - accidental: altération textuelle LilyPond ("", "is", "es", …).
    - octave: relatif (compte de ' et ,) ou absolu selon future décision.
    - m21_repr: placeholder pour stocker/aligner une représentation music21.
    """

    step: Literal["a", "b", "c", "d", "e", "f", "g"] = Field(..., description="Nom de note")
    accidental: str = Field(default="", description="Altération LilyPond: is/es/…")
    octave: int = Field(default=0, description="Décalage d’octave (placeholder)")
    m21_repr: str | None = Field(default=None, description="Représentation music21 (placeholder)")


class DurationModel(BaseModel):
    """Durée compatible LilyPond et proche de music21.duration.Duration.

    - den: valeur de note (1,2,4,8,16,…)
    - dots: nombre de points.
    - quarter_length: optionnel, pour s’aligner avec music21 (placeholder).
    """

    den: int = Field(..., ge=1, description="Dénominateur de durée (puissance de 2)")
    dots: int = Field(default=0, ge=0, le=3, description="Nombre de points")
    quarter_length: float | None = Field(
        default=None, description="Durée en noires (music21), placeholder"
    )


class KeySignatureModel(BaseModel):
    """Armure et mode, mappables vers music21.key.Key/KeySignature."""

    tonic: Literal[
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "ais",
        "bes",
        "cis",
        "des",
        "dis",
        "ees",
        "fis",
        "ges",
        "gis",
        "aes",
    ]
    mode: Literal["major", "minor"]
    m21_repr: str | None = None


class TimeSignatureModel(BaseModel):
    """Mesure (ex: 4/4), mappable vers music21.meter.TimeSignature."""

    numerator: int = Field(..., ge=1)
    denominator: int = Field(..., ge=1)
    m21_repr: str | None = None


class NoteModel(BaseModel):
    pitch: PitchModel
    duration: DurationModel
    tie: Literal["NONE", "START", "CONT"] = "NONE"


class RestModel(BaseModel):
    duration: DurationModel


class Event(BaseModel):
    """Union typée d’événements; placeholder générique pour le squelette.

    À spécialiser plus tard via discriminants si nécessaire.
    """

    kind: Literal["NOTE", "REST", "BAR"]
    note: NoteModel | None = None
    rest: RestModel | None = None


class TokenizationResult(BaseModel):
    """Résultat d’une tokenization (squelette)."""

    key: KeySignatureModel | None = None
    time: TimeSignatureModel | None = None
    events: list[Event] = Field(default_factory=list)


def tokenize_nederlands(text: str) -> TokenizationResult:  # placeholder
    """Tokenize un texte LilyPond `nederlands(...)` via python-ly (à venir).

    Squelette: ne fait rien pour l’instant; retourne une structure vide.
    """

    # TODO: utiliser python-ly pour parser en nederlands(a,b,c,d,e,f,g)
    # TODO: convertir dans les modèles Pydantic ci-dessus
    return TokenizationResult()


def detokenize_to_nederlands(result: TokenizationResult) -> str:  # placeholder
    """Rend une structure tokenisée vers du texte LilyPond nederlands (à venir)."""

    # TODO: sérialiser depuis TokenizationResult → texte LilyPond
    return ""


def tokenize(text: str) -> TokenizationResult:
    """Parse un texte LilyPond enrobé et affiche le dump python-ly.

    - Enrobage: \\language "nederlands" \relative c' { <text> }
    - Parcours: ly.music.document(ly.document.Document(snippet))
    - Sortie: impression de `dump()` brute (aucune transformation pour l’instant).
    """

    snippet = (
        "\\language \"nederlands\" "
        "\\relative c' { " + text + " }"
    )

    try:
        import ly.document
        import ly.music

        doc = ly.document.Document(snippet)
        music = ly.music.document(doc)
        try:
            print(music.dump())
        except Exception:
            # Certaines versions exposent dump() via items; fallback minimal
            print(music)
    except Exception as exc:
        print(f"[debug] Échec lecture python-ly: {exc}")

    return TokenizationResult()


__all__ = [
    "PitchModel",
    "DurationModel",
    "NoteModel",
    "RestModel",
    "KeySignatureModel",
    "TimeSignatureModel",
    "Event",
    "TokenizationResult",
    "tokenize",
    "detokenize_to_nederlands",
]
