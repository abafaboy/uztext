"""Command line interface: ``uztext <command> [text ...]``.

Text commands read their arguments (joined by spaces) or, with no
arguments, standard input. ``sum-words`` reads amounts from its arguments
or one amount per line from standard input.
"""

from __future__ import annotations

import argparse
import sys

from . import (
    __version__,
    from_new,
    normalize,
    search_key,
    sum_words,
    to_cyrillic,
    to_latin,
    to_new,
)

TEXT_COMMANDS = {
    "to-latin": (to_latin, "any script -> current Latin (oʻ gʻ sh ch)"),
    "to-cyrillic": (to_cyrillic, "any script -> Cyrillic"),
    "to-new": (to_new, "any script -> new Latin (ö ğ ş ç)"),
    "from-new": (from_new, "new Latin -> current Latin"),
    "normalize": (normalize, "fix apostrophe look-alikes (ʻ U+02BB, ʼ U+02BC)"),
    "search-key": (search_key, "fold scripts and apostrophes into one search key"),
}


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="uztext", description="Uzbek text toolkit.")
    p.add_argument("--version", action="version", version=f"uztext {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    for name, (_, help_text) in TEXT_COMMANDS.items():
        cmd = sub.add_parser(name, help=help_text, description=help_text)
        cmd.add_argument("text", nargs="*", help="text (default: read stdin)")
    sw = sub.add_parser(
        "sum-words",
        help="amount -> Uzbek words for invoices",
        description="Write amounts in words. Reads one amount per line from "
        "stdin when no amount is given.",
    )
    sw.add_argument("amount", nargs="*", help='e.g. 1250000.50 or "1 250 000,50"')
    sw.add_argument("--script", choices=("latin", "cyrillic", "new"), default="latin")
    sw.add_argument("--currency", default="so'm")
    sw.add_argument("--subunit", default="tiyin")
    return p


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stdin):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = _parser().parse_args(argv)
    if args.command == "sum-words":
        amounts = args.amount or [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
        try:
            for amount in amounts:
                print(sum_words(amount, args.script, args.currency, args.subunit))
        except ValueError as exc:
            print(f"uztext: {exc}", file=sys.stderr)
            return 2
        return 0
    fn = TEXT_COMMANDS[args.command][0]
    if args.text:
        print(fn(" ".join(args.text)))
    else:
        sys.stdout.write(fn(sys.stdin.read()))
    return 0
