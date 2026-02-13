# Mobile Design Skill

This skill provides comprehensive mobile-first design guidance for iOS and Android applications.

## Installation

1. Copy the `mobile-design` folder to your workspace under `.kiro/skills/`
2. Restart Kiro IDE
3. The skill will automatically activate when you work on mobile projects

## Quick Start

When working on mobile development, ask yourself:

```
🧠 CHECKPOINT:

Platform:   [ iOS / Android / Both ]
Framework:  [ React Native / Flutter / SwiftUI / Kotlin ]
Files Read: [ List the skill files you've read ]

3 Principles I Will Apply:
1. _______________
2. _______________
3. _______________

Anti-Patterns I Will Avoid:
1. _______________
2. _______________
```

## Usage

This skill automatically activates when your requests contain keywords like:
- "mobile app"
- "ios app" 
- "android app"
- "react native"
- "flutter"
- "mobile design"
- "mobile ux"

## Files Structure

```
mobile-design/
├── SKILL.md                    # Main skill file
├── agentskills.json           # Kiro compatibility metadata
├── scripts/
│   └── mobile_audit.py       # Mobile UX audit script
├── references/                # Documentation files
│   ├── mobile-design-thinking.md
│   ├── touch-psychology.md
│   ├── mobile-performance.md
│   ├── platform-ios.md
│   ├── platform-android.md
│   └── ...
└── assets/                    # Templates and resources
```

## Runtime Scripts

Use the mobile audit script to validate your mobile UX:

```bash
python scripts/mobile_audit.py <project_path>
```

## License

MIT License - feel free to share and modify for your projects.