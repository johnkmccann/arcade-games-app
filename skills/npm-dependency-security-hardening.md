# SKILL: npm Dependency Security Hardening

**VERSION**: 1.0  
**LAST UPDATED**: March 1, 2026  
**APPLIES TO**: Node.js/npm projects (JavaScript, TypeScript)  
**DOES NOT APPLY TO**: Python, Rust, Go, Ruby, or other ecosystems

## Activation Trigger

Apply this SKILL when the user mentions or context includes:
- "npm install"
- "dependencies"
- "vulnerabilities"
- "security"
- "npm audit"
- Any work on Node.js projects requiring dependency management

**If the user says**: "Apply the npm security SKILL" → Do not ask for confirmation, apply immediately.

---

**Goal**: Ensure production and development npm dependencies are secure and maintainable.

## Decision Tree

```
Run: npm audit
    ↓
CRITICAL vulnerability found?
├─ YES → MUST FIX (blocking, required before proceeding)
│   ├─ Try: npm audit fix
│   ├─ If fails → Upgrade affected package to latest version
│   └─ If still fails → STOP and report blocker
│
└─ NO → Continue to HIGH
    ↓
    HIGH severity vulnerability found?
    ├─ YES → MUST FIX (non-negotiable)
    │   ├─ Try: npm audit fix
    │   ├─ If fails → Upgrade affected package
    │   └─ If still fails → STOP and report blocker
    │
    └─ NO → Continue to MODERATE
        ↓
        MODERATE severity vulnerability found?
        ├─ YES → ATTEMPT FIX (pragmatic approach)
        │   ├─ Can fix with simple version upgrade? → DO IT
        │   ├─ Can remove unused dependency? → DO IT
        │   ├─ Requires complex refactoring? → SKIP (don't fix)
        │   ├─ Dev-only dependency? → May ACCEPT unsolved
        │   └─ After any fix → Run full validation suite
        │
        └─ NO → Continue to LOW
            ↓
            LOW severity vulnerability found?
            ├─ YES → Ignore (unless fixing moderate/high)
            └─ NO → DONE - Zero vulnerabilities
```

## When to Apply

- After running `npm install`
- When adding new dependencies
- After any `package.json` modification
- When user explicitly requests vulnerability fixes
- Before committing to main branch (CI/CD check)

## Approach (Detailed Steps)

**Step 1: Audit Current State**
   - Run `npm audit` to identify all vulnerabilities
   - Categorize by severity (critical > high > moderate > low)
   - Document the baseline counts

**Step 2: Apply Decision Tree**
   - For critical/high: Use decision tree above (non-negotiable)
   - For moderate: Use pragmatic judgment (upgrade if simple)

**Step 3: Implement Fixes**
   - Simple: `npm audit fix` (safe, automatic)
   - Version upgrade: Update `package.json` version constraint and `npm install`
   - Remove: Delete unused dependency from `package.json` and `npm install`
   - Force fix: `npm audit fix --force` only after validating tests pass

**Step 4: Full Validation**
   - `npm test` - All tests must pass
   - `npm run build` - Build must succeed
   - `npm run lint` - No new linting errors
   - `npm audit` - Verify improvements

**Step 5: Confirm & Commit**
   - If vulnerabilities reduced: Commit the changes
   - If stuck: Document why in this SKILL and inform user
   - Success message includes before/after counts

## What NOT to Do

- ❌ Do NOT make complex structural changes to fix moderate vulnerabilities
- ❌ Do NOT remove core dependencies to hide vulnerabilities
- ❌ Do NOT skip testing after version upgrades
- ❌ Do NOT accept unresolved critical/high vulnerabilities
- ❌ Do NOT modify code architecture unless absolutely necessary
- ❌ Do NOT use `--force` flag without running full test suite afterward
- ❌ Do NOT ignore vulnerabilities in production dependencies

## Success Criteria

✅ Zero critical vulnerabilities  
✅ Zero high severity vulnerabilities  
✅ Moderate vulnerabilities minimized (ideally zero, acceptable if dev-only)  
✅ All tests passing  
✅ Build completes successfully  
✅ No new linting errors introduced  
✅ Vulnerability count improved from baseline

## Example Workflow

```bash
# 1. Audit
npm audit

# 2. Fix (automatic)
npm audit fix

# 3. Validate
npm test
npm run build
npm run lint

# 4. Confirm
npm audit

# 5. Report results
# "Vulnerabilities reduced from 11 to 0. All tests pass. Ready to commit."
```

---

## Implementation History

**March 1, 2026**: 
- **Project**: arcade-games-app (frontend)
- **Baseline**: 11 vulnerabilities (1 moderate from @typescript-eslint, 6 high, 4 moderate from vitest)
- **Actions**: Upgraded @typescript-eslint v6→v8, Vitest v1→v2→v4, removed unused @vitest/ui
- **Result**: Zero vulnerabilities, all tests pass, build succeeds, no code changes required
- **Note**: Dashboard feature (UI) preserved through careful version selection
- **Time**: Approximately 20 minutes with testing and validation

---
