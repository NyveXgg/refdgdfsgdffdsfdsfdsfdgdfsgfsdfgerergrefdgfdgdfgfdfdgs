import os

FOLDER = "C:\\Windows\\System32"         
EXTENSION = ".tsunami"

EXCLUDE_STRING = ".tsunami"

DRY_RUN = False             
QUIET = True           

def get_free_name(base_path):
    i = 0
    while True:
        suffix = f"({i})" if i > 0 else ""
        candidate = f"{base_path}{suffix}{EXTENSION}"
        if not os.path.exists(candidate):
            return candidate
        i += 1

def main():
    renamed = 0
    skipped = 0
    errors = 0

    for root, dirs, files in os.walk(FOLDER):
        for name in files:
            try:
                # exclude by string
                if EXCLUDE_STRING and EXCLUDE_STRING.lower() in name.lower():
                    skipped += 1
                    continue

                old_path = os.path.join(root, name)
                base, _ = os.path.splitext(old_path)
                new_path = get_free_name(base)

                if DRY_RUN:
                    if not QUIET:
                        print(f"DRY: {old_path} -> {new_path}")
                    continue

                try:
                    os.rename(old_path, new_path)
                    renamed += 1
                    if not QUIET:
                        print(f"Rename: {old_path} -> {new_path}")
                except:
                    errors += 1
                    continue

            except:
                errors += 1
                continue

    print(f"\nSummary: renamed={renamed}, skipped={skipped}, errors={errors}")

if __name__ == "__main__":
    main()
