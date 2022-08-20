.PHONY=deploy

deploy:
	gcloud functions deploy tag-file                                        \
	--runtime=python310                                                     \
	--source=.                                                              \
	--entry-point=on_new_file_inbox                                         \
	--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
	--trigger-event-filters="bucket=inbox-gcp4affi"

