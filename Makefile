IMAGE := ghcr.io/2nothing4/bfd-tracker:latest

.PHONY: build run test seed list

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm -v $(HOME)/.bfd_tracker.json:/app/.bfd_tracker.json $(IMAGE)

test:
	python3 tracker.py seed && python3 tracker.py list

seed:
	python3 tracker.py seed

list:
	python3 tracker.py list
