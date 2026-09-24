"""Small, tested reference checks. Not a hydrological model or source verification."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
import math
from typing import Iterable, Sequence


def finite(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def rainfall_departure(actual_mm: float | None, normal_mm: float | None) -> float | None:
    """Return percent departure; unavailable normal returns None, never zero."""
    if actual_mm is None or normal_mm is None:
        return None
    a, n = finite(actual_mm, "actual"), finite(normal_mm, "normal")
    if a < 0 or n < 0:
        raise ValueError("Rainfall cannot be negative")
    if n == 0:
        return None
    return 100.0 * (a / n - 1.0)


def precipitation_volume_m3(rainfall_mm: float, area_km2: float) -> float:
    """Gross precipitation volume only. It is NOT usable water supply."""
    rain, area = finite(rainfall_mm, "rainfall"), finite(area_km2, "area")
    if rain < 0 or area <= 0:
        raise ValueError("Rainfall must be nonnegative and area positive")
    return rain * area * 1000.0


def aggregate_rainfall_departure(rows: Sequence[tuple[float | None, float | None, float]]) -> float | None:
    """Ratio of area-weighted actual/normal totals, over complete supplied rows.

    Missing rows are rejected. The caller must explicitly define and publish
    any reduced coverage before invoking this on a subset.
    """
    if not rows:
        raise ValueError("No observations")
    actual_sum = normal_sum = 0.0
    for actual, normal, area in rows:
        if actual is None or normal is None:
            raise ValueError("Missing row: define coverage explicitly, do not silently drop it")
        a, n, w = finite(actual, "actual"), finite(normal, "normal"), finite(area, "area")
        if a < 0 or n < 0 or w <= 0:
            raise ValueError("Invalid rainfall or area")
        actual_sum += a * w
        normal_sum += n * w
    return rainfall_departure(actual_sum, normal_sum)


def aggregate_storage_fill(rows: Sequence[tuple[float, float]]) -> float:
    """Storage/capacity ratio over a separately verified common cohort and unit.

    Values above 100% are not silently clipped; the producer must review them.
    """
    if not rows:
        raise ValueError("No reservoirs")
    storage = capacity = 0.0
    for s, c in rows:
        s, c = finite(s, "storage"), finite(c, "capacity")
        if s < 0 or c <= 0:
            raise ValueError("Invalid live storage/capacity")
        storage += s
        capacity += c
    return 100.0 * storage / capacity


@dataclass(frozen=True)
class ComparisonContext:
    metric: str
    definition_version: str
    unit: str
    geography: str
    boundary_version: str
    series: str
    baseline: str
    season: str
    period_kind: str
    cutoff_month_day: str
    cohort: str | None = None
    population_basis: str | None = None


def comparison_problems(left: ComparisonContext, right: ComparisonContext) -> list[str]:
    """Strict guard: harmonization must happen upstream with reviewed lineage."""
    issues = []
    required = ("metric", "definition_version", "unit", "geography", "boundary_version", "series", "baseline", "season", "period_kind", "cutoff_month_day")
    for field in required:
        a, b = getattr(left, field), getattr(right, field)
        if not a or not b:
            issues.append(f"{field}: unknown")
        elif a != b:
            issues.append(f"{field}: mismatch")
    for field in ("cohort", "population_basis"):
        if getattr(left, field) != getattr(right, field):
            issues.append(f"{field}: mismatch")
    return issues


def count_at_or_below(values: Iterable[float], threshold: float) -> tuple[int, int]:
    """Return historical count and denominator, NOT an event return period."""
    xs = [finite(x, "historical value") for x in values]
    t = finite(threshold, "threshold")
    if not xs:
        raise ValueError("No eligible historical observations")
    return sum(x <= t for x in xs), len(xs)


def aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone-aware timestamp required")
    return value


def is_stale(observed_through: datetime, as_of: datetime, max_age: timedelta) -> bool:
    """Use the true observation watermark; retrieval time is not a substitute."""
    observed_through, as_of = aware(observed_through), aware(as_of)
    if max_age.total_seconds() < 0 or observed_through > as_of:
        raise ValueError("Invalid age or future observation")
    return as_of - observed_through > max_age


def forecast_active(issued: datetime, valid_from: datetime, valid_to: datetime, as_of: datetime) -> bool:
    issued, valid_from, valid_to, as_of = map(aware, (issued, valid_from, valid_to, as_of))
    if issued > valid_to or valid_from >= valid_to:
        raise ValueError("Invalid forecast chronology")
    return issued <= as_of and valid_from <= as_of < valid_to
