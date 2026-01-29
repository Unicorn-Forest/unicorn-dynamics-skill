#!/usr/bin/env python3
"""
Session Planner for Unicorn Dynamics Strategic Visioning

Generates session agendas based on objectives, team size, and available time.
Maps Grove Graphic Guides to planning phases and T-System transformations.
"""

import json
import sys
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Guide:
    name: str
    type: str  # Structure or Process
    dimension: str  # Performance, Potential, Commitment
    duration_minutes: int
    t_codes: List[str]
    description: str

# Grove Graphic Guides library
GUIDES = {
    "meeting_startup_river": Guide(
        "Meeting Startup - River Rafting", "Process", "General", 30,
        ["T1"], "Establish OARRs using river navigation metaphor"
    ),
    "meeting_startup_treasure": Guide(
        "Meeting Startup - Treasure Map", "Process", "General", 30,
        ["T1"], "Establish OARRs using journey to treasure metaphor"
    ),
    "context_map": Guide(
        "Context Map", "Structure", "Performance", 60,
        ["T1", "T8"], "Scan external environment, identify trends and issues"
    ),
    "spot_matrix": Guide(
        "SPOT Matrix", "Process", "Commitment", 45,
        ["T4"], "Assess Strengths, Problems, Opportunities, Threats"
    ),
    "cover_story_vision": Guide(
        "Cover Story Vision", "Process", "Commitment", 60,
        ["T2", "T3"], "Create future-state story from magazine cover perspective"
    ),
    "five_bold_steps": Guide(
        "Five Bold Steps", "Process", "Commitment", 45,
        ["T4", "T5"], "Define specific strategic initiatives toward vision"
    ),
    "graphic_gameplan": Guide(
        "Graphic Gameplan", "Process", "Commitment", 60,
        ["T5", "T6"], "Create whole-systems action plan"
    ),
    "graphic_roadmap": Guide(
        "Graphic Roadmap", "Process", "Commitment", 60,
        ["T5", "T7"], "Document milestones and commitments"
    ),
    "journey_vision": Guide(
        "Journey Vision", "Process", "Potential", 60,
        ["T2", "T9"], "Map past, present, future trajectory"
    ),
    "mandala_vision": Guide(
        "Mandala Vision", "Structure", "Potential", 45,
        ["T2", "T3"], "Cluster vision themes into unified whole"
    ),
    "stakeholder_map": Guide(
        "Stakeholder Map", "Structure", "Potential", 45,
        ["T1", "T6"], "Identify and map key relationships"
    ),
    "value_proposition": Guide(
        "Value Proposition", "Structure", "Potential", 60,
        ["T3", "T7"], "Clarify offer, connection, and infrastructure"
    ),
    "investment_portfolio": Guide(
        "Investment Portfolio", "Structure", "Potential", 45,
        ["T7", "T8"], "Allocate resources across Sow/Grow/Plow/Harvest"
    ),
    "industry_structure_map": Guide(
        "Industry Structure Map", "Structure", "Commitment", 60,
        ["T1", "T4"], "Analyze value chain and competitive landscape"
    ),
    "graphic_history": Guide(
        "Graphic History", "Structure", "Performance", 45,
        ["T7", "T9"], "Harvest lessons from organizational evolution"
    ),
}

# Planning cycle phases
CYCLES = {
    "current_environment": {
        "name": "Current Environment Analysis",
        "guides": ["context_map", "graphic_history", "spot_matrix", "industry_structure_map"],
        "t_codes": ["T1", "T4", "T7", "T8"],
        "description": "Understand where we are now"
    },
    "future_planning": {
        "name": "Future Planning",
        "guides": ["cover_story_vision", "mandala_vision", "journey_vision", "stakeholder_map"],
        "t_codes": ["T2", "T3", "T6", "T9"],
        "description": "Envision where we want to be"
    },
    "action_planning": {
        "name": "Action Planning",
        "guides": ["five_bold_steps", "value_proposition", "graphic_gameplan", "graphic_roadmap"],
        "t_codes": ["T4", "T5", "T6", "T7"],
        "description": "Plan how to get there"
    }
}


def generate_session_agenda(
    objective: str,
    duration_hours: float,
    team_size: int,
    focus_cycle: Optional[str] = None,
    include_startup: bool = True
) -> dict:
    """Generate a session agenda based on parameters."""
    
    available_minutes = int(duration_hours * 60)
    agenda = {
        "objective": objective,
        "duration_hours": duration_hours,
        "team_size": team_size,
        "sessions": [],
        "total_minutes": 0,
        "t_system_coverage": set()
    }
    
    # Add meeting startup if requested
    if include_startup:
        startup = GUIDES["meeting_startup_river" if team_size > 8 else "meeting_startup_treasure"]
        agenda["sessions"].append({
            "name": startup.name,
            "duration": startup.duration_minutes,
            "type": startup.type,
            "dimension": startup.dimension,
            "t_codes": startup.t_codes,
            "description": startup.description
        })
        agenda["total_minutes"] += startup.duration_minutes
        agenda["t_system_coverage"].update(startup.t_codes)
    
    # Select guides based on focus cycle or full strategic session
    if focus_cycle and focus_cycle in CYCLES:
        cycles_to_include = [focus_cycle]
    else:
        cycles_to_include = ["current_environment", "future_planning", "action_planning"]
    
    for cycle_key in cycles_to_include:
        cycle = CYCLES[cycle_key]
        
        # Add break before each major phase
        if agenda["total_minutes"] > 0:
            agenda["sessions"].append({
                "name": "Break",
                "duration": 15,
                "type": "Break",
                "dimension": "-",
                "t_codes": [],
                "description": "Refresh and transition"
            })
            agenda["total_minutes"] += 15
        
        # Add cycle header
        agenda["sessions"].append({
            "name": f"Phase: {cycle['name']}",
            "duration": 0,
            "type": "Phase",
            "dimension": "-",
            "t_codes": cycle["t_codes"],
            "description": cycle["description"]
        })
        
        # Add guides for this cycle
        for guide_key in cycle["guides"]:
            if agenda["total_minutes"] + GUIDES[guide_key].duration_minutes > available_minutes:
                break
            
            guide = GUIDES[guide_key]
            agenda["sessions"].append({
                "name": guide.name,
                "duration": guide.duration_minutes,
                "type": guide.type,
                "dimension": guide.dimension,
                "t_codes": guide.t_codes,
                "description": guide.description
            })
            agenda["total_minutes"] += guide.duration_minutes
            agenda["t_system_coverage"].update(guide.t_codes)
    
    # Convert set to sorted list for JSON serialization
    agenda["t_system_coverage"] = sorted(list(agenda["t_system_coverage"]))
    
    return agenda


def format_agenda_markdown(agenda: dict) -> str:
    """Format agenda as Markdown."""
    lines = [
        f"# Strategic Visioning Session Agenda",
        f"",
        f"**Objective:** {agenda['objective']}",
        f"**Duration:** {agenda['duration_hours']} hours ({agenda['total_minutes']} minutes planned)",
        f"**Team Size:** {agenda['team_size']} participants",
        f"**T-System Coverage:** {', '.join(agenda['t_system_coverage'])}",
        f"",
        f"---",
        f"",
    ]
    
    current_time = 0
    for session in agenda["sessions"]:
        if session["type"] == "Phase":
            lines.append(f"## {session['name']}")
            lines.append(f"*{session['description']}*")
            lines.append("")
        elif session["type"] == "Break":
            lines.append(f"### [{current_time//60}:{current_time%60:02d}] Break (15 min)")
            lines.append("")
            current_time += session["duration"]
        else:
            t_codes = ", ".join(session["t_codes"]) if session["t_codes"] else "-"
            lines.append(f"### [{current_time//60}:{current_time%60:02d}] {session['name']} ({session['duration']} min)")
            lines.append(f"- **Type:** {session['type']} | **Dimension:** {session['dimension']} | **T-Codes:** {t_codes}")
            lines.append(f"- {session['description']}")
            lines.append("")
            current_time += session["duration"]
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python session-planner.py <objective> [duration_hours] [team_size] [focus_cycle]")
        print("")
        print("Arguments:")
        print("  objective      - Session objective (required)")
        print("  duration_hours - Available time in hours (default: 4)")
        print("  team_size      - Number of participants (default: 10)")
        print("  focus_cycle    - Optional: current_environment, future_planning, or action_planning")
        print("")
        print("Example:")
        print("  python session-planner.py 'Annual strategic planning' 8 15")
        print("  python session-planner.py 'Vision refresh' 4 8 future_planning")
        sys.exit(1)
    
    objective = sys.argv[1]
    duration_hours = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    team_size = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    focus_cycle = sys.argv[4] if len(sys.argv) > 4 else None
    
    agenda = generate_session_agenda(objective, duration_hours, team_size, focus_cycle)
    markdown = format_agenda_markdown(agenda)
    
    print(markdown)


if __name__ == "__main__":
    main()
