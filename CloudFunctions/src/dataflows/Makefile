.PHONY=deploy 

deploy: 
	python3 -m finalize_master_account                           \
    --input_topic /topics/gcp4affi-dc76/master_account_finalized \
	--output_table gcp4affi-dc76:outbox_data.outbox              \
    --runner DataflowRunner                                      \
    --temp_location gs://outbox-gcp4affi/temp/                   \
	--requirements_file requirements.txt
