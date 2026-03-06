---
title: Folder Structure Patterns
type: note
permalink: organizing/folder-structure-patterns
tags:
- organizing
- folders
- structure
- consistency
---

# Folder Structure Patterns

## Core Principle

**Consistent folder structure across projects.** Use standard folders for predictable organization.

## Standard Folders

| Folder | Purpose | Examples |
|--------|---------|----------|
| `sessions/` | Work session summaries | Session 2025-11-23 - Topic |
| `procedures/` | Step-by-step guides | Deployment Procedure |
| `testing/` | Test strategies, results | Integration Testing Framework |
| `technical/` | Implementation details | Error Handling Implementation |
| `issues/` | Problems, bugs, troubleshooting | ODBC Driver Configuration Issue |
| `insights/` | Lessons learned, discoveries | Memory System Architecture Plan |
| `architecture/` | System design, patterns | Message Reprocessability Architecture |
| `archive/` | Historical content | archive/phase-1-planning/ |

## Organization Strategies

### Type-Based (Simple Projects)
```
project/
├── sessions/
├── procedures/
├── testing/
├── issues/
└── archive/
```

Best for: Small projects, cross-cutting knowledge bases

### Service-Based (Multi-Component Projects)
```
project/
├── service-a/
│   ├── testing/
│   ├── issues/
│   └── error-handling/
├── service-b/
│   └── ...
├── shared/
│   ├── sessions/
│   ├── procedures/
│   └── insights/
└── archive/
```

Best for: Pipeline projects, microservices, multi-component systems

## Choosing a Strategy

| Project Type | Recommended Strategy |
|--------------|---------------------|
| General knowledge | Type-based |
| Single service | Type-based |
| Multi-service pipeline | Service-based |
| Cross-cutting practices | Type-based |

## Folder Naming

- Use lowercase with hyphens: `error-handling/`
- Be descriptive: `multi-format-testing/` not `testing-2/`
- Group related content: `compression-strategies/`

## Observations

- [requirement] Use consistent folder structure across projects
- [technique] Choose type-based or service-based based on project complexity
- [best-practice] Use lowercase hyphenated folder names

## Relations

- part_of [[Archive Protocols]]
- enables [[Knowledge Graph Optimization]]

#organizing #folders #structure #consistency
