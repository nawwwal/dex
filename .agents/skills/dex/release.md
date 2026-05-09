# /dex release

Release one dex marketplace plugin with a version bump, commit, tag, push, and GitHub Release.

The repo is both the Claude marketplace and the Codex marketplace:

- Claude reads `.claude-plugin/marketplace.json`, which duplicates plugin versions.
- Codex reads `.agents/plugins/marketplace.json`, whose plugin entries are Git-backed `git-subdir` sources tracking `main`; Codex gets versions from each plugin's `.codex-plugin/plugin.json`.

## Usage

`/dex release core` - patch bump `core`
`/dex release design minor` - minor bump `design`
`/dex release dev` - patch bump `dev`
`/dex release dev initial` - publish the current `dev` version as its first release
`/dex release tools minor` - minor bump `tools`

Supported plugins: `core`, `design`, `dev`, `tools`

## Version bump rules

| Bump | When |
|------|------|
| `patch` | Bug fixes, wording changes, metadata-only updates, or small behavior-preserving edits |
| `minor` | New skills, moved skills with a replacement route, renamed skills with an obvious successor, noticeable behavior changes, or backward-compatible memory/schema changes |
| `major` | Rare. Use only when existing installs cannot keep working without a manual migration: plugin source/manifest shape changes that require reinstall, command contracts removed with no replacement, persistent data formats made unreadable, or an entire plugin discontinued |
| `initial` | First release of a newly added plugin; keep the current manifest version and create its first tag |

Default is `patch` when no bump is specified. When in doubt between `patch` and `minor`, use `minor` if users will notice the change. When in doubt between `minor` and `major`, use `minor`.

Major releases are opt-in, not inferred from cleanup alone. Skill moves, router deletions, renamed skills, or removed duplicate docs are usually `minor` when users have a clear replacement path. A `major` release must name the migration reason before running the release commands.

## Steps

Run these as bash commands from the repo root. Stop on any failure.

### 1. Preflight checks

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

PLUGIN="${1:-}"
BUMP="${2:-patch}"

case "$PLUGIN" in
  core|design|dev|tools) ;;
  *) echo "ERROR: First arg must be one of: core, design, dev, tools"; exit 1 ;;
esac

if [ "$BUMP" = "major" ] && [ -z "${DEX_MAJOR_REASON:-}" ]; then
  echo "ERROR: Major releases require DEX_MAJOR_REASON explaining the manual migration."
  echo "If users have a replacement path, use minor instead."
  exit 1
fi

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
CLAUDE_PLUGIN_JSON="plugins/$PLUGIN/.claude-plugin/plugin.json"
CODEX_PLUGIN_JSON="plugins/$PLUGIN/.codex-plugin/plugin.json"
CLAUDE_MARKETPLACE_JSON=".claude-plugin/marketplace.json"
CODEX_MARKETPLACE_JSON=".agents/plugins/marketplace.json"

CURRENT=$(python3 -c "import json; print(json.load(open('$CLAUDE_PLUGIN_JSON'))['version'])")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$BUMP" in
  initial) ;;
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  *) echo "ERROR: Invalid bump type: $BUMP (use patch, minor, major, or initial)"; exit 1 ;;
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

plugin = "$PLUGIN"
new_version = "$NEW_VERSION"

for path in [
    "$CLAUDE_PLUGIN_JSON",
    "$CODEX_PLUGIN_JSON",
]:
    with open(path) as fh:
        data = json.load(fh)
    data["version"] = new_version
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")

with open("$CLAUDE_MARKETPLACE_JSON") as fh:
    data = json.load(fh)
for entry in data.get("plugins", []):
    if entry.get("name") == plugin:
        entry["version"] = new_version
with open("$CLAUDE_MARKETPLACE_JSON", "w") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")

with open("$CODEX_MARKETPLACE_JSON") as fh:
    codex_marketplace = json.load(fh)
if codex_marketplace.get("name") != "nawwwal-dex":
    raise SystemExit("Codex marketplace name must be nawwwal-dex")

expected_plugins = {"core", "design", "dev", "tools"}
seen_plugins = set()
for entry in codex_marketplace.get("plugins", []):
    name = entry.get("name")
    seen_plugins.add(name)
    source = entry.get("source", {})
    if name in expected_plugins:
        expected_path = f"./plugins/{name}"
        if source.get("source") != "git-subdir":
            raise SystemExit(f"Codex marketplace {name} must use git-subdir")
        if source.get("url") != "https://github.com/nawwwal/dex.git":
            raise SystemExit(f"Codex marketplace {name} must point at nawwwal/dex")
        if source.get("path") != expected_path:
            raise SystemExit(f"Codex marketplace {name} path must be {expected_path}")
        if source.get("ref") != "main":
            raise SystemExit(f"Codex marketplace {name} must track main")

missing = expected_plugins - seen_plugins
if missing:
    raise SystemExit(f"Codex marketplace missing plugins: {', '.join(sorted(missing))}")
PY
```

### 5. Commit, tag, and push

```bash
git add \
  "$CLAUDE_PLUGIN_JSON" \
  "$CODEX_PLUGIN_JSON" \
  "$CLAUDE_MARKETPLACE_JSON" \
  "$CODEX_MARKETPLACE_JSON"

if git diff --cached --quiet; then
  if [ "$BUMP" = "initial" ]; then
    echo "No version bump for initial release; tagging current HEAD"
  else
    echo "ERROR: No version files changed"
    exit 1
  fi
else
  git commit -m "release($PLUGIN): v$NEW_VERSION"
fi

git tag "$TAG"
git push origin HEAD
git push origin "$TAG"
```

### 6. Create the GitHub Release

Use GitHub Releases as the changelog surface, not tags alone.

First, get the previous tag to scope the commit range:

```bash
PREV_TAG=$(git tag --sort=-version:refname | grep "^$PLUGIN-v" | grep -v "^$TAG$" | head -1)
if [ -n "$PREV_TAG" ]; then
  COMMIT_RANGE="$PREV_TAG..HEAD"
else
  COMMIT_RANGE="HEAD"
fi
```

Before writing the release notes, read the commits in that range and synthesize them into user-facing bullets. Do not paste raw commit messages — rewrite them as what changed for the user.

```bash
git log --oneline "$COMMIT_RANGE"
```

Group changes into:
- **New** — new skills or commands added
- **Changed** — behavior changes, routing changes, renames
- **Removed** — deleted skills, files, memory artifacts
- **Fixed** — bug fixes
- **Migration** — required user action; include this only for `major` releases

Omit groups with no entries. Omit internal-only changes (version bumps, lint, formatting) unless they affect behavior.

For `major` releases, the release notes must include a **Migration** section with the exact user action. If there is no migration step, downgrade to `minor`.

Then create the release:

```bash
NOTES_FILE=$(mktemp)
cat > "$NOTES_FILE" <<NOTES
## What's new

<!-- write synthesized bullets here before running gh -->

## Versioning
- Claude plugin manifest: \`plugins/$PLUGIN/.claude-plugin/plugin.json\`
- Codex plugin manifest: \`plugins/$PLUGIN/.codex-plugin/plugin.json\`
NOTES

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
