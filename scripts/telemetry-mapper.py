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
    B9 = "b9"  # Connection Edges - localhost terminal patterns
    P9 = "p9"  # Execution Membranes - globalhost thread pools
    J9 = "j9"  # Distribution Gradients - orgalhost topology


class AutognosisLevel(Enum):
    EMISSION = 0     # Raw telemetry signals
    PATTERNS = 1     # Recognized patterns
    SELF_IMAGE = 2   # System self-model
    OPTIMIZATION = 3 # Improvement recommendations


class Dimension(Enum):
    M = "Performance"  # Execution, output, response
    G = "Potential"    # Ideas, resources, memory
    C = "Commitment"   # Work, feedback, integration


@dataclass
class TelemetryMetric:
    name: str
    layer: ArchitectureLayer
    dimension: Dimension
    autognosis_level: AutognosisLevel
    t_codes: List[str]
    description: str
    unit: str
    thresholds: Dict[str, float]


# Standard telemetry metrics for Unicorn Dynamics
METRICS = {
    # b9 Layer - Connection Edges
    "connection_latency": TelemetryMetric(
        "Connection Latency", ArchitectureLayer.B9, Dimension.M,
        AutognosisLevel.EMISSION, ["T1", "T8"],
        "Time to establish localhost terminal connections", "ms",
        {"warning": 100, "critical": 500}
    ),
    "edge_throughput": TelemetryMetric(
        "Edge Throughput", ArchitectureLayer.B9, Dimension.M,
        AutognosisLevel.EMISSION, ["T1"],
        "Data transfer rate across connection edges", "MB/s",
        {"warning": 10, "critical": 1}
    ),
    "terminal_sessions": TelemetryMetric(
        "Terminal Sessions", ArchitectureLayer.B9, Dimension.M,
        AutognosisLevel.PATTERNS, ["T8"],
        "Active localhost terminal session count", "count",
        {"warning": 100, "critical": 200}
    ),
    
    # p9 Layer - Execution Membranes
    "membrane_utilization": TelemetryMetric(
        "Membrane Utilization", ArchitectureLayer.P9, Dimension.G,
        AutognosisLevel.PATTERNS, ["T2", "T7"],
        "Percentage of execution membrane capacity in use", "%",
        {"warning": 80, "critical": 95}
    ),
    "thread_pool_depth": TelemetryMetric(
        "Thread Pool Depth", ArchitectureLayer.P9, Dimension.G,
        AutognosisLevel.PATTERNS, ["T2"],
        "Globalhost thread pool queue depth", "count",
        {"warning": 50, "critical": 100}
    ),
    "scope_nesting": TelemetryMetric(
        "Scope Nesting Level", ArchitectureLayer.P9, Dimension.G,
        AutognosisLevel.SELF_IMAGE, ["T3", "T6"],
        "Current P-system nested scope depth", "level",
        {"warning": 8, "critical": 12}
    ),
    "memory_allocation": TelemetryMetric(
        "Memory Allocation", ArchitectureLayer.P9, Dimension.G,
        AutognosisLevel.EMISSION, ["T7"],
        "Memory allocated to execution membranes", "GB",
        {"warning": 12, "critical": 15}
    ),
    
    # j9 Layer - Distribution Gradients
    "gradient_entropy": TelemetryMetric(
        "Gradient Entropy", ArchitectureLayer.J9, Dimension.C,
        AutognosisLevel.SELF_IMAGE, ["T3", "T6"],
        "Distribution uniformity across orgalhost topology", "bits",
        {"warning": 2.5, "critical": 1.5}
    ),
    "topology_coverage": TelemetryMetric(
        "Topology Coverage", ArchitectureLayer.J9, Dimension.C,
        AutognosisLevel.PATTERNS, ["T4", "T5"],
        "Percentage of topology nodes actively participating", "%",
        {"warning": 70, "critical": 50}
    ),
    "compute_distribution": TelemetryMetric(
        "Compute Distribution", ArchitectureLayer.J9, Dimension.C,
        AutognosisLevel.OPTIMIZATION, ["T4", "T5", "T9"],
        "Evenness of compute load across distribution gradients", "ratio",
        {"warning": 0.7, "critical": 0.5}
    ),
    
    # Cross-layer metrics
    "system_coherence": TelemetryMetric(
        "System Coherence", ArchitectureLayer.B9, Dimension.M,
        AutognosisLevel.SELF_IMAGE, ["T9"],
        "Overall system integration and alignment score", "score",
        {"warning": 0.7, "critical": 0.5}
    ),
    "renewal_cycle_time": TelemetryMetric(
        "Renewal Cycle Time", ArchitectureLayer.P9, Dimension.G,
        AutognosisLevel.OPTIMIZATION, ["T9"],
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
    if metric_key in ["edge_throughput", "topology_coverage", "compute_distribution", 
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
    """Map architecture layer to recommended Grove Guides."""
    mapping = {
        ArchitectureLayer.B9: ["Context Map", "Stakeholder Map", "Graphic History"],
        ArchitectureLayer.P9: ["Graphic Gameplan", "Graphic Roadmap", "Five Bold Steps"],
        ArchitectureLayer.J9: ["Investment Portfolio", "Value Proposition", "Industry Structure Map"],
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
                "dimension": metric.dimension.value,
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
        layer_names = {"b9": "b9 (Connection Edges)", "p9": "p9 (Execution Membranes)", "j9": "j9 (Distribution Gradients)"}
        
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
            lines.append(f"- **Layer:** {rec['layer']} | **Dimension:** {rec['dimension']}")
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
