docker-run:
	cat websites.txt | docker compose run -T --build --rm extractor 