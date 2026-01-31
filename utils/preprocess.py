import pandas as pd

def monthly_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    group_cols = ["property", "utility", "year", "month"]
    agg = df.groupby(group_cols).agg(
        usage=("usage", "sum"),
        cost=("cost", "sum"),
        occupancy=("occupancy", "mean"),
    ).reset_index()

    agg["usage_per_occupied_unit"] = agg["usage"] / agg["occupancy"].replace(0, pd.NA)
    agg["cost_per_occupied_unit"] = agg["cost"] / agg["occupancy"].replace(0, pd.NA)
    return agg

def occupancy_normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "occupancy" not in df.columns or df["occupancy"].isna().all():
        df["occupancy"] = 1
    df["usage_per_occupied_unit"] = df["usage"] / df["occupancy"].replace(0, pd.NA)
    df["cost_per_occupied_unit"] = df["cost"] / df["occupancy"].replace(0, pd.NA)
    return df

def meter_group(df: pd.DataFrame) -> pd.DataFrame:
    if "meter_number" not in df.columns:
        return pd.DataFrame()
    return df.groupby("meter_number").agg(
        total_usage=("usage", "sum"),
        total_cost=("cost", "sum"),
    ).reset_index()

def provider_group(df: pd.DataFrame) -> pd.DataFrame:
    if "provider_code" not in df.columns:
        return pd.DataFrame()
    return df.groupby("provider_code").agg(
        total_usage=("usage", "sum"),
        total_cost=("cost", "sum"),
    ).reset_index()

def utility_group(df: pd.DataFrame) -> pd.DataFrame:
    if "utility" not in df.columns:
        return pd.DataFrame()
    return df.groupby("utility").agg(
        total_usage=("usage", "sum"),
        total_cost=("cost", "sum"),
    ).reset_index()

def portfolio_summary(df: pd.DataFrame) -> pd.DataFrame:
    total_usage = df["usage"].sum()
    total_cost = df["cost"].sum()
    total_properties = df["property"].nunique()
    total_meters = df["meter_number"].nunique() if "meter_number" in df.columns else 0

    return pd.DataFrame(
        [
            {
                "total_usage": total_usage,
                "total_cost": total_cost,
                "total_properties": total_properties,
                "total_meters": total_meters,
            }
        ]
    )

def property_ranking(df: pd.DataFrame, metric: str = "usage", top_n: int = 5) -> pd.DataFrame:
    if metric not in df.columns:
        return pd.DataFrame()
    grouped = df.groupby("property").agg(
        usage=("usage", "sum"),
        cost=("cost", "sum"),
    ).reset_index()
    return grouped.sort_values(metric, ascending=False).head(top_n)
