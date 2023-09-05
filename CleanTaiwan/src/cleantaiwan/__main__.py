import os
import pandas as pd

PATH = "data/"

def remove_last_line(path: str) -> None:
    print(f"Processing {path} ... ", end="")
    df = pd.read_parquet(path)
    last_row_fields = df.iat[-1,0]

    delete_last_line = False
    for field in last_row_fields:
        if field["tag"] == "quantity" and not field["value"].isdigit():
            delete_last_line = True

    if delete_last_line:
        df.drop(index=df.index[-1], axis=0, inplace=True)
        df.to_parquet(path)
        print("Patched.")
    else:
        print("No changes.")

for root, dirs, files in os.walk(PATH):
    for file in files:
        remove_last_line(os.path.join(root, file))

