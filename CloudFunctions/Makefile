.PHONY=deploy deploy-functions deploy-dataflows

deploy: deploy-functions deploy-dataflows

deploy-functions:
	$(MAKE) -C src/functions deploy

deploy-dataflows:
	$(MAKE) -C src/dataflows deploy
