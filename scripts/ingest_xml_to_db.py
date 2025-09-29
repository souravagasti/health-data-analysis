from src import get_settings
from src.extract.apple_health import parse_xml
from src.extract.apple_health import extract_steps
from src.extract.apple_health import extract_sleep
from src.extract.apple_health import extract_hr
from src.db import get_engine, read_table, write_table
# from src.llm import get_llm_response

# (apple-health) souravagasti@Souravs-MacBook-Air health % python3 -m scripts.ingest_xml_to_db

def main():
    print("Starting...")
    root = parse_xml("data/raw/export.xml")
    steps_df = extract_steps(root)
    print("Extracted steps")
    sleep_df = extract_sleep(root)
    print("Extracted sleep")
    hr_df = extract_hr(root)
    print("Extracted heart rate")
    # print(type(steps_df),type(sleep_df),type(hr_df))
    
    # print(steps_df.shape, steps_daily.shape)

    # TODO: convert to DataFrames and save
    write_table(steps_df, "steps", "health", get_engine())
    print(f"Wrote steps ({steps_df.shape[0]} records)")
    # write_table(steps_daily, "steps_daily", "health", get_engine())
    write_table(sleep_df, "sleep", "health", get_engine())
    print(f"Wrote sleep ({sleep_df.shape[0]} records)")
    # write_table(sleep_daily, "sleep_daily", "health", get_engine())
    write_table(hr_df, "heart", "health", get_engine())
    print(f"Wrote heart rate ({hr_df.shape[0]} records)")
    # write_table(hr_daily, "heart_daily", "health", get_engine())

    # at this point we have the data in the db
    # we can use the llm to generate insights
    # or use metabase to visualize

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Encountered error:", e)
        raise e
