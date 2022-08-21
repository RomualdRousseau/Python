.PHONY=deploy test log

FILE=HongKong\ -\ ZUELLIG\ -\ Sales\ -\ 201903_2.xlsx

deploy:
	gcloud functions deploy tag-file                                            \
	--runtime=python310                                                         \
	--source=.                                                                  \
	--entry-point=on_new_file_inbox                                             \
	--trigger-event-filters="type=google.cloud.storage.object.v1.finalized"     \
	--trigger-event-filters="bucket=inbox-gcp4affi"                             \
	--set-env-vars "PROJECT_ID=gcp4affi-dc76"                                   \
	--set-env-vars "OUTPUT=outbox-gcp4affi"                                     \
	--set-env-vars "TOPIC=new-file-outbox"                                      \
	--set-env-vars "DSL_BASE_URL=https://deepsealoader.servier.com"             \
	--set-env-vars "DSL_TOKEN=YnJ1Y2UuYmFubmVyQHNlcnZpZXIuY29tOmJhbm5lcg=="

test:
	gsutil                                    \
	-h "x-goog-meta-collection:sales.zuellig" \
	-h "x-goog-meta-batchDate:2022-01-01"     \
	cp ../../data/$(FILE) gs://inbox-gcp4affi

log:
	gcloud functions logs read tag-file
