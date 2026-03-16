#!/usr/bin/env python3
"""
Create ELAN (.eaf) files from participant/operator SRT transcriptions and split utterances into turns.

What this script does
---------------------
- reads pairs of SRT files with transcriptions for participant and operator;
- optionally links available media files when --link-media is used;
- creates these tiers in this order:
    participant
    operator
    production_annotation
    confidence_production
    backchannels
- fills:
    - participant: transcription annotations from participant SRT
    - operator: transcription annotations from operator SRT
    - production_annotation: empty annotations spanning participant turns
- leaves these tiers empty:
    - confidence_production
    - backchannels

Turn definition
---------------
To define the turns, the script merges consecutive IPUs from one speaker into a turn until the other
speaker starts a non-overlapping contribution.

Examples
--------
python3 create_eaf_from_srt.py /path/to/data
python3 create_eaf_from_srt.py /path/to/data --keys sub-01_run-01_human_low
python3 create_eaf_from_srt.py /path/to/data --link-media
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

import pympi


INPUT_TIERS = ["participant", "operator"]
OUTPUT_TIERS = ["production_annotation"]
TIER_MAP = {"participant": "production_annotation"}

DESIRED_TIER_ORDER = [
    "participant",
    "operator",
    "production_annotation",
    "confidence_production",
    "backchannels",
]

SRT_RE = re.compile(
    r"^(sub-\d+_run-\d+)_(participant|operator)_([A-Za-z0-9-]+)_([A-Za-z0-9-]+)\.srt$",
    re.IGNORECASE,
)
KEY_RE = re.compile(r"^sub-\d+_run-\d+_[A-Za-z0-9-]+_[A-Za-z0-9-]+$", re.IGNORECASE)


def srt_time_to_ms(timestamp: str) -> int:
    """Convert SRT timestamp (HH:MM:SS,mmm) to milliseconds."""
    hms, ms = timestamp.strip().split(",")
    h, m, s = hms.split(":")
    return int(h) * 3_600_000 + int(m) * 60_000 + int(s) * 1_000 + int(ms)


def parse_srt(filepath: Path):
    """Yield (start_ms, end_ms, text) from a simple SRT file."""
    text = filepath.read_text(encoding="utf-8").strip()
    if not text:
        return

    blocks = re.split(r"\n\s*\n", text)
    for block in blocks:
        lines = [line.rstrip("\n") for line in block.strip().splitlines()]
        if len(lines) < 3:
            continue

        try:
            times = lines[1].split(" --> ")
            start = srt_time_to_ms(times[0])
            end = srt_time_to_ms(times[1])
        except Exception:
            continue

        transcript = " ".join(line.strip() for line in lines[2:]).strip()
        yield start, end, transcript


def collect_keys(data_dir: Path) -> list[str]:
    """Collect shared keys from participant SRT files.

    Example key:
        sub-01_run-01_human_low
    """
    keys = []
    for srt_path in sorted(data_dir.glob("sub-*_run-*_participant_*.srt")):
        m = SRT_RE.match(srt_path.name)
        if not m:
            continue
        prefix, speaker, group, engagement = m.groups()
        if speaker.lower() != "participant":
            continue
        keys.append(f"{prefix}_{group}_{engagement}")
    return sorted(set(keys))


def parse_key(key: str) -> tuple[str, str, str]:
    """Split key into prefix, group, engagement.

    Example:
        sub-01_run-01_human_low -> (sub-01_run-01, human, low)
    """
    if not KEY_RE.fullmatch(key):
        raise ValueError(
            f"Invalid key format: {key}. Expected sub-XX_run-XX_group_engagement"
        )
    prefix, group, engagement = key.rsplit("_", 2)
    return prefix, group, engagement


def add_media_links(eaf: pympi.Elan.Eaf, files: dict[str, Path], key: str) -> None:
    """Link any available media files. Missing files are skipped."""
    participant_denoised = files["participant_denoised"]
    participant_raw = files["participant_raw"]
    operator_audio = files["operator_audio"]

    linked_any = False

    if participant_denoised.exists():
        eaf.add_linked_file(str(participant_denoised))
        linked_any = True
    else:
        print(f"Note: {key} has no participant denoised audio (skipped)")

    if participant_raw.exists():
        eaf.add_linked_file(str(participant_raw))
        linked_any = True
    else:
        print(f"Note: {key} has no participant raw audio (skipped)")

    if operator_audio.exists():
        eaf.add_linked_file(str(operator_audio))
        linked_any = True
    else:
        print(f"Note: {key} has no operator audio (skipped)")

    if not linked_any:
        print(f"Note: {key} created without linked media")


def add_tiers_in_order(eaf: pympi.Elan.Eaf) -> None:
    """Create all required tiers in the desired order."""
    for tier in DESIRED_TIER_ORDER:
        if tier not in eaf.get_tier_names():
            eaf.add_tier(tier)


def add_transcriptions(eaf: pympi.Elan.Eaf, participant_srt: Path, operator_srt: Path) -> None:
    """Populate participant and operator transcription tiers."""
    for start, end, text in parse_srt(participant_srt):
        eaf.add_annotation("participant", start, end, text)

    for start, end, text in parse_srt(operator_srt):
        eaf.add_annotation("operator", start, end, text)


def add_turn_annotations(eaf: pympi.Elan.Eaf) -> None:
    """
    Identify turns from transcription annotations and add empty annotations
    to the production tier.
    """
    ipus = []
    for speaker in INPUT_TIERS:
        ipus.extend(
            (start, end, speaker)
            for start, end, _ in eaf.get_annotation_data_for_tier(speaker)
        )
    ipus.sort()

    current_turns = {s: None for s in INPUT_TIERS}
    merged_turns = {s: [] for s in INPUT_TIERS}

    def finalize_turn(speaker):
        turn = current_turns[speaker]
        if turn:
            merged_turns[speaker].append((turn[0], turn[1]))
        current_turns[speaker] = None

    for start, end, speaker in ipus:
        other = [s for s in INPUT_TIERS if s != speaker][0]

        if current_turns[speaker] is None:
            current_turns[speaker] = [start, end]
        else:
            current_turns[speaker][1] = max(current_turns[speaker][1], end)

        if current_turns[other]:
            _, other_end = current_turns[other]
            if start < other_end:
                continue
            else:
                finalize_turn(other)

    for speaker in INPUT_TIERS:
        finalize_turn(speaker)

    for start, end in merged_turns["participant"]:
        eaf.add_annotation(TIER_MAP["participant"], start, end, "")


def build_file_map(data_dir: Path, key: str) -> dict[str, Path]:
    """Return expected input file paths for one sub/run/group/engagement key."""
    prefix, group, engagement = parse_key(key)
    return {
        "participant_denoised": data_dir / f"{prefix}_participant-denoised.wav",
        "participant_raw": data_dir / f"{prefix}_participant-raw.wav",
        "operator_audio": data_dir / f"{prefix}_operator.wav",
        "participant_srt": data_dir / f"{prefix}_participant_{group}_{engagement}.srt",
        "operator_srt": data_dir / f"{prefix}_operator_{group}_{engagement}.srt",
    }


def create_eaf_for_key(
    data_dir: Path,
    key: str,
    overwrite: bool = False,
    suffix: str = "",
    link_media: bool = False,
) -> Path | None:
    """Create one EAF file for a given sub/run/group/engagement key."""
    files = build_file_map(data_dir, key)

    if not (files["participant_srt"].exists() and files["operator_srt"].exists()):
        print(f"Skipping {key}: missing participant or operator SRT file")
        return None

    out_file = data_dir / f"{key}{suffix}.eaf"
    if out_file.exists() and not overwrite:
        print(f"Skipping {key}: output already exists ({out_file.name}). Use --overwrite to replace it.")
        return None

    eaf = pympi.Elan.Eaf()

    if link_media:
        add_media_links(eaf, files, key)

    add_tiers_in_order(eaf)
    add_transcriptions(eaf, files["participant_srt"], files["operator_srt"])
    add_turn_annotations(eaf)

    eaf.to_file(str(out_file))
    print(f"Saved {out_file}")
    return out_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create ELAN .eaf files from participant/operator SRT files."
    )
    parser.add_argument(
        "data_dir",
        type=Path,
        help="Folder containing sub-XX_run-XX_participant_GROUP_ENG.srt / sub-XX_run-XX_operator_GROUP_ENG.srt and optional wav files.",
    )
    parser.add_argument(
        "--keys",
        nargs="*",
        default=None,
        help="Optional list of keys to process, e.g. --keys sub-01_run-01_human_low",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output .eaf files.",
    )
    parser.add_argument(
        "--suffix",
        default="",
        help="Optional suffix before .eaf in the output filename (default: none).",
    )
    parser.add_argument(
        "--link-media",
        action="store_true",
        help="Link available wav files into the EAF. If omitted, create the EAF without media links.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_dir = args.data_dir.expanduser().resolve()

    if not data_dir.exists():
        print(f"Data directory does not exist: {data_dir}", file=sys.stderr)
        return 1

    keys = args.keys if args.keys else collect_keys(data_dir)
    if not keys:
        print(
            f"No matching participant SRT files found in {data_dir} for pattern sub-*_run-*_participant_*_*.srt",
            file=sys.stderr,
        )
        return 1

    created = 0
    for key in keys:
        try:
            result = create_eaf_for_key(
                data_dir=data_dir,
                key=key,
                overwrite=args.overwrite,
                suffix=args.suffix,
                link_media=args.link_media,
            )
        except ValueError as e:
            print(f"Skipping {key}: {e}")
            continue
        if result is not None:
            created += 1

    print(f"Done. Created {created} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
