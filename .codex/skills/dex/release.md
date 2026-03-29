# /dex release

Release one dex marketplace plugin with a version bump, commit, tag, push, and GitHub Release.

## Usage

`/dex release tools` — patch bump `tools`
`/dex release tools minor` — minor bump `tools`
`/dex release tools major` — major bump `tools`

Supported plugins: `core`, `design`, `tools`

## Steps

Run these as bash commands from the repo root. Stop on any failure.

### 1. Preflight checks

```bash
cd ~/dex

PLUGIN="${1:-}"
BUMP="${2:-patch}"

case "$PLUGIN" in
  core|design|tools) ;;
  *) echo "ERROR: First arg must be one of: core, design, tools"; exit 1 ;;
esac

BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
  echo "ERROR: Must be on main branch (currently on $BRANCH)"
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "ERROR: Worktree is dirty. Commit or stash changes first."
  git status --short
  exit 1
fi

if ! git ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
  echo "ERROR: Cannot reach git remote. Check auth."
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI is required to publish GitHub Releases."
  exit 1
fi
```

### 2. Bump the selected plugin version

```bash
PLUGIN_JSON="plugins/$PLUGIN/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

CURRENT=$(python3 -c "import json; print(json.load(open('$PLUGIN_JSON'))['version'])")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$BUMP" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  *) echo "ERROR: Invalid bump type: $BUMP (use patch, minor, or major)"; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
TAG="$PLUGIN-v$NEW_VERSION"

echo "Bumping $PLUGIN: $CURRENT -> $NEW_VERSION ($BUMP)"
```

### 3. Check the tag does not already exist

```bash
if git tag -l "$TAG" | grep -q .; then
  echo "ERROR: Tag $TAG already exists"
  exit 1
fi
```

### 4. Update version files

```bash
python3 - <<PY
import json

plugin_json = "$PLUGIN_JSON"
marketplace_json = "$MARKETPLACE_JSON"
plugin = "$PLUGIN"
new_version = "$NEW_VERSION"

with open(plugin_json) as fh:
    data = json.load(fh)
data["version"] = new_version
with open(plugin_json, "w") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")

with open(marketplace_json) as fh:
    data = json.load(fh)
for entry in data.get("plugins", []):
    if entry.get("name") == plugin:
        entry["version"] = new_version
with open(marketplace_json, "w") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")
PY
```

### 5. Commit, tag, and push

```bash
git add "$PLUGIN_JSON" "$MARKETPLACE_JSON"
git commit -m "release($PLUGIN): v$NEW_VERSION"
git tag "$TAG"
git push origin HEAD
git push origin "$TAG"
```

### 6. Create the GitHub Release

Use GitHub Releases as the changelog surface, not tags alone.

```bash
NOTES_FILE=$(mktemp)
cat > "$NOTES_FILE" <<EOF
## Summary
- Released \`$PLUGIN\` plugin v$NEW_VERSION

## Changelog
- Describe the user-facing changes in this release
- Mention any important migration or behavior notes

## Versioning
- Marketplace plugin: \`$PLUGIN\` -> \`$NEW_VERSION\`
EOF

gh release create "$TAG" \
  --title "$PLUGIN v$NEW_VERSION" \
  --notes-file "$NOTES_FILE"

rm -f "$NOTES_FILE"
```

### 7. Done

```text
Released $PLUGIN v$NEW_VERSION
Published tag: $TAG
GitHub Releases now carries the changelog for this plugin release.
```
