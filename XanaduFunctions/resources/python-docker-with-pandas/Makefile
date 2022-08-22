NAME = romualdrousseau/python
TAG = 3

.PHONY: push clean

build: 
	docker build --tag $(NAME):$(TAG) .

push:
	docker push $(NAME):$(TAG)

clean:
	docker image rm $(NAME):$(TAG)

