from src.utils import run_sql_file

def main():
    df = run_sql_file("scripts/sleep_steps_hr.sql",as_table="health.combined_features")
    print(f"Wrote combined_features ({df.shape[0]} records)")
    # print(df.head())

if __name__ == "__main__":
    main()