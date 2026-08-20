---
description: Update versions in project configuration files and prepare an approved release.
---

# Workflow: /bumpversion

1. Validate the requested `x.y.z` version.
2. Run the repository's version synchronization script in its required runtime.
3. Review the resulting diff and run the release verification suite.
4. Commit and tag only after verification passes.
5. Push the branch and tag only when the user explicitly requests publishing.
