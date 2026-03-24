#!/bin/bash

echo "=== YouTube Research Skill - Verification ==="
echo ""

SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SKILL_DIR"

ERRORS=0

# Test 1: Python version
echo "Test 1: Python version"
if python3 --version &> /dev/null; then
    echo "  ✓ Python 3: $(python3 --version)"
else
    echo "  ❌ Python 3 not found"
    ERRORS=$((ERRORS + 1))
fi

# Test 2: yt-dlp
echo ""
echo "Test 2: yt-dlp installation"
if command -v yt-dlp &> /dev/null; then
    echo "  ✓ yt-dlp: $(yt-dlp --version)"
else
    echo "  ❌ yt-dlp not found"
    echo "     Install: pip3 install -U yt-dlp"
    ERRORS=$((ERRORS + 1))
fi

# Test 3: Node.js or Deno
echo ""
echo "Test 3: Node.js/Deno (required by yt-dlp)"
if command -v node &> /dev/null; then
    echo "  ✓ Node.js: $(node --version)"
elif command -v deno &> /dev/null; then
    echo "  ✓ Deno: $(deno --version | head -1)"
else
    echo "  ❌ Neither Node.js nor Deno found"
    echo "     Install: brew install node OR brew install deno"
    ERRORS=$((ERRORS + 1))
fi

# Test 4: Python imports
echo ""
echo "Test 4: Python dependencies"
if python3 -c "import notebooklm, bs4, readability, html2text, requests" 2>/dev/null; then
    echo "  ✓ All Python packages installed"
else
    echo "  ❌ Missing Python packages"
    echo "     Install: pip3 install -r scripts/requirements.txt"
    ERRORS=$((ERRORS + 1))
fi

# Test 5: NotebookLM CLI
echo ""
echo "Test 5: NotebookLM CLI"
if command -v notebooklm &> /dev/null; then
    echo "  ✓ NotebookLM CLI installed"

    # Check if authenticated (this is tricky to test non-interactively)
    echo "  ℹ️  NotebookLM auth status: Run 'notebooklm login' if needed"
else
    echo "  ❌ NotebookLM CLI not found"
    echo "     Should be installed with notebooklm-py package"
    ERRORS=$((ERRORS + 1))
fi

# Test 6: Utilities module
echo ""
echo "Test 6: Utils module"
if python3 -c "import sys; sys.path.insert(0, 'scripts'); from utils import generate_slug; assert generate_slug('API Design') == 'api-design'" 2>/dev/null; then
    echo "  ✓ Utils module working"
else
    echo "  ❌ Utils module test failed"
    ERRORS=$((ERRORS + 1))
fi

# Test 7: YouTube search (quick test with 1 result)
echo ""
echo "Test 7: YouTube search (this may take 10-20 seconds...)"
if python3 scripts/search_youtube.py "python tutorial" /tmp/yt_verify_test.json --max-results 1 2>/dev/null; then
    if [ -f /tmp/yt_verify_test.json ]; then
        VIDEO_COUNT=$(python3 -c "import json; data=json.load(open('/tmp/yt_verify_test.json')); print(data.get('total_found', 0))" 2>/dev/null)
        if [ "$VIDEO_COUNT" -gt 0 ]; then
            echo "  ✓ YouTube search working (found $VIDEO_COUNT video)"
        else
            echo "  ⚠️  YouTube search ran but found no videos with transcripts"
            echo "     (This is OK - some videos lack transcripts)"
        fi
        rm -f /tmp/yt_verify_test.json
    else
        echo "  ❌ YouTube search did not create output file"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  ❌ YouTube search failed"
    echo "     Check: yt-dlp --version"
    echo "     Check: node --version OR deno --version"
    ERRORS=$((ERRORS + 1))
fi

# Test 8: Vault directory
echo ""
echo "Test 8: Vault directory"
if [ -d "$HOME/.claude/work/deep-research" ]; then
    echo "  ✓ Vault directory exists"
else
    echo "  ❌ Vault directory not found"
    echo "     Create: mkdir -p '$HOME/.claude/work/deep-research'"
    ERRORS=$((ERRORS + 1))
fi

# Summary
echo ""
echo "==================================="
if [ $ERRORS -eq 0 ]; then
    echo "✓ All tests passed!"
    echo ""
    echo "The YouTube Research skill is ready to use."
    echo ""
    echo "Try it:"
    echo "  Ask Claude Code: 'Research API design best practices'"
    exit 0
else
    echo "❌ $ERRORS test(s) failed"
    echo ""
    echo "Fix the errors above, then run ./verify.sh again"
    exit 1
fi
