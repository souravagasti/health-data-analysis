from datetime import datetime
import pandas as pd

def extract_sleep(root) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stub: extract sleep analysis records."""

    sleep_records = []

    for record in root.findall("Record"):
        if record.attrib["type"] == "HKCategoryTypeIdentifierSleepAnalysis":
            start = datetime.fromisoformat(record.attrib["startDate"].replace(" +0530", ""))
            end = datetime.fromisoformat(record.attrib["endDate"].replace(" +0530", ""))
            value = record.attrib.get("value")
            hours = (end - start).total_seconds() / 3600.0
            sleep_records.append({"start_timestamp": start, "end_timestamp": end, "value": value, "hours": hours})
    
    sleep_df = pd.DataFrame(sleep_records)
    sleep_df["date"] = sleep_df["start_timestamp"].dt.date

    # Aggregate total sleep duration per day
    # sleep_daily = sleep_df.groupby(["date"])["hours"].sum().reset_index()

    return sleep_df
    
