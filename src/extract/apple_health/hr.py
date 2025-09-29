import pandas as pd
from datetime import datetime

def extract_hr(root) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stub: extract heart rate records."""
    hr_records = []

    for record in root.findall("Record"):
        if record.attrib["type"] == "HKQuantityTypeIdentifierHeartRate":
            start = datetime.fromisoformat(record.attrib["startDate"].replace(" +0530", ""))
            value = int(float(record.attrib.get("value")))
            hr_records.append({"timestamp": start, "bpm": value})
    
    hr_df = pd.DataFrame(hr_records)
    hr_df["date"] = hr_df["timestamp"].dt.date

    # Aggregate average heart rate per hour
    # hr_daily = hr_df.groupby("date")["bpm"].mean().reset_index()

    return hr_df
