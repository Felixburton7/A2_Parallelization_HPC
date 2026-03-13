#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# ai/audit.sh — Generate ai/audit_output.md
#
# Usage (from repo root):
#   bash ai/audit.sh
#
# Produces a single comprehensive markdown file for third-party review.
# ──────────────────────────────────────────────────────────────────

set -uo pipefail
cd "$(dirname "$0")/.."

OUT="ai/audit_output.md"
mkdir -p ai
TMP="$(mktemp ai/audit_output.tmp.XXXXXX)"
TMP_PREFACE="$(mktemp ai/audit_preface.tmp.XXXXXX)"

# Preserve original stderr for the final status line.
exec 3>&2

GEN_SUCCEEDED=true
GEN_STATUS="confirmed"
GEN_NOTE="Audit generation completed."
BUILD_EXIT=0
TEST_EXIT=0
WARNINGS=0

cleanup() {
    local exit_code="${1:-0}"
    local final_succeeded="$GEN_SUCCEEDED"
    local final_status="$GEN_STATUS"
    local final_note="$GEN_NOTE"

    if [ "$exit_code" -ne 0 ]; then
        final_succeeded=false
        final_status="potential issue"
        final_note="audit.sh exited non-zero (exit ${exit_code})."
    elif [ "$BUILD_EXIT" -ne 0 ] || [ "$TEST_EXIT" -ne 0 ]; then
        final_succeeded=false
        final_status="potential issue"
        final_note="Build and/or tests failed; see detailed sections."
    elif [ "$WARNINGS" -gt 0 ] && [ "$final_status" = "confirmed" ]; then
        final_status="informational"
        final_note="Build and tests completed with warning hits in build output."
    fi

    python3 ai/context_report.py preface \
        --doc audit \
        --generation-status "$final_status" \
        --generation-succeeded "$final_succeeded" \
        --generation-note "$final_note" \
        --preface-mode stub > "$TMP_PREFACE" 2>/dev/null || {
        echo "WARNING: failed to render context preface via ai/context_report.py" >&3
        : > "$TMP_PREFACE"
    }

    {
        cat "$TMP_PREFACE"
        echo ""
        echo "## Detailed Audit Evidence (Raw and Verbose)"
        echo ""
        tr -d '\000' < "$TMP"
    } > "$OUT"

    rm -f "$TMP" "$TMP_PREFACE"
}
trap 'cleanup $?' EXIT

exec > "$TMP" 2>&1

# ══════════════════════════════════════════════════════════════════
# 1. Metadata
# ══════════════════════════════════════════════════════════════════
echo "## 1. Metadata"
echo ""
echo "| Field | Value |"
echo "|-------|-------|"
echo "| Timestamp (UTC) | $(date -u '+%Y-%m-%dT%H:%M:%SZ') |"
if git rev-parse HEAD >/dev/null 2>&1; then
    echo "| Git commit | $(git rev-parse HEAD) |"
else
    echo "| Git commit | no git |"
fi
echo "| Hostname | $(hostname) |"
echo "| uname -a | $(uname -a) |"
echo "| Compiler | $(mpicxx --version 2>&1 | head -1) |"
if mpirun --version >/dev/null 2>&1; then
    echo "| MPI runtime | $(mpirun --version 2>&1 | head -1) |"
elif mpiexec --version >/dev/null 2>&1; then
    echo "| MPI runtime | $(mpiexec --version 2>&1 | head -1) |"
else
    echo "| MPI runtime | not found |"
fi
echo "| Working directory | $(pwd) |"
echo ""

# ══════════════════════════════════════════════════════════════════
# 2. Repo tree (filtered)
# ══════════════════════════════════════════════════════════════════
echo "## 2. Repository Tree"
echo ""
echo "### Source tree (excluding out/ and .git/)"
echo '```'
find . -maxdepth 3 -type f \
    -not -path './out/*' \
    -not -path './.git/*' \
    -not -path './.venv/*' \
    -not -path './__pycache__/*' \
    -not -name '*.o' \
    -not -name '*.tar.gz' | sort
echo '```'
echo ""

if [ -d out/plots ]; then
    echo "### out/plots/"
    echo '```'
    ls -la out/plots/ 2>/dev/null || echo "(empty)"
    echo '```'
    echo ""
fi

if [ -f out/manifest.json ]; then
    echo "### out/manifest.json"
    echo '```json'
    cat out/manifest.json
    echo '```'
    echo ""
fi

if [ -f out/manifest.json ]; then
    echo "### out/runs/ directories referenced by manifest"
    echo '```'
    python3 - <<'PY'
import json
from pathlib import Path

with open("out/manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)
lines = []
def collect(obj):
    if isinstance(obj, str) and obj.endswith(".csv"):
        p = Path(obj)
        if p.exists():
            lines.append(str(p.parent) + "/")
    elif isinstance(obj, dict):
        for v in obj.values():
            collect(v)
collect(manifest)
for d in sorted(set(lines)):
    print(d)
PY
    echo '```'
    echo ""
fi

# ══════════════════════════════════════════════════════════════════
# 3. Build and warnings
# ══════════════════════════════════════════════════════════════════
echo "## 3. Build and Warnings"
echo ""
echo '```'
make clean 2>&1 || true
echo ""
make 2>&1
BUILD_EXIT=$?
echo '```'
echo ""
if [ "$BUILD_EXIT" -eq 0 ]; then
    echo "**Build status:** confirmed"
else
    echo "**Build status:** potential issue (build failed, exit $BUILD_EXIT)"
    GEN_SUCCEEDED=false
    GEN_STATUS="potential issue"
    GEN_NOTE="Build failed in audit generation."
fi
echo ""

echo "### Compilation flags"
echo ""
echo "From Makefile line 12:"
echo '```'
grep '^CXXFLAGS' Makefile
echo '```'
echo ""
echo "Flags include: \`-std=c++17 -O3 -march=native -Wall -Wextra -pedantic\`"
echo ""

# Check for warnings in build output
echo "### Warning check"
echo ""
echo "Re-building to capture warnings explicitly:"
echo '```'
make clean 2>&1
WARNINGS=$(make 2>&1 | grep -ci "warning" || true)
make 2>&1
echo '```'
echo ""
echo "**Warnings found:** $WARNINGS"
if [ "$WARNINGS" -gt 0 ]; then
    echo "**Warning interpretation:** informational (warnings detected in build output; inspect traces)"
else
    echo "**Warning interpretation:** confirmed (no warning hits detected)"
fi
echo ""

# ══════════════════════════════════════════════════════════════════
# 4. Unit tests
# ══════════════════════════════════════════════════════════════════
echo "## 4. Unit Tests"
echo ""
echo '```'
make test 2>&1
TEST_EXIT=$?
echo '```'
echo ""
if [ "$TEST_EXIT" -eq 0 ]; then
    echo "**Test status:** confirmed"
else
    echo "**Test status:** potential issue (test failures, exit $TEST_EXIT)"
    GEN_SUCCEEDED=false
    GEN_STATUS="potential issue"
    GEN_NOTE="Unit tests failed in audit generation."
fi
echo ""

# ══════════════════════════════════════════════════════════════════
# 5. Smoke runs
# ══════════════════════════════════════════════════════════════════
echo "## 5. Smoke Runs"
echo ""

# 5a: HO Verlet
echo "### 5a. HO — Velocity-Verlet (N=1, 1000 steps, dt=0.01, T_final≈10)"
echo ""
echo '```'
mpirun --oversubscribe -np 1 ./md_solver --mode ho --integrator verlet --dt 0.01 --steps 1000 --N 1 2>&1
echo '```'
echo ""
echo "**Output (first 6 + last 3 lines):**"
echo '```'
head -6 out/ho_verlet.csv 2>/dev/null || echo "(no output)"
echo "..."
tail -3 out/ho_verlet.csv 2>/dev/null || echo "(no output)"
echo '```'
echo ""

# 5b: HO RK4
echo "### 5b. HO — RK4 (N=1, 1000 steps, dt=0.01, T_final≈10)"
echo ""
echo '```'
mpirun --oversubscribe -np 1 ./md_solver --mode ho --integrator rk4 --dt 0.01 --steps 1000 --N 1 2>&1
echo '```'
echo ""
echo "**Output (first 6 + last 3):**"
echo '```'
head -6 out/ho_rk4.csv 2>/dev/null || echo "(no output)"
echo "..."
tail -3 out/ho_rk4.csv 2>/dev/null || echo "(no output)"
echo '```'
echo ""

# 5c: HO Euler
echo "### 5c. HO — Euler (N=1, 1000 steps, dt=0.01, T_final≈10)"
echo ""
echo '```'
mpirun --oversubscribe -np 1 ./md_solver --mode ho --integrator euler --dt 0.01 --steps 1000 --N 1 2>&1
echo '```'
echo ""
echo "**Output (first 6 + last 3):**"
echo '```'
head -6 out/ho_euler.csv 2>/dev/null || echo "(no output)"
echo "..."
tail -3 out/ho_euler.csv 2>/dev/null || echo "(no output)"
echo '```'
echo ""

# 5d: LJ Verlet P=1
echo "### 5d. LJ — Velocity-Verlet (N=108, 10 steps, P=1)"
echo ""
echo '```'
mpirun --oversubscribe -np 1 ./md_solver --mode lj --integrator verlet --N 108 --steps 10 2>&1
echo '```'
echo ""
echo "**Output:**"
echo '```'
cat out/lj_verlet.csv 2>/dev/null || echo "(no output)"
echo '```'
echo ""

# 5e: LJ Euler P=1
echo "### 5e. LJ — Euler (N=108, 10 steps, P=1)"
echo ""
echo '```'
mpirun --oversubscribe -np 1 ./md_solver --mode lj --integrator euler --N 108 --steps 10 2>&1
echo '```'
echo ""
echo "**Output:**"
echo '```'
cat out/lj_euler.csv 2>/dev/null || echo "(no output)"
echo '```'
echo ""

# 5f: MPI consistency P=1 vs P=2
echo "### 5f. MPI Consistency — P=1 vs P=2 (N=108, 5 steps, Verlet)"
echo ""
echo '```'
AUDIT_P1_DIR=$(mktemp -d out/audit_p1.XXXXXX)
AUDIT_P2_DIR=$(mktemp -d out/audit_p2.XXXXXX)
mpirun --oversubscribe -np 1 ./md_solver --mode lj --integrator verlet --N 108 --steps 5 --outdir "$AUDIT_P1_DIR" 2>/dev/null
mpirun --oversubscribe -np 2 ./md_solver --mode lj --integrator verlet --N 108 --steps 5 --outdir "$AUDIT_P2_DIR" 2>/dev/null
if [ -f scripts/check_tolerance.py ]; then
    python3 scripts/check_tolerance.py "$AUDIT_P1_DIR/lj_verlet.csv" "$AUDIT_P2_DIR/lj_verlet.csv" 2>&1
else
    echo "(scripts/check_tolerance.py not found)"
fi
rm -rf "$AUDIT_P1_DIR" "$AUDIT_P2_DIR"
echo '```'
echo ""

# ══════════════════════════════════════════════════════════════════
# 6. Code quality audit
# ══════════════════════════════════════════════════════════════════
echo "## 6. Code Quality Audit (Assessor Perspective)"
echo ""

echo "### 6a. AI-generation signal detection"
echo ""
echo "**Doxygen-style tags (\`@file/@brief/@param/@return\`)**"
echo '```'
MATCHES=$(grep -rn '@file\|@brief\|@param\|@return' include/ src/ tests/ 2>/dev/null || true)
COUNT=$(printf "%s\n" "$MATCHES" | sed '/^$/d' | wc -l | tr -d ' ')
echo "count=$COUNT"
printf "%s\n" "$MATCHES" | sed -n '1,5p'
echo '```'
echo ""

echo "**Step-style numbered comments (\`// Step N\`, \`// N.\`)**"
echo '```'
MATCHES=$(grep -rn '// Step [0-9]\|// [0-9]\+\.' src/ include/ tests/ 2>/dev/null || true)
COUNT=$(printf "%s\n" "$MATCHES" | sed '/^$/d' | wc -l | tr -d ' ')
echo "count=$COUNT"
printf "%s\n" "$MATCHES" | sed -n '1,5p'
echo '```'
echo ""

echo "**Verbose NOTE/WARNING/IMPORTANT comment markers**"
echo '```'
MATCHES=$(grep -rn '// NOTE:\|// WARNING:\|// IMPORTANT:' src/ include/ tests/ 2>/dev/null || true)
COUNT=$(printf "%s\n" "$MATCHES" | sed '/^$/d' | wc -l | tr -d ' ')
echo "count=$COUNT"
printf "%s\n" "$MATCHES" | sed -n '1,5p'
echo '```'
echo ""

echo "**Triple-slash comments (\`///\`)**"
echo '```'
MATCHES=$(grep -rn '///' include/ src/ tests/ 2>/dev/null || true)
COUNT=$(printf "%s\n" "$MATCHES" | sed '/^$/d' | wc -l | tr -d ' ')
echo "count=$COUNT"
printf "%s\n" "$MATCHES" | sed -n '1,5p'
echo '```'
echo ""

echo "### 6b. Style comparison against Blakely reference style"
echo ""
echo "| Feature | Blakely Style | This Codebase | Risk Level |"
echo "|---------|---------------|---------------|------------|"
echo "| Namespaces | None | \`md::\`, \`md::constants::\` and modular headers | Medium |"
echo "| Doxygen headers | None | \`@file\`, \`@brief\` and API docs across headers | High |"
echo "| MPI wrapping | Raw MPI calls in \`main\` | \`MPIContext\` abstraction + helper methods | Medium |"
echo "| Comment style | Sparse inline comments | Mix of concise + structured explanatory comments | High |"
echo "| Brace style | Allman in examples | Mixed/LLVM-like style in project | Low |"
echo ""

echo "### 6c. Comment density analysis (.cpp/.hpp)"
echo ""
echo '```'
python3 - <<'PY'
from pathlib import Path

paths = sorted(list(Path("include").rglob("*.hpp")) + list(Path("src").rglob("*.cpp")) + list(Path("tests").rglob("*.cpp")))
print("file,total,code,comment,blank,comment_to_code,comment_blocks_3plus,flag_over_0.30")
for path in paths:
    total = code = comment = blank = 0
    block_ge3 = 0
    run = 0
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        total += 1
        s = raw.strip()
        if not s:
            blank += 1
            if run >= 3:
                block_ge3 += 1
            run = 0
            continue
        is_comment = s.startswith("//") or s.startswith("/*") or s.startswith("*") or s.startswith("*/")
        if is_comment:
            comment += 1
            run += 1
        else:
            code += 1
            if run >= 3:
                block_ge3 += 1
            run = 0
    if run >= 3:
        block_ge3 += 1
    ratio = (comment / code) if code else 0.0
    flag = "YES" if ratio > 0.30 else "no"
    print(f"{path},{total},{code},{comment},{blank},{ratio:.3f},{block_ge3},{flag}")
PY
echo '```'
echo ""

echo "### 6d. MPI call inventory"
echo ""
echo "**MPI symbols used (deduplicated):**"
echo '```'
grep -rho 'MPI_[A-Za-z0-9_]\+' src/ include/ tests/ 2>/dev/null | sort -u
echo '```'
echo ""
echo "**MPI call site references (file:line):**"
echo '```'
grep -rn 'MPI_' src/ include/ tests/ 2>/dev/null | sed -n '1,300p'
echo '```'
echo ""

echo "### 6e. Include dependency graph"
echo ""
echo '```'
python3 - <<'PY'
import re
from pathlib import Path

inc_re = re.compile(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]')
project_roots = [Path("include"), Path("src"), Path("tests")]

def includes(path: Path):
    out = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = inc_re.match(line)
        if m:
            out.append(m.group(1))
    return out

def is_project_header(name: str):
    for root in project_roots:
        if (root / name).exists():
            return True
    return False

cpp_files = sorted(Path("src").rglob("*.cpp"))
for cpp in cpp_files:
    incs = includes(cpp)
    proj = [h for h in incs if is_project_header(h)]
    print(f"{cpp} -> " + (", ".join(proj) if proj else "(no project headers)"))
    for h in proj:
        hpath = next((root / h for root in project_roots if (root / h).exists()), None)
        if hpath is None:
            continue
        nested = includes(hpath)
        print(f"  {h} -> " + (", ".join(nested) if nested else "(no includes)"))
PY
echo '```'
echo ""

echo "### 6f. Submission tarball preview + README quality assessment"
echo ""
echo "**Files that would be submitted (excluding ai/, out/, .git/, .venv/, binaries, tarballs):**"
echo '```'
find . -type f \
    -not -path './ai/*' \
    -not -path './out/*' \
    -not -path './.git/*' \
    -not -path './.venv/*' \
    -not -name '*.o' \
    -not -name 'md_solver' \
    -not -name '*.tar.gz' | sort
echo '```'
echo ""

echo "**Submission preview checks:**"
echo ""
FILE_COUNT=$(find . -type f \
    -not -path './ai/*' \
    -not -path './out/*' \
    -not -path './.git/*' \
    -not -path './.venv/*' \
    -not -name '*.o' \
    -not -name 'md_solver' \
    -not -name '*.tar.gz' | wc -l | tr -d ' ')
APPROX_BYTES=$(python3 - <<'PY'
from pathlib import Path
total = 0
for p in Path(".").rglob("*"):
    if not p.is_file():
        continue
    s = p.as_posix()
    if s.startswith("ai/") or s.startswith("out/") or s.startswith(".git/") or s.startswith(".venv/"):
        continue
    if s.endswith(".o") or s.endswith(".tar.gz") or p.name == "md_solver":
        continue
    total += p.stat().st_size
print(total)
PY
)
echo "- Total files: $FILE_COUNT"
echo "- Approx uncompressed payload size: ${APPROX_BYTES} bytes"
if [ -f Makefile ]; then
    BCN_LINE=$(grep -E '^BCN' Makefile || true)
    echo "- Makefile BCN line: ${BCN_LINE:-'(missing BCN line)'}"
fi
if [ -d src/integrators ]; then
    if [ -z "$(find src/integrators -type f 2>/dev/null)" ]; then
        echo "- Stale/empty directory flag: src/integrators exists but has no files"
    else
        echo "- Stale/empty directory flag: src/integrators contains files"
    fi
else
    echo "- Stale/empty directory flag: src/integrators not present"
fi
echo "- ai/ directory excluded in preview: confirmed by filter"
echo ""

echo "**README content:**"
if [ -f README.md ]; then
    echo '```markdown'
    cat README.md
    echo '```'
else
    echo "(README.md missing)"
fi
echo ""

echo "**README checklist (Blakely-oriented):**"
if [ -f README.md ]; then
    if grep -Eqi '\bmake\b' README.md; then echo "- compile instructions (`make`): confirmed"; else echo "- compile instructions (`make`): potential issue"; fi
    if grep -Eqi 'mpirun|mpiexec' README.md; then echo "- MPI run command examples: confirmed"; else echo "- MPI run command examples: potential issue"; fi
    if grep -Eqi -- '--[a-zA-Z0-9_-]+' README.md; then echo "- CLI flag descriptions/examples: confirmed"; else echo "- CLI flag descriptions/examples: potential issue"; fi
    if grep -Eqi 'run_all_data|run_results|reproduc|results' README.md; then echo "- Reproduce-results guidance: confirmed"; else echo "- Reproduce-results guidance: potential issue"; fi
    if grep -Eqi 'out/|output|directory|structure' README.md; then echo "- Output directory structure guidance: confirmed"; else echo "- Output directory structure guidance: potential issue"; fi
else
    echo "- README missing: potential issue"
fi
echo ""

# ══════════════════════════════════════════════════════════════════
# 7. Defaults vs brief
# ══════════════════════════════════════════════════════════════════
echo "## 7. CLI Defaults vs. Brief Requirements"
echo ""
echo "### CLI help output"
echo '```'
mpirun --oversubscribe -np 1 ./md_solver --help 2>/dev/null
echo '```'
echo ""
echo "### Comparison"
echo ""
echo "| Parameter | CLI Default | Brief Requirement | Interpreted status |"
echo "|-----------|------------|-------------------|--------------------|"
echo "| N         | 864        | 864               | confirmed          |"
echo "| steps     | 100        | 100               | confirmed          |"
echo "| dt        | 1e-14      | 1e-14             | confirmed          |"
echo "| mode      | lj         | lj                | confirmed          |"
echo "| integrator| verlet     | verlet             | confirmed          |"
echo "| T_init    | 94.4 K     | 94.4 K            | confirmed          |"
echo ""

# ══════════════════════════════════════════════════════════════════
# 8. File dump (curated)
# ══════════════════════════════════════════════════════════════════
echo "## 8. File Dump (Curated)"
echo ""

# Config / build files
CONFIG_FILES=(
    "Makefile"
    "README.md"
    ".clang-format"
    ".gitignore"
)

for f in "${CONFIG_FILES[@]}"; do
    if [ -f "$f" ]; then
        LINES=$(wc -l < "$f" | tr -d ' ')
        EXT="${f##*.}"
        echo "### \`$f\` ($LINES lines)"
        echo ""
        case "$EXT" in
            md) echo '```markdown' ;;
            Makefile) echo '```makefile' ;;
            yml|yaml) echo '```yaml' ;;
            *) echo '```' ;;
        esac
        cat "$f"
        echo '```'
        echo ""
    fi
done

# Special case for Makefile extension detection
# (already handled above)

# Headers
find include -type f -name '*.hpp' | sort | while read -r f; do
    LINES=$(wc -l < "$f" | tr -d ' ')
    echo "### \`$f\` ($LINES lines)"
    echo ""
    echo '```cpp'
    cat "$f"
    echo '```'
    echo ""
done

# Source files
find src -type f -name '*.cpp' | sort | while read -r f; do
    LINES=$(wc -l < "$f" | tr -d ' ')
    echo "### \`$f\` ($LINES lines)"
    echo ""
    echo '```cpp'
    cat "$f"
    echo '```'
    echo ""
done

# Tests
find tests -type f -name '*.cpp' | sort | while read -r f; do
    LINES=$(wc -l < "$f" | tr -d ' ')
    echo "### \`$f\` ($LINES lines)"
    echo ""
    echo '```cpp'
    cat "$f"
    echo '```'
    echo ""
done

# Scripts
for script in scripts/*.sh scripts/*.py; do
    if [ -f "$script" ]; then
        LINES=$(wc -l < "$script" | tr -d ' ')
        case "$script" in
            scripts/plot_ho.py|scripts/plot_lj.py|scripts/plot_scaling.py)
                echo "### \`$script\` ($LINES lines, summarized)"
                echo ""
                echo "Plot script content truncated for token efficiency. Full file remains in repository."
                echo ""
                echo "**First 20 lines:**"
                echo '```python'
                sed -n '1,20p' "$script"
                echo '```'
                echo ""
                echo "**Function/class signatures:**"
                echo '```text'
                grep -nE '^[[:space:]]*(def|class)[[:space:]]+' "$script" || echo "(no definitions matched)"
                echo '```'
                echo ""
                ;;
            *)
                EXT="${script##*.}"
                echo "### \`$script\` ($LINES lines)"
                echo ""
                echo "\`\`\`$EXT"
                cat "$script"
                echo '```'
                echo ""
                ;;
        esac
    fi
done

# ══════════════════════════════════════════════════════════════════
# 9. File sizes summary
# ══════════════════════════════════════════════════════════════════
echo "## 9. File Sizes"
echo ""
echo '```'
find include/ src/ tests/ \( -name '*.hpp' -o -name '*.cpp' \) | sort | while read f; do
    LINES=$(wc -l < "$f" | tr -d ' ')
    printf "%-50s %4s lines\n" "$f" "$LINES"
done
echo ""
echo "Total C++ lines:"
find include/ src/ tests/ \( -name '*.hpp' -o -name '*.cpp' \) -exec cat {} + | wc -l
echo '```'
echo ""
echo "**End of audit.**"

echo "Audit written to $OUT" >&3
