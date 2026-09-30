from src.tools.format_prd import format_prd


def test_format_prd_creates_expected_sections():
    result = format_prd(
        problem="Users cannot preview changes before publishing.",
        user_stories=[
            "As a user, I want to preview my changes before publishing.",
            "As a user, I want to return to editing from the preview.",
        ],
        acceptance_criteria=[
            "Preview displays unpublished changes.",
            "User can return to editing without losing changes.",
        ],
    )

    assert "# Product Requirements Document" in result
    assert "## Problem Statement" in result
    assert "## User Stories" in result
    assert "## Acceptance Criteria" in result
    assert "Users cannot preview changes before publishing." in result
    assert "Preview displays unpublished changes." in result
