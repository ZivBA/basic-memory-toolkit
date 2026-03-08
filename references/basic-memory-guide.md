# Basic Memory Guide for AI Assistants

<system>
  <type>Local-first knowledge management system</type>
  <storage>Markdown files with semantic markup</storage>
  <features>Real-time sync, multi-project organization, knowledge graph, WikiLinks</features>
</system>

<session_startup>
  <step_1>Run list_projects() at conversation start</step_1>
  <step_2>Ask user: "Which project should I use for this session?"</step_2>
  <step_3>All operations use project="selected-project" parameter</step_3>
  <step_4>User can switch mid-session: "switch to [project]"</step_4>
</session_startup>

<detailed_rules>
  <location>memory-rules project</location>
  <purpose>Authoritative source for all memory management rules</purpose>
  <when_to_consult>Before creating/editing notes, search memory-rules for relevant guidelines</when_to_consult>
  <categories>
    <anti_patterns>Self-referential relations, cross-project WikiLinks, generic titles</anti_patterns>
    <creating_notes>Relation rules, new note checklist, title standards</creating_notes>
    <organizing>Consolidation criteria, archive protocols, folder patterns</organizing>
    <quality>Observation standards, pre-publish checklist</quality>
    <updating>Edit vs rewrite, relation verification</updating>
  </categories>
</detailed_rules>

<projects>
  <location>/home/zivben/basic-memory-projects/</location>
  <default>main</default>

  <main>
    <purpose>Cross-cutting knowledge, project directory</purpose>
    <use_when>Unclear which project, truly cross-cutting topics</use_when>
  </main>

  <memory_rules>
    <purpose>Authoritative memory management rules</purpose>
    <use_when>Before any note creation/editing for rule lookup</use_when>
  </memory_rules>

  <phone_refactor>
    <purpose>AnalyticJson PhoneEnhanced mapper refactoring</purpose>
    <use_when>Phone mapper, AnalyticJson, PhoneEnhanced work</use_when>
  </phone_refactor>

  <edifact_pipeline>
    <purpose>EDIFACT processing (Split → Parse → Insert)</purpose>
    <use_when>EdifactSplit, Parser-Edifact, Json-Insertion work</use_when>
  </edifact_pipeline>

  <infrastructure>
    <purpose>Cross-project Docker, CI/CD, testing</purpose>
    <use_when>Deployment, Docker patterns, cross-service testing</use_when>
  </infrastructure>

  <development_practices>
    <purpose>General coding patterns, best practices</purpose>
    <use_when>Programming patterns, coding standards</use_when>
  </development_practices>

  <etl_packages>
    <purpose>ETL package ecosystem — extraction guides, architecture, package notes, CI/CD</purpose>
    <use_when>ETL package extraction, etl-contracts, etl-harness, package scaffolding, Cloud Build for packages</use_when>
  </etl_packages>

  <bootstrap_framework>
    <purpose>Project scaffolding and code generation</purpose>
    <use_when>Creating microservices from templates</use_when>
  </bootstrap_framework>
</projects>

<critical_rule>Projects point to markdown directories, NOT code repositories</critical_rule>

<mcp_tools>
  <write_note>
    <params>title, content, folder, tags, project</params>
    <behavior>Same title+folder overwrites existing</behavior>
  </write_note>

  <read_note>
    <params>identifier, project</params>
    <identifiers>title, folder/title, permalink</identifiers>
  </read_note>

  <search_notes>
    <params>query, project, search_type</params>
    <critical>Always specify project parameter</critical>
  </search_notes>

  <edit_note>
    <params>identifier, operation, content, project</params>
    <operations>append, prepend, find_replace, replace_section</operations>
    <warning>Requires EXACT identifier</warning>
  </edit_note>

  <move_note>
    <params>identifier, destination_path, project</params>
    <warning>Requires EXACT identifier</warning>
  </move_note>

  <list_projects>
    <use>Session startup</use>
  </list_projects>

  <recent_activity>
    <params>timeframe, depth, project</params>
    <timeframe>"7d", "yesterday", "last week"</timeframe>
  </recent_activity>

  <build_context>
    <params>url, depth, project</params>
    <use>Follow knowledge graph connections</use>
  </build_context>
</mcp_tools>

<memory_urls>
  <format_1>memory://title</format_1>
  <format_2>memory://folder/title</format_2>
  <format_3>memory://permalink</format_3>
  <format_4>memory://project-name/folder/title (cross-project, unambiguous)</format_4>
  <cross_project_examples>
    memory://main/docs/authentication
    memory://edifact-pipeline/pipeline-integration/EDIFACT PNR Processing Pipeline
  </cross_project_examples>
</memory_urls>

<semantic_markup>
  <observations>
    <format>- [category] Description #tag</format>
    <categories>decision, requirement, technique, issue, fact, idea, question, preference, best-practice</categories>
  </observations>

  <relations>
    <format>- relation_type [[Target Entity]]</format>
    <types>implements, requires, part_of, extends, contrasts_with, inspired_by, relates_to</types>
  </relations>

  <wikilinks>
    <format>[[Exact Title]]</format>
    <same_project_only>WikiLinks don't cross project boundaries</same_project_only>
    <cross_project>Use text: "Note Title" (project-name)</cross_project>
  </wikilinks>

  <forward_references>
    <allowed>Yes - auto-resolve when target created</allowed>
  </forward_references>
</semantic_markup>

<recording_protocol>
  <when>Decisions, conclusions, important information, technical insights</when>
  <workflow>
    <step_1>Identify valuable information</step_1>
    <step_2>Ask: "Would you like me to record this?"</step_2>
    <step_3>If agreed, use write_note() with semantic markup</step_3>
    <step_4>Confirm: "I've saved to Basic Memory"</step_4>
  </workflow>
  <dont>Avoid trivial or duplicate information</dont>
</recording_protocol>

<note_requirements>
  <title>Specific, searchable (not generic)</title>
  <observations>3-5 with specific categories</observations>
  <relations>2-3 minimum</relations>
  <tags>3-5 relevant tags</tags>
  <see_rules>memory-rules/creating-notes/ for detailed checklists</see_rules>
</note_requirements>

<critical_anti_patterns>
  <self_referential>NEVER create relations where target = current note</self_referential>
  <cross_project_wikilinks>Use text format for cross-project refs</cross_project_wikilinks>
  <generic_titles>Avoid "Notes", "Discussion", "Ideas"</generic_titles>
  <see_rules>memory-rules/anti-patterns/ for details and fixes</see_rules>
</critical_anti_patterns>

<troubleshooting>
  <cant_find_note>
    <solution_1>Use search_notes() with broader terms</solution_1>
    <solution_2>Check different project</solution_2>
  </cant_find_note>

  <edit_fails>
    <cause>Requires EXACT identifier</cause>
    <solution>search_notes() first to get exact title</solution>
  </edit_fails>

  <unresolved_wikilinks>
    <explanation>Forward refs auto-resolve when target created</explanation>
  </unresolved_wikilinks>

  <cross_project_issues>
    <limitation>Moving notes between projects not supported</limitation>
    <workaround>Create new note in target project</workaround>
  </cross_project_issues>
</troubleshooting>

<key_principles>
  <principle_1>Projects = markdown directories, not code repos</principle_1>
  <principle_2>Search before creating to avoid duplicates</principle_2>
  <principle_3>Ask permission before recording</principle_3>
  <principle_4>Use exact identifiers for edit/move</principle_4>
  <principle_5>Build rich connections (graph density)</principle_5>
  <principle_6>Consult memory-rules before note operations</principle_6>
</key_principles>

<version>Basic Memory v0.15.0+ | Four-tier architecture 2025-11-27</version>
