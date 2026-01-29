#!/usr/bin/env python3
"""
Telemetry Mapper for Unicorn Dynamics

Maps operational metrics to b9/p9/j9 architecture layers and AUTOGNOSIS levels.
Provides integration between Grove planning artifacts and system telemetry.
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum


class ArchitectureLayer(Enum):
    B9 = "b9"  # Form Triad - Rooted trees (structure/sensory) - T7, T4, T1
    P9 = "p9"  # Void Triad - Membrane pools (process/motor) - T2, T5, T8
    J9 = "j9"  # Pole Triad - Resonant echoes/ESN (association/relational) - T3, T6, T9


class AutognosisLevel(Enum):
    EMISSION = 0     # Raw telemetry signals
    PATTERNS = 1     # Recognized patterns
    SELF_IMAGE = 2   # System self-model
    OPTIMIZATION = 3 # Improvement recommendations


class Triad(Enum):
    FORM = "Form"      # Structure/Sensory - b9 rooted trees
    VOID = "Void"      # Process/Motor - p9 membrane pools  
    POLE = "Pole"      # Association/Relational - j9 resonant echoes (ESN)


@dataclass
class TelemetryMetric:
    name: str
    layer: ArchitectureLayer
    triad: Triad
    autognosis_level: AutognosisLevel
    t_codes: List[str]
    description: str
    unit: str
    thresholds: Dict[str, float]


# Standard telemetry metrics for Unicorn Dynamics
METRICS = {
    # b9 Layer - Form Triad (Rooted Trees: T7, T4, T1)
    "connection_latency": TelemetryMetric(
        "Connection Latency", ArchitectureLayer.B9, Triad.FORM,
        AutognosisLevel.EMISSION, ["T1"],
        "Time to establish localhost terminal connections", "ms",
        {"warning": 100, "critical": 500}
    ),
    "edge_throughput": TelemetryMetric(
        "Edge Throughput", ArchitectureLayer.B9, Triad.FORM,
        AutognosisLevel.EMISSION, ["T1"],
        "Data transfer rate across connection edges", "MB/s",
        {"warning": 10, "critical": 1}
    ),
    "terminal_sessions": TelemetryMetric(
        "Terminal Sessions", ArchitectureLayer.B9, Triad.FORM,
        AutognosisLevel.PATTERNS, ["T4", "T7"],
        "Active localhost terminal session count", "count",
        {"warning": 100, "critical": 200}
    ),
    
    # p9 Layer - Void Triad (Membrane Pools: T2, T5, T8)
    "membrane_utilization": TelemetryMetric(
        "Membrane Utilization", ArchitectureLayer.P9, Triad.VOID,
        AutognosisLevel.OPTIMIZATION, ["T2", "T5", "T8"],
        "Percentage of execution membrane capacity in use", "%",
        {"warning": 80, "critical": 95}
    ),
    "thread_pool_depth": TelemetryMetric(
        "Thread Pool Depth", ArchitectureLayer.P9, Triad.VOID,
        AutognosisLevel.OPTIMIZATION, ["T2", "T5"],
        "Globalhost thread pool queue depth", "count",
        {"warning": 50, "critical": 100}
    ),
    "scope_nesting": TelemetryMetric(
        "Scope Nesting Level", ArchitectureLayer.P9, Triad.VOID,
        AutognosisLevel.OPTIMIZATION, ["T5", "T8"],
        "Current P-system nested scope depth", "level",
        {"warning": 8, "critical": 12}
    ),
    "memory_allocation": TelemetryMetric(
        "Memory Allocation", ArchitectureLayer.B9, Triad.FORM,
        AutognosisLevel.PATTERNS, ["T7"],
        "Memory allocated as quantized technique", "GB",
        {"warning": 12, "critical": 15}
    ),
    
    # j9 Layer - Pole Triad (Resonant Echoes/ESN: T3, T6, T9)
    "gradient_entropy": TelemetryMetric(
        "Gradient Entropy", ArchitectureLayer.J9, Triad.POLE,
        AutognosisLevel.SELF_IMAGE, ["T3", "T6"],
        "Distribution uniformity across ESN reservoir topology", "bits",
        {"warning": 2.5, "critical": 1.5}
    ),
    "topology_coverage": TelemetryMetric(
        "Topology Coverage", ArchitectureLayer.J9, Triad.POLE,
        AutognosisLevel.SELF_IMAGE, ["T6", "T9"],
        "Percentage of ESN nodes actively participating", "%",
        {"warning": 70, "critical": 50}
    ),
    "resonance_coherence": TelemetryMetric(
        "Resonance Coherence", ArchitectureLayer.J9, Triad.POLE,
        AutognosisLevel.SELF_IMAGE, ["T3", "T6", "T9"],
        "Echo state network reservoir coherence", "ratio",
        {"warning": 0.7, "critical": 0.5}
    ),
    
    # Cross-layer metrics
    "system_coherence": TelemetryMetric(
        "System Coherence", ArchitectureLayer.J9, Triad.POLE,
        AutognosisLevel.SELF_IMAGE, ["T9"],
        "Overall system integration via AAR core", "score",
        {"warning": 0.7, "critical": 0.5}
    ),
    "renewal_cycle_time": TelemetryMetric(
        "Renewal Cycle Time", ArchitectureLayer.J9, Triad.POLE,
        AutognosisLevel.SELF_IMAGE, ["T9"],
        "Time to complete full T-system renewal cycle", "seconds",
        {"warning": 300, "critical": 600}
    ),
}


@dataclass
class TelemetryReading:
    metric_key: str
    value: float
    timestamp: str
    status: str  # normal, warning, critical


def evaluate_metric(metric_key: str, value: float) -> str:
    """Evaluate metric value against thresholds."""
    if metric_key not in METRICS:
        return "unknown"
    
    metric = METRICS[metric_key]
    thresholds = metric.thresholds
    
    # Handle metrics where lower is worse
    if metric_key in ["edge_throughput", "topology_coverage", "resonance_coherence", 
                      "system_coherence", "gradient_entropy"]:
        if value <= thresholds["critical"]:
            return "critical"
        elif value <= thresholds["warning"]:
            return "warning"
        return "normal"
    
    # Handle metrics where higher is worse
    if value >= thresholds["critical"]:
        return "critical"
    elif value >= thresholds["warning"]:
        return "warning"
    return "normal"


def map_to_grove_guides(layer: ArchitectureLayer) -> List[str]:
    """Map architecture layer (triad) to recommended Grove Guides."""
    mapping = {
        # b9 Form Triad - Structure/Sensory guides
        ArchitectureLayer.B9: ["Context Map", "Graphic History", "SPOT Matrix"],
        # p9 Void Triad - Process/Motor guides  
        ArchitectureLayer.P9: ["Graphic Gameplan", "Graphic Roadmap", "Five Bold Steps"],
        # j9 Pole Triad - Association/Relational guides
        ArchitectureLayer.J9: ["Stakeholder Map", "Value Proposition", "Journey Vision"],
    }
    return mapping.get(layer, [])


def generate_telemetry_report(readings: List[TelemetryReading]) -> dict:
    """Generate a comprehensive telemetry report."""
    report = {
        "summary": {
            "total_metrics": len(readings),
            "normal": 0,
            "warning": 0,
            "critical": 0,
        },
        "by_layer": {
            "b9": {"metrics": [], "status": "normal"},
            "p9": {"metrics": [], "status": "normal"},
            "j9": {"metrics": [], "status": "normal"},
        },
        "by_autognosis_level": {
            "0_emission": [],
            "1_patterns": [],
            "2_self_image": [],
            "3_optimization": [],
        },
        "recommendations": [],
    }
    
    for reading in readings:
        if reading.metric_key not in METRICS:
            continue
        
        metric = METRICS[reading.metric_key]
        status = evaluate_metric(reading.metric_key, reading.value)
        
        # Update summary counts
        report["summary"][status] += 1
        
        # Add to layer grouping
        layer_key = metric.layer.value
        report["by_layer"][layer_key]["metrics"].append({
            "name": metric.name,
            "value": reading.value,
            "unit": metric.unit,
            "status": status,
            "t_codes": metric.t_codes,
        })
        
        # Update layer status (worst status wins)
        if status == "critical":
            report["by_layer"][layer_key]["status"] = "critical"
        elif status == "warning" and report["by_layer"][layer_key]["status"] != "critical":
            report["by_layer"][layer_key]["status"] = "warning"
        
        # Add to autognosis level grouping
        level_key = f"{metric.autognosis_level.value}_{metric.autognosis_level.name.lower()}"
        report["by_autognosis_level"][level_key].append({
            "name": metric.name,
            "value": reading.value,
            "status": status,
        })
        
        # Generate recommendations for issues
        if status in ["warning", "critical"]:
            guides = map_to_grove_guides(metric.layer)
            report["recommendations"].append({
                "metric": metric.name,
                "status": status,
                "layer": layer_key,
                "triad": metric.triad.value,
                "suggested_guides": guides,
                "t_codes": metric.t_codes,
            })
    
    return report


def format_report_markdown(report: dict) -> str:
    """Format telemetry report as Markdown."""
    lines = [
        "# Unicorn Dynamics Telemetry Report",
        "",
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| Normal | {report['summary']['normal']} |",
        f"| Warning | {report['summary']['warning']} |",
        f"| Critical | {report['summary']['critical']} |",
        "",
        "---",
        "",
        "## Layer Status",
        "",
    ]
    
    for layer_key, layer_data in report["by_layer"].items():
        status_emoji = {"normal": "🟢", "warning": "🟡", "critical": "🔴"}[layer_data["status"]]
        layer_names = {"b9": "b9 Form (Rooted Trees)", "p9": "p9 Void (Membrane Pools)", "j9": "j9 Pole (Resonant Echoes)"}
        
        lines.append(f"### {status_emoji} {layer_names[layer_key]}")
        lines.append("")
        
        if layer_data["metrics"]:
            lines.append("| Metric | Value | Status | T-Codes |")
            lines.append("|--------|-------|--------|---------|")
            for m in layer_data["metrics"]:
                lines.append(f"| {m['name']} | {m['value']} {m['unit']} | {m['status']} | {', '.join(m['t_codes'])} |")
        else:
            lines.append("*No metrics reported*")
        lines.append("")
    
    if report["recommendations"]:
        lines.append("---")
        lines.append("")
        lines.append("## Recommendations")
        lines.append("")
        
        for rec in report["recommendations"]:
            lines.append(f"### {rec['metric']} ({rec['status'].upper()})")
            lines.append(f"- **Layer:** {rec['layer']} | **Triad:** {rec['triad']}")
            lines.append(f"- **T-Codes:** {', '.join(rec['t_codes'])}")
            lines.append(f"- **Suggested Grove Guides:** {', '.join(rec['suggested_guides'])}")
            lines.append("")
    
    return "\n".join(lines)


def main():
    # Example usage with sample readings
    sample_readings = [
        TelemetryReading("connection_latency", 45, "2026-01-29T10:00:00Z", "normal"),
        TelemetryReading("edge_throughput", 25, "2026-01-29T10:00:00Z", "normal"),
        TelemetryReading("membrane_utilization", 85, "2026-01-29T10:00:00Z", "warning"),
        TelemetryReading("thread_pool_depth", 35, "2026-01-29T10:00:00Z", "normal"),
        TelemetryReading("gradient_entropy", 3.2, "2026-01-29T10:00:00Z", "normal"),
        TelemetryReading("topology_coverage", 65, "2026-01-29T10:00:00Z", "warning"),
        TelemetryReading("system_coherence", 0.82, "2026-01-29T10:00:00Z", "normal"),
    ]
    
    report = generate_telemetry_report(sample_readings)
    markdown = format_report_markdown(report)
    
    print(markdown)
    print("\n---\n")
    print("JSON Report:")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
