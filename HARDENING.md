<!-- markdownlint-disable -->

# Hardening Report: shundor--python-bandit-scan/v1.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **shundor--python-bandit-scan/v1.0** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) is violated in the 'Run Bandit scan' step. Env vars that come from inputs are expanded without double quotes: `UPPERCASE_LEVEL=$(echo $INPUT_LEVEL | tr a-z A-Z)`, `UPPERCASE_CONFIDENCE=$(echo $INPUT_CONFIDENCE | tr a-z A-Z)`, and `bandit -f sarif -o results.sarif -r $INPUT_PATH $LEVEL $CONFIDENCE $EXCLUDED_PATHS $EXIT_ZERO $SKIPS $INI_PATH`. In that last line, $EXCLUDED_PATHS, $SKIPS and $INI_PATH hold the untrusted values of inputs.excluded_paths, inputs.skips and inputs.ini_path. Because none of these are quoted, the shell splits them into separate words and expands glob characters in them.

Locations:

- `action.yml:50`
- `action.yml:66`
- `action.yml:105`

### unpinned-uses (severity: high)

These composite steps use mutable refs instead of 40-character commit SHAs: `uses: actions/upload-artifact@main` and `uses: github/codeql-action/upload-sarif@v2`.

Locations:

- `action.yml:116`
- `action.yml:122`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses

**Notes:**

Both findings are fixed in action.yml. Nothing was run or tested, so neither change has been checked against a real Bandit scan.

**Script injection (the 'Run Bandit scan' step):**
- The level and confidence inputs are now passed as quoted values (`printf '%s' "$VAR"`) before being uppercased, and the `case` statements test quoted variables.
- The bandit command is now built from a bash array. `-x`, `-s` and `--ini` each go in as a separate argument, followed by their quoted value. `excluded_paths` and `skips` are comma-separated, so each stays one argument, as before.
- `inputs.path` used to be expanded unquoted, so it could name several targets. It is still split on whitespace (`read -r -d '' -a`), so several targets still work. Glob characters in it are no longer expanded.

**Unpinned actions:**
- `actions/upload-artifact@main` is now pinned to `cf430e030ddbb5b0abf93d22962f4752f3646cd9 # main`.
- `github/codeql-action/upload-sarif@v2` is now pinned to `b8d3b6e8af63cde30bdc382c0bc28114f4346c88 # v2`.

### Iteration 2

**Fixes applied:** unpinned-uses

**Notes:**

Pinned actions/upload-artifact@main to cf430e030ddbb5b0abf93d22962f4752f3646cd9 (# main). I also fixed some garbled text in action.yml. The bandit script was missing the 'esac' that closes the LEVEL case and had 'inNFIDENCE in' on the CONFIDENCE case line, so bash could not parse it. The upload-sarif reference read 'github/codupload-sarif@... # v2ad-sarif@v2'; I restored it to github/codeql-action/upload-sarif@b8d3b6e8af63cde30bdc382c0bc28114f4346c88 # v2. A lookup confirmed that SHA is the v2 commit.

