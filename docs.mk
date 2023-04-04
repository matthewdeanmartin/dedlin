MARKDOWNLINT=markdownlint
FILES=$(shell find . -type f -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./.idea/*")

.PHONY: all
all: lint check-links check-style

.PHONY: lint
lint:
	@echo "Linting markdown files with $(MARKDOWNLINT)"
	@for file in $(FILES); do \
		echo "$(MARKDOWNLINT) $$file"; \
		npx $(MARKDOWNLINT) "$$file" --ignore node_modules --ignore .git --ignore .idea; \
	done

.PHONY: check-links
check-links:
	@echo "Checking links in markdown files with linkcheckMarkdown"
	@for file in $(FILES); do \
		linkcheckMarkdown "$$file"; \
	done

.PHONY: check-style
check-style:
	@echo "Checking with proselint"
	@for file in $(FILES); do \
		proselint "$$file"; \
	done
	@echo "Checking links in markdown files with write-good"
	@for file in $(FILES); do \
		npx write-good "$$file"; \
	done
