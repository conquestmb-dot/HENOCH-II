#!/usr/bin/env python3
"""II Księga Henocha: 73 MP3 files, Edge TTS, FFmpeg assembly."""
import argparse
import asyncio
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEXT_DIR = ROOT / "teksty"
MP3_DIR = ROOT / "mp3"
OUTPUT = ROOT / "II_Ksiega_Henocha_1-73_CALOSC.mp3"
DEFAULT_VOICE = "pl-PL-MarekNeural"
EXISTING = {
    1: "https://resource2.heygen.ai/text_to_speech/25796852147f415d9072b465b2da452f/0eb85e6e8710473b82f7e88609ba3053/id=a23e6d55b4ff4cd096c81ad5c60f39f4.mp3",
    2: "https://resource2.heygen.ai/text_to_speech/25796852147f415d9072b465b2da452f/0eb85e6e8710473b82f7e88609ba3053/id=9cafb31c1f8844dc9a446bd50ea51fd8.mp3",
    3: "https://resource2.heygen.ai/text_to_speech/25796852147f415d9072b465b2da452f/0eb85e6e8710473b82f7e88609ba3053/id=b083567bc2a3436380d6735b3682a6bc.mp3",
}

def destination(n):
    return MP3_DIR / f"Henoch_II_{n:03d}.mp3"

def is_mp3(path):
    if not path.exists() or path.stat().st_size < 500:
        return False
    with path.open("rb") as f:
        header = f.read(3)
    return header == b"ID3" or (
        len(header) >= 2 and header[0] == 255 and (header[1] & 224) == 224
    )

def download():
    MP3_DIR.mkdir(parents=True, exist_ok=True)
    for n, url in EXISTING.items():
        path = destination(n)
        if is_mp3(path):
            print(f"[{n}] istnieje, pomijam")
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
            tmp = path.with_suffix(".download")
            tmp.write_bytes(data)
            if not is_mp3(tmp):
                tmp.unlink(missing_ok=True)
                raise ValueError("Pobrany plik nie jest MP3")
            tmp.replace(path)
            print(f"[{n}] pobrano MP3")
        except Exception as ex:
            print(f"[{n}] nie pobrano: {ex}")

async def generate(start, end, voice):
    try:
        import edge_tts
    except ImportError as ex:
        raise RuntimeError("Zainstaluj: py -m pip install edge-tts") from ex
    MP3_DIR.mkdir(parents=True, exist_ok=True)
    for n in range(start, end + 1):
        path = destination(n)
        if is_mp3(path):
            print(f"[{n}] MP3 już jest; pomijam")
            continue
        txt = TEXT_DIR / f"Henoch_II_{n:03d}.txt"
        if not txt.exists():
            print(f"[{n}] brak pełnego tekstu: {txt.name}")
            continue
        source = txt.read_text(encoding="utf-8-sig").strip()
        if len(source) < 30 or source.startswith("WSTAW "):
            print(f"[{n}] tekst pusty lub zastępczy; pomijam")
            continue
        try:
            print(f"[{n}] synteza głosem {voice}")
            await edge_tts.Communicate(source, voice).save(str(path))
            if not is_mp3(path):
                raise ValueError("Niepoprawny wynik MP3")
        except Exception as ex:
            path.unlink(missing_ok=True)
            print(f"[{n}] błąd: {ex}")

def check():
    missing = [n for n in range(1, 74) if not is_mp3(destination(n))]
    print(f"Gotowych MP3: {73-len(missing)}/73")
    print("Brakujące:", ", ".join(map(str, missing)) if missing else "brak")
    return not missing

def join():
    if not check():
        raise RuntimeError("Montaż przerwany: brak wszystkich 73 MP3.")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("Nie znaleziono ffmpeg w PATH.")
    playlist = ROOT / "lista_ffmpeg.txt"
    playlist.write_text(
        "".join(f"file 'mp3/Henoch_II_{n:03d}.mp3'\n" for n in range(1, 74)),
        encoding="utf-8",
    )
    # Re-encode to reconcile different MP3 bitrates and sample rates.
    subprocess.run(
        [ffmpeg, "-hide_banner", "-y", "-f", "concat", "-safe", "0",
         "-i", str(playlist), "-vn", "-ar", "44100", "-ac", "1",
         "-c:a", "libmp3lame", "-b:a", "128k", str(OUTPUT)],
        check=True,
    )
    print(f"Gotowy audiobook: {OUTPUT}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["download", "generate", "check", "join", "all"])
    parser.add_argument("--start", type=int, default=4)
    parser.add_argument("--end", type=int, default=73)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    args = parser.parse_args()
    if not 1 <= args.start <= args.end <= 73:
        parser.error("Zakres musi obejmować rozdziały od 1 do 73")
    if args.action in ("download", "all"):
        download()
    if args.action in ("generate", "all"):
        asyncio.run(generate(args.start, args.end, args.voice))
    if args.action == "check":
        check()
    if args.action in ("join", "all"):
        join()

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"BŁĄD: {exc}", file=sys.stderr)
        raise SystemExit(1)
