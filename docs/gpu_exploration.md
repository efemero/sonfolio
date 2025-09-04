# Sonfolio — Exploration GPU (Résumé)

## Focus — AMD RX 7900 XT 20 GB
- Plateforme: Linux (Ubuntu 22.04/24.04) + ROCm 6.x. Sous Windows, l’entraînement GPU natif n’est pas supporté officiellement; viser Linux.
- Précision: BF16 recommandé (bon support RDNA3); sinon FP16.
- Capacité attendue: batch 1–2 à 768 px, 2–4 à 512 px (avec gradient accumulation pour un effectif 8–16). Idéal pour fine‑tune de modèles base/small image→texte.
- Perf: proche 4070 Ti/4080 selon kernels; absence de certains fused CUDA kernels, donc privilégier gradient checkpointing + attention slicing. Flash‑Attention ROCm existe mais pas obligatoire.
- Inférence Rust: accélération GPU via onnxruntime ROCm non triviale; options pratiques:
  - CPU en Rust, ou
  - micro‑service Python (Torch/ONNX ROCm) appelé par le CLI Rust.

Installation (checklist condensée)
- Installer ROCm 6.x selon AMD (kernel supporté, user dans `video`/`render`).
- PyTorch ROCm: installer la roue `torch==2.x` compatible ROCm 6.x depuis les index officiels AMD/PyTorch.
- Vérification rapide:
  - `python -c "import torch; print(torch.version.__version__, torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"`
  - Attendu: `True` et un nom AMD (API CUDA proxifiée via HIP).

Preset d’entraînement conseillé (7900 XT)
- Images: 512–640 px côté long; crops par portée/système; N&B si utile.
- Modèle: vision-encoder-decoder base/small; tokenizer BPE sur LilyPond canonique.
- Mémoire: BF16 autocast; gradient checkpointing; accumulation (eff. batch 8–16);
  éventuel `torch.set_float32_matmul_precision("medium")`.
- Optim: AdamW 8‑bit optionnel (bitsandbytes ROCm si dispo), clipping grad, early stop.

Points d’attention
- Certaines ops/kernels sont moins optimisés que CUDA; anticiper un throughput inférieur à A100/4090.
- `torch.compile` sur ROCm 6.x progresse mais peut être instable selon versions.
- ONNX Runtime ROCm: souvent nécessite build from source; à éviter au début.

## GPU local détecté (actuel)
- NVIDIA GeForce RTX 3050 Ti Laptop — 4 GB VRAM
- Driver/CUDA: 570.153.02 / CUDA 12.8

## Faisabilité entraînement par configuration (résumé)
- 4 GB NVIDIA (machine actuelle)
  - Prototypage uniquement. Modèle petit, images ≤ 512–640, batch 1, FP16/BF16, checkpointing.
  - Recadrer par portée; éviter grosses augmentations online.

- 16 GB NVIDIA (ex: 4070 Ti Super)
  - Fine‑tune sérieux; ~0.4–1.5 s/step (512–640). 100k steps ≈ 11–42 h.
  - FP16/BF16, checkpointing, accumulation; crops par portée; sortie LilyPond canonique.

## Cloud — Lambda.ai (on‑demand)
- Prix / GPU·h (1 GPU)
  - B200 180 GB: $4.99
  - H100 80 GB: $2.99
  - A100 80 GB: $1.79
  - A100 40 GB: $1.29
  - V100 16 GB: $0.55
- Coût / h d’un nœud 8× (si 8 GPUs utilisés)
  - B200: $39.92 | H100: $23.92 | A100 80: $14.32 | A100 40: $10.32 | V100: $4.40
- Estimations « marge haute »
  - 200 GPU·h: B200 ~$998 | H100 ~$598 | A100 80 ~$358 | A100 40 ~$258 | V100 ~$110
  - 500 GPU·h: B200 ~$2,495 | H100 ~$1,495 | A100 80 ~$895 | A100 40 ~$645 | V100 ~$275
- Méthode de calcul pratique
  - Mesurer localement sec/step (sur 300–500 steps) → GPU·h = steps × sec/step / 3600.
  - Appliquer un facteur d’accélération estimé (vs 3050 Ti): A100 80 ≈ 8–15×, H100 ≈ 12–25×.

## Quand passer au cloud
- Besoin d’images ≥ 768–1024 px, batch ≥ 4, ou itérations 5–10× plus rapides.
- Entraînements longs (≥ 200 GPU·h) ou multi‑expériences parallèles.

## Recommandations rapides
- Chemin privilégié local: viser une RX 7900 XT 20 GB (Linux + ROCm 6.x) pour un fine‑tune confortable à 512–640 px.
- Démarrer sur 4 GB: valider pipeline, tokenizer, “smoke” training; compiler LilyPond des sorties.
- Cloud pour vitesse: A100 80 GB (sweet spot) ou H100 si contrainte de temps mur.
- Inférence Rust + AMD: commencer en CPU ou via micro‑service Python ROCm.

## Prochaines actions (si/qd décidé)
- Mesurer sec/step local (512 px, modèle base, 300–500 steps).
- Fixer objectif steps et résolution cible (512/640/768).
- Choisir cible GPU (local 16–20 GB ou cloud A100/H100) et estimer coût/temps.
