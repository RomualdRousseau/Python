"""A streaming word-counting workflow.
"""

import json
import argparse
import logging

import pandas as pd

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

SALES_SCHEMA = [
    'id',
    'rowNum',
    'sheetName',
    'date',
    'customerCode',
    'customerName',
    'productCode',
    'productName',
    'quantity',
    'amount']


class CustomPipelineOptions(PipelineOptions):
    """ CustomPipelineOptions
    """
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--input_subscription',
            required=True,
            help=(
                'Input PubSub subscription of the form '
                '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>".'))
        parser.add_value_provider_argument(
            '--output_table',
            required=True,
            help=(
                'Output BigQuery table for results specified as: '
                'PROJECT:DATASET.TABLE or DATASET.TABLE.'))


class ReadCsvFile(beam.DoFn):
    """ ReadCsvFile
    """
    def process(self, element):
        path = element
        print(f"Processing {path} ...")
        data = pd.read_csv(path, names = SALES_SCHEMA, skiprows=1)
        data["id"]=data["rowNum"]
        return data.to_dict("records")


def to_table_schema(schema):
    """ Transform the schema into a BigQuery table schema
    """
    return ",".join(map(lambda x: f"{x}:STRING", schema))


def main(argv=None, save_main_session=True):
    """ Build and run the pipeline.
    """

    parser = argparse.ArgumentParser()
    _, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    custom_options = pipeline_options.view_as(CustomPipelineOptions)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
    pipeline_options.view_as(StandardOptions).streaming = True
    with beam.Pipeline(options=pipeline_options) as pipeline:
        _ = (
            pipeline
            | "ReadPubSub" >> beam.io.ReadFromPubSub(
                subscription=str(custom_options.input_subscription)).with_output_types(bytes)
            | "DecodeMessage" >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
            | "ExtractFilePath" >> beam.Map(lambda x: f"gs://{x['bucket']}/{x['file_name']}")
            | "ReadCsvFile" >> beam.ParDo(ReadCsvFile())
            | "WriteData" >> beam.io.WriteToBigQuery(
                custom_options.output_table,
                schema=to_table_schema(SALES_SCHEMA),
                method="FILE_LOADS",
                triggering_frequency=10,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
