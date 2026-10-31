"""Évalue la traduction français → éwé sur le corpus synthétique.

Usage (depuis backend/) :
    .venv/bin/python eval_translation.py [--limit N]

La qualité finale doit être relue par des locuteurs compétents en éwé (§8.2).
"""

import argparse
import time

from app.translation import translate_fr_to_ewe
from corpus_fr_ewe import CORPUS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Nombre de phrases à traduire")
    args = parser.parse_args()

    items = CORPUS[: args.limit] if args.limit else CORPUS
    print(f"{len(items)} phrases à traduire\n")

    for i, item in enumerate(items, 1):
        t0 = time.time()
        try:
            out = translate_fr_to_ewe(item["fr"])
        except Exception as exc:
            out = f"ERREUR : {type(exc).__name__}"
        dt = time.time() - t0
        print(f"[{i}/{len(items)}] ({item['category']}) {dt:.1f}s")
        print(f"  FR : {item['fr']}")
        print(f"  EWE: {out}")
        print()


if __name__ == "__main__":
    main()
