#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const path = require("node:path");

const repoRoot = path.resolve(__dirname, "..");
const cliArgs = process.argv.slice(2);

const pythonCandidates = process.env.PYTHON
  ? [[process.env.PYTHON, []]]
  : [
      ["python", []],
      ["python3", []],
      ["py", ["-3"]],
    ];

const env = {
  ...process.env,
  PYTHONPATH: process.env.PYTHONPATH
    ? `${repoRoot}${path.delimiter}${process.env.PYTHONPATH}`
    : repoRoot,
  BRO_SKILLS_INSTALL_METHOD: "npm",
};

for (const [command, prefixArgs] of pythonCandidates) {
  const result = spawnSync(command, [...prefixArgs, "-m", "bro_skills", ...cliArgs], {
    cwd: process.cwd(),
    env,
    stdio: "inherit",
  });

  if (result.error && result.error.code === "ENOENT") {
    continue;
  }

  if (result.error) {
    console.error(`bro-skills: failed to start ${command}: ${result.error.message}`);
    process.exit(1);
  }

  process.exit(result.status ?? 0);
}

console.error("bro-skills: Python 3.9+ is required. Install Python or set the PYTHON environment variable.");
process.exit(1);
