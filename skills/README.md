# AI Agent Skills

Collection of reusable, high-signal patterns for consistent AI agent behavior across this project and future work.

## How to Use Skills

When starting a conversation with an AI agent:

1. **Reference a specific skill**: "Apply the npm-dependency-security-hardening SKILL"
2. **Or mention context**: "I'm working on Node.js dependencies" (agent should recognize and apply)
3. **Or include in instructions**: Paste the relevant SKILL file into the conversation

## Active Skills

### [npm-dependency-security-hardening](npm-dependency-security-hardening.md)
- **Purpose**: Manage Node.js/npm dependency vulnerabilities systematically
- **Scope**: Node.js projects (JavaScript, TypeScript, Electron, etc.)
- **Activation**: When working with `npm install`, dependencies, or security
- **Version**: 1.0
- **Last Updated**: March 1, 2026
- **Status**: Ready for use

**Quick Start**: 
```bash
npm audit
npm audit fix
npm test && npm run build && npm run lint
npm audit
```

### [agentic-pattern-recognition](agentic-pattern-recognition.md)
- **Purpose**: Teach agentic patterns by recognizing and explaining them during development
- **Scope**: All development work
- **Activation**: Always active (user is learning agentic coding)
- **Version**: 1.0
- **Last Updated**: March 1, 2026
- **Status**: Always on

---

## Planned Skills

- **python-dependency-security** - Python/pip equivalent (Planned)
- **git-workflow-standards** - Branch, commit, PR practices (Planned)
- **code-quality-gates** - Linting, formatting, type checking (Planned)
- **test-coverage-standards** - Unit/integration test best practices (Planned)

---

## Adding New Skills

To add a new SKILL to this folder:

1. Create a new markdown file: `skills/my-new-skill.md`
2. Follow the structure of existing skills (metadata, activation trigger, decision tree, validation)
3. Add an entry to this README under "Active Skills"
4. Include example/history at the bottom of the SKILL file

**SKILL Template** (minimal):
```markdown
# SKILL: [Skill Name]

**VERSION**: 1.0  
**APPLIES TO**: [Scope]  
**DOES NOT APPLY TO**: [Out of scope]

### Activation Trigger
When the user mentions: [keywords/context]

### Decision Tree
[Flowchart or step-by-step logic]

### Validation
[How to verify the SKILL worked]

### Implementation History
[Real examples from actual use]
```

---

## Notes

- SKILLs are descriptive of best practices, not prescriptive of all work
- Apply pragmatically: If a SKILL doesn't fit the situation, note why
- Update SKILLs when you learn better approaches
- Version bump (0.1 → 0.2) for minor updates, (1.0 → 2.0) for major changes
