NAME = romualdrousseau/function-example
TAG = latest

SOURCES = main.py

.PHONY: push clean

build: $(SOURCES) Dockerfile
	docker build --tag $(NAME):$(TAG) .

push:
	docker push $(NAME):$(TAG)

clean:
	docker image rm $(NAME):$(TAG)

