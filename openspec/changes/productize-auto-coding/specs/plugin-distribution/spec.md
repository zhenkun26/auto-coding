## Purpose

Defines how the auto-coding skill set is packaged and distributed as an installable Codex plugin with a marketplace entry, versioning, and changelog.

## ADDED Requirements

### Requirement: Plugin manifest
The repository SHALL contain a `.codex-plugin/plugin.json` declaring the plugin id, name, version, and the skills it bundles, so Codex can install it.

#### Scenario: Manifest is valid
- **WHEN** the plugin manifest is validated against the Codex plugin schema
- **THEN** it declares a stable plugin id (`auto-coding`), a human-readable name, a semantic version, and a non-empty skills list

### Requirement: Marketplace entry
The repository SHALL provide a marketplace entry that references the plugin manifest, allowing one-command installation.

#### Scenario: User installs from marketplace
- **WHEN** a user runs the documented marketplace install command
- **THEN** the plugin and its bundled skills are installed into the user's Codex environment

### Requirement: Versioned releases
The repository SHALL maintain a `CHANGELOG.md` and use semantic versioning so users can track changes across releases.

#### Scenario: Version is bumped
- **WHEN** a release is cut
- **THEN** the plugin manifest version and the CHANGELOG top entry describe the same semantic version

### Requirement: Installation documentation
The README SHALL document how to install, update, and uninstall the plugin, including the marketplace source URL.

#### Scenario: User follows installation steps
- **WHEN** a user follows the installation section of the README
- **THEN** they can install, update, and uninstall the plugin without inspecting the plugin internals
