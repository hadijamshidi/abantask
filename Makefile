
fake_data:
	docker exec -it web python create_fake_data.py

local:
	docker compose up -d --build --remove-orphans && docker compose logs -f -n 5


test:
	docker compose up -d --build --remove-orphans web && docker exec -it web python manage.py test

shell:
	docker exec -it web python manage.py shell

stop:
	docker compose down
