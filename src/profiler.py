# Assuming we have our profiling functions from Day 2
MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value):
    if value is None:
        return True
    return value.strip().casefold() in MISSING_VALUES

def try_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def infer_type(values):
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def numeric_stats(values):
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums = [try_float(v) for v in usable if try_float(v) is not None]
    count = len(nums)
    return {
        "count": count,
        "missing": missing,
        "unique": len(set(nums)),
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "mean": sum(nums) / count if count else None,
    }

def text_stats(values, top_k=3):
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    counts = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top = [{"value": v, "count": c} for v, c in sorted_items[:top_k]]
    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }

def profile_csv(rows):
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}

    columns = list(rows[0].keys())
    col_profiles = []

    for col in columns:
        values = [row.get(col, "") for row in rows]
        col_type = infer_type(values)

        if col_type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        col_profiles.append({
            "name": col,
            "type": col_type,
            **stats
        })

    return {
        "n_rows": len(rows),
        "n_cols": len(columns),
        "columns": col_profiles
    }

