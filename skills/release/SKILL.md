---
name: release
description: "Bump version, commit, tag, push, and re-symlink. Usage: /dex:release [patch|minor|major]"
---

# /dex:release

Release a new version of the dex plugin. Bumps version, commits, tags, pushes to GitHub, and re-creates the dev symlink.

## Usage

`/dex:release` — patch bump (default)
`/dex:release minor` — minor bump
`/dex:release major` — major bump

## Steps

Run these as bash commands from the `~/dex` directory. Stop on any failure.

### 1. Preflight checks

```bash
cd ~/dex

# Must be on main branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
  echo "ERROR: Must be on main branch (currently on $BRANCH)"
  exit 1
fi

# Must have clean worktree (except version files which we'll change)
if [ -n "$(git status --porcelain)" ]; then
  echo "ERROR: Worktree is dirty. Commit or stash changes first."
  git status --short
  exit 1
fi

# Must be able to reach remote
if ! git ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
  echo "ERROR: Cannot reach git remote. Check auth."
  exit 1
fi
```

### 2. Bump version

Read current version from `plugin.json`, bump per the argument (default: patch).

```bash
BUMP="${1:-patch}"  # patch, minor, or major
CURRENT=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$BUMP" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  *) echo "ERROR: Invalid bump type: $BUMP (use patch, minor, or major)"; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "Bumping: $CURRENT -> $NEW_VERSION ($BUMP)"
```

### 3. Check tag doesn't exist

```bash
if git tag -l "v$NEW_VERSION" | grep -q .; then
  echo "ERROR: Tag v$NEW_VERSION already exists"
  exit 1
fi
```

### 4. Update version files

```bash
python3 -c "
import json
for f in ['.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']:
    with open(f) as fh: d = json.load(fh)
    if 'version' in d: d['version'] = '$NEW_VERSION'
    for p in d.get('plugins', []):
        if p.get('name') == 'dex': p['version'] = '$NEW_VERSION'
    if 'metadata' in d and 'version' in d['metadata']: d['metadata']['version'] = '$NEW_VERSION'
    with open(f, 'w') as fh: json.dump(d, fh, indent=2); fh.write('\n')
"
```

### 5. Commit, tag, push

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "release: dex v$NEW_VERSION"
git tag "v$NEW_VERSION"
git push origin HEAD
git push origin "v$NEW_VERSION"
```

### 6. Re-create dev symlink

```bash
if [ -x "$(pwd)/scripts/dev-link.sh" ]; then
  ./scripts/dev-link.sh
fi
```

### 7. Done

```
Released dex v$NEW_VERSION
Teammates can update with: /plugin update dex@nawwwal-dex
```
