all: save organize patch_image_paths

.PHONY: save
save:
	mkdir -p notes
	shortcuts run "Export Notes" -i ./notes

.PHONY: organize
organize: 
	python3 scripts/organize.py ./notes

.PHONY: patch_image_paths
patch_image_paths:
	python3 scripts/patch_image_paths.py ./notes

.PHONY: clean
clean:
	rm -rf ./notes