deploy:
	gcloud functions deploy tag-file											\
		--runtime=python310 													\
		--region=asia-southeast1												\
		--source=src															\
		--entry-point=on_new_file_inbox											\
		--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
		--trigger-event-filters="bucket=inbox-gcp4affi"

test:
	gsutil cp data/HongKong\ -\ ZUELLIG\ -\ Sales\ -\ 201903_2.xlsx gs://inbox-gcp4affi/sales.zuellig
