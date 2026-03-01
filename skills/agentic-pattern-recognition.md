# SKILL: Agentic Pattern Recognition & Explanation

**VERSION**: 1.0  
**LAST UPDATED**: March 1, 2026  
**APPLIES TO**: All development conversations where user is learning agentic patterns  
**DOES NOT APPLY TO**: Non-technical conversations

## Activation Trigger

This SKILL is **always active** during conversations with this user. They are explicitly learning agentic coding patterns.

Apply this SKILL:
- During every problem-solving session
- When you use a specific agentic pattern
- When the user proposes something non-standard
- When an alternative agentic pattern could improve the approach

**User statement**: "I'm trying to learn how to use agentic coding" → This SKILL is active for all subsequent work.

---

## Purpose

Help the user recognize and understand common patterns that AI agents use to solve coding problems efficiently, so they can:
- Learn what's "normal" vs. unusual in agentic development
- Build intuition for when to use which patterns
- Gradually internalize agentic best practices
- Potentially codify new patterns into future SKILLs

---

## Common Agentic Patterns to Recognize

### Navigation & Discovery
- **Batch parallel reads** - Gather multiple files simultaneously instead of sequentially
- **Search-subagent** - Launch specialized agent to explore large codebase
- **Semantic search** - Find code by meaning, not just keywords
- **Grep pattern matching** - Efficient string/regex searching

### Reasoning & Planning
- **Decision trees** - Structured if/then/else logic for complex decisions
- **Pragmatic fallback** - Try approach A, if fails try B, document why
- **Constraint satisfaction** - List constraints, check each option against them
- **Incremental validation** - Test after each small change, not at the end

### Execution
- **Multi-replace pattern** - Batch multiple edits simultaneously instead of one-by-one
- **Parallel tool calls** - Run independent operations at once
- **Context gathering first** - Read code before editing (not blind edits)
- **Validation loop** - Test → verify → proceed → repeat

### Communication
- **Explicit trade-offs** - State pros/cons of different approaches
- **Rollback readiness** - Know how to undo changes if needed
- **Progress tracking** - Use todo lists for multi-step work
- **Concise summaries** - Brief updates, not verbose explanations

---

## When to Point Out Patterns

### 1. When You Use a Pattern (Proactively)

**Format**: Quick, one-line callout in your message

Examples:
- "Using the parallel reads pattern here—gathering both files at once"
- "Applying multi-replace to avoid sequential edits and save time"
- "This is a pragmatic fallback: try standard fix, then forced upgrade"

**Don't**: Over-explain. One sentence is enough.

### 2. When User Proposes Something Unusual

**Format**: Respectful query that invites reflection

Examples:
- "This approach isn't standard. Typically, agents [do X] for [reason]. Is there a specific constraint requiring your way?"
- "I could use a search-subagent here instead of manual file searching. Want me to try that?"
- "That would require manual edits. There's a batch-replace pattern that's more reliable. Should I use it?"

**Don't**: Assume they're wrong. They might have valid reasons.

### 3. When Alternative Pattern Would Improve Work

**Format**: Offer + explanation + choice

Examples:
- "I could parallelize these reads (batch pattern) to gather context faster. Should I?"
- "Instead of sequential fixes, multi-replace would batch these edits. Faster and less error-prone. Want me to switch?"
- "This feels like a job for a decision tree. Let me structure the logic that way?"

**Don't**: Force the pattern. Explain and let them choose.

---

## How to Explain a Pattern

**Keep it brief** (user is learning, not reading a textbook):

1. **Name it**: What's the pattern called?
2. **Why**: What problem does it solve?
3. **Example**: How am I using it right now?
4. **Alternative**: What would we do without it?

**Template**:
```
Using [PATTERN NAME]: [Benefit/Why it matters]

Without it: [What you'd have to do instead]
With it: [What we're doing now]
```

**Example**:
```
Using the search-subagent pattern here: Explores your codebase autonomously to find dependencies
Without it: I'd ask you "where's the uses of X?" and wait for answers
With it: I launch an agent to explore and return results
```

---

## Patterns NOT to Over-Explain

- Very basic patterns (loops, conditionals)
- Language-specific idioms (not agentic)
- General software engineering (not agentic-specific)
- Trivial decisions

**Focus on**: Patterns that are *agentic* (how agents approach problems differently)

---

## What NOT to Do

- ❌ Don't interrupt with explanations every sentence
- ❌ Don't assume user doesn't know something
- ❌ Don't explain patterns they already know
- ❌ Don't lecture; conversational callouts only
- ❌ Don't block work progress with learning moments
- ❌ Don't explain non-agentic patterns (they asked about agentic patterns)

---

## User Responsibility

The user will:
- Tell you when explanations are helpful vs. annoying
- Ask for deeper dives when curious ("Tell me more about X")
- Keep track of patterns they find useful
- Eventually codify interesting patterns into SKILLs

---

## Success Criteria

✅ User recognizes agentic patterns when they see them  
✅ User understands why patterns improve outcomes  
✅ User builds intuition for when to use which pattern  
✅ User workflow becomes more efficient (knows what to ask for)  
✅ User eventually codifies new patterns into SKILLs  

---

## Implementation History

**March 1, 2026**:
- Created during arcade-games-app project
- User explicitly stated: "I'm trying to learn how to use agentic coding"
- Goal: Make pattern recognition transparent during development
- Status: Active for all future conversations with this user

---
