def project_indicator(wb_data, field_name="co2_emissions", target_year=2030):
    """
    Fits a linear trend (y = mx + b) to historical World Bank data
    and projects values up to target_year.
    """
    # Extract (year, value) pairs sorted chronologically, skipping None values
    points = sorted(
        (row.year, getattr(row, field_name))
        for row in wb_data
        if getattr(row, field_name) is not None
    )

    # Need at least 2 data points to calculate a trend line
    if len(points) < 2:
        return None

    n = len(points)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    x_mean = sum(xs) / n
    y_mean = sum(ys) / n

    # Ordinary Least Squares (OLS) slope and intercept
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in points)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        return None

    slope = numerator / denominator
    intercept = y_mean - (slope * x_mean)

    last_year = xs[-1]
    future_years = list(range(last_year + 1, target_year + 1))

    # Build aligned arrays for Chart.js
    all_years = xs + future_years
    historical_series = [round(y, 2) for y in ys] + [None] * len(future_years)

    # Connect the projection line starting from the last actual data point
    projected_series = [None] * (len(ys) - 1) + [round(ys[-1], 2)]
    for yr in future_years:
        # Clamp at 0 so emissions/percentages don't project negative
        projected_val = max(0.0, slope * yr + intercept)
        projected_series.append(round(projected_val, 2))

    return {
        "labels": all_years,
        "historical": historical_series,
        "projected": projected_series,
        "slope": round(slope, 3),
        "projected_target": projected_series[-1],
        "target_year": target_year,
    }