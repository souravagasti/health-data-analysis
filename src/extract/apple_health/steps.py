from datetime import datetime
import pandas as pd

def extract_steps(root) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stub: extract step count records from XML root."""

    steps_records = []

    for record in root.findall("Record"):
        if record.attrib["type"] == "HKQuantityTypeIdentifierStepCount":
            start = datetime.fromisoformat(record.attrib["startDate"].replace(" +0530", ""))
            value = int(record.attrib["value"])
            end = datetime.fromisoformat(record.attrib["endDate"].replace(" +0530", ""))
            steps_records.append({"start_timestamp": start,"end_timestamp": end, "steps": value})
    
    # Aggregate steps per day
    steps_df = pd.DataFrame(steps_records)
    steps_df["date"] = steps_df["start_timestamp"].dt.date
    # steps_daily = steps_df.groupby("date")["steps"].sum().reset_index()

    return steps_df


