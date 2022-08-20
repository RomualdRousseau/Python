.PHONY=deploy-functions deploy-dataflows test log

FILE=HongKong\ -\ ZUELLIG\ -\ Sales\ -\ 201903_2.xlsx

deploy-functions:
	$(MAKE) -C src/functions deploy

deploy-dataflow:
	$(MAKE) -C src/dataflows deploy

test:
	gsutil                                    \
	-h "x-goog-meta-collection:sales.zuellig" \
	-h "x-goog-meta-batchDate:2022-01-01"     \
	cp data/$(FILE) gs://inbox-gcp4affi

log:
	gcloud functions logs read tag-file
