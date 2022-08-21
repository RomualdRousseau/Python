.PHONY=deploy test log

deploy: 
	python3 -m finalize_master_account                                             \
	--project gcp4affi-dc76                                                        \
	--region asia-southeast1                                                       \
	--runner DataflowRunner                                                        \
	--staging_location gs://var-gcp4affi/staging                                   \
	--template_location gs://var-gcp4affi/templates/FinalizeMasterAccount          \
	--temp_location gs://var-gcp4affi/temp/                                        \
	--requirements_file requirements.txt                                           \
	--no_use_public_ips                                                            \
	--num_workers=2                                                                \
	--max_num_workers=3                                                            \
	--input_subscription projects/gcp4affi-dc76/subscriptions/new-file-outbox-test \
	--output_table gcp4affi-dc76:outbox_data.outbox


test:
	python3 -m finalize_master_account                                             \
	--temp_location gs://outbox-gcp4affi/temp/                                     \
	--input_subscription projects/gcp4affi-dc76/subscriptions/new-file-outbox-test \
	--output_table gcp4affi-dc76:outbox_data.outbox

log:
	echo "Not implemented"
