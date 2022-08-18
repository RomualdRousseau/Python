import pandas as pd

def on_new_file_inbox(file, context):
    bucket = validate_message(file, "bucket")
    filename = validate_message(file, "name")

    df = pd.read_excel(f"gs://{bucket}/{filename}", header=7)
    print(df)
    df.to_csv(f"gs://outbox-gcp4affi/test.csv")


def validate_message(message, param):
    var = message.get(param)
    if not var:
        raise ValueError(
            "{} is not provided. Make sure you have \
                          property {} in the request".format(
                param, param
            )
        )
    return var
