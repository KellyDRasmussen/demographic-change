#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image

def white_to_transparent(img: Image.Image, threshold: int = 240) -> Image.Image:
    """
    Convert near-white pixels to transparent.
    threshold: 0..255; higher means more aggressive (treats more light colors as white).
    """
    # Ensure RGBA
    img = img.convert("RGBA")
    pixels = img.getdata()

    new_pixels = []
    for r, g, b, a in pixels:
        if a == 0:
            # Already transparent, keep it
            new_pixels.append((r, g, b, a))
            continue

        # Mark pixel transparent if it's "white-ish" (all channels above threshold)
        if r >= threshold and g >= threshold and b >= threshold:
            new_pixels.append((r, g, b, 0))
        else:
            new_pixels.append((r, g, b, a))

    img.putdata(new_pixels)
    return img

def process_file(src_path: Path, out_dir: Path, suffix: str, threshold: int, overwrite: bool, keep_subdirs: bool):
    try:
        with Image.open(src_path) as im:
            out_img = white_to_transparent(im, threshold=threshold)

            stem = src_path.stem
            # Always save as PNG to preserve transparency
            out_name = f"{stem}{suffix}.png"

            if keep_subdirs:
                rel_parent = src_path.parent
                # Re-root under the provided input directory
                out_file = out_dir / rel_parent.relative_to(args.input_dir) / out_name
            else:
                out_file = out_dir / out_name

            out_file.parent.mkdir(parents=True, exist_ok=True)

            if out_file.exists() and not overwrite:
                print(f"Skip (exists): {out_file}")
                return

            save_params = {}
            # Preserve DPI if available
            if "dpi" in im.info:
                save_params["dpi"] = im.info["dpi"]

            out_img.save(out_file, format="PNG", **save_params)
            print(f"Saved: {out_file}")
    except Exception as e:
        print(f"Error processing {src_path}: {e}")

def gather_images(input_dir: Path, recursive: bool, exts):
    pattern = "**/*" if recursive else "*"
    for p in input_dir.glob(pattern):
        if p.is_file() and p.suffix.lower().lstrip(".") in exts:
            yield p

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make white/near-white backgrounds transparent across a folder of images."
    )
    parser.add_argument("input_dir", type=Path, help="Folder containing images")
    parser.add_argument("-o", "--output-dir", type=Path, default=None,
                        help="Where to save results (default: input_dir)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recurse into subfolders")
    parser.add_argument("-k", "--keep-subdirs", action="store_true",
                        help="Mirror the input subfolder structure inside the output dir")
    parser.add_argument("-s", "--suffix", default="_transparent",
                        help="Suffix for output filenames (default: _transparent)")
    parser.add_argument("-t", "--threshold", type=int, default=240,
                        help="0-255. Higher = more pixels become transparent (default: 240)")
    parser.add_argument("--ext", nargs="*", default=["png", "jpg", "jpeg", "webp"],
                        help="File extensions to process (default: png jpg jpeg webp)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files in the output directory")

    args = parser.parse_args()
    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir).resolve()

    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    images = list(gather_images(input_dir, args.recursive, set(e.lower() for e in args.ext)))
    if not images:
        print("No matching images found.")
        raise SystemExit(0)

    for img_path in images:
        process_file(
            src_path=img_path,
            out_dir=output_dir,
            suffix=args.suffix,
            threshold=args.threshold,
            overwrite=args.overwrite,
            keep_subdirs=args.keep_subdirs,
        )

    print("Done.")
