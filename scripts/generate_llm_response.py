from src import generate_code, read_table, get_engine, execute_code
import pandas as pd
# from Ipython.display import display


df = read_table(schema_name="health",table_name="combined_features",engine=get_engine())
cols = df.columns.tolist()
question = "Are steps related to sleep?"
code = generate_code(question,cols,"health.combined_features")
print("Generated code:")
print(code)

# print("\nExecuting code...")
# df_output = execute_code(df, code)
# print(type(df_output))
# print("Done.")
# print("\nResult:")
# print(df_output.head(10))


# python3 -m scripts.generate_llm_response

