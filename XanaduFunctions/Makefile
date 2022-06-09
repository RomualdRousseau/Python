NAME = function-example

.PHONY: build push clean deploy 

define FOREACH
	for DIR in */.; do \
		$(MAKE) -C $$DIR $(1); \
	done
endef

all: build push deploy

build:
	$(call FOREACH, $@)

push:
	$(call FOREACH, $@)

clean:
	$(call FOREACH, $@)

deploy: 
	docker stack deploy --compose-file docker-compose.yml --with-registry-auth $(NAME) 

delete:
	docker stack rm $(NAME)

redeploy: delete deploy
