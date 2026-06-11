---
description: Automatically update versions in all configuration files and create git tags.
---

# Workflow: /bumpversion

The process of automatically upgrading versions and creating tags for projects.

## Steps

1. **Get input**: Determine the new version number to update (format `x.y.z` ).
2. **Run Script**: Run python script to synchronize:
   ```bash
   python .agent/scripts/bump_version.py <version>
   ```
3. **Commit & Tag**:
   - `git add .`
   - `git commit -m "chore(release): bump version to <version>"`
   - `git push origin main`
   - `git tag v<version>`
   - `git push origin v<version>`
