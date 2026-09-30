def format_prd(
    problem: str,
    user_stories: list[str],
    acceptance_criteria: list[str],
) -> str:
    """Format PRD components into a Markdown document."""

    user_story_section = "\n".join(
        f"- {story}" for story in user_stories
    )

    acceptance_section = "\n".join(
        f"- {criterion}" for criterion in acceptance_criteria
    )

    return f"""# Product Requirements Document

## Problem Statement

{problem}

## User Stories

{user_story_section}

## Acceptance Criteria

{acceptance_section}
"""
