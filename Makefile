CONTAINER_NAME=django-docker

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

update_requirements:
	docker compose up --build