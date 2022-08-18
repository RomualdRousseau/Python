.PHONY=deploy test log

FILE=HongKong\ -\ ZUELLIG\ -\ Sales\ -\ 201903_2.xlsx

deploy:
	gcloud functions deploy tag-file                                        \
	--runtime=python310                                                     \
	--region=asia-southeast1                                                \
	--source=src/main                                                       \
	--entry-point=on_new_file_inbox                                         \
	--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
	--trigger-event-filters="bucket=inbox-gcp4affi"

test:
	gsutil                                    \
	-h "x-goog-meta-collection:sales.zuellig" \
	-h "x-goog-meta-batchDate:2022-01-01"     \
	cp data/$(FILE) gs://inbox-gcp4affi

log:
	gcloud functions logs read tag-file
