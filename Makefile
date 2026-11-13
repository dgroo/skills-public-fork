SKILLS_DIR := $(CURDIR)/skills
TARGET_DIR := $(HOME)/.claude/skills
# The repo loads as one Claude Code plugin: a folder with .claude-plugin/plugin.json
# under ~/.claude/skills is loaded in place, and its skills are named <plugin>:<skill>.
# PLUGIN_NAME must match "name" in .claude-plugin/plugin.json.
PLUGIN_NAME := vfs
PLUGIN_LINK := $(TARGET_DIR)/$(PLUGIN_NAME)
HOOKS_SRC := $(CURDIR)/scripts/hooks
HOOKS_DST := $(CURDIR)/.git/hooks

SKILL_DIRS := $(wildcard $(SKILLS_DIR)/*)

.PHONY: install uninstall unlink-legacy list install-hooks check-pii upstream-check upstream-skills readme-index readme-check design-directory-check

install: install-hooks
	@mkdir -p "$(TARGET_DIR)"
	@if [ -L "$(PLUGIN_LINK)" ] && [ "$$(readlink "$(PLUGIN_LINK)")" = "$(CURDIR)" ]; then \
		echo "  ok  $(PLUGIN_NAME) plugin (already linked)"; \
	elif [ -e "$(PLUGIN_LINK)" ] || [ -L "$(PLUGIN_LINK)" ]; then \
		echo "  ‼ COLLISION  $(PLUGIN_LINK) already exists and is not this repo's; the $(PLUGIN_NAME) plugin is NOT installed until you remove or rename it"; \
		exit 1; \
	else \
		ln -s "$(CURDIR)" "$(PLUGIN_LINK)"; \
		echo "  link  $(PLUGIN_NAME) plugin → $(CURDIR)"; \
	fi
	@for target in "$(TARGET_DIR)"/*; do \
		[ -L "$$target" ] || continue; \
		dest=$$(readlink "$$target"); \
		case "$$dest" in \
			"$(SKILLS_DIR)"/*) ;; \
			*) continue ;; \
		esac; \
		if [ ! -e "$$dest" ]; then \
			rm "$$target"; \
			echo "  prune  $$(basename "$$target") (source skill removed)"; \
		fi; \
	done
	@legacy=0; for skill in $(SKILL_DIRS); do \
		target="$(TARGET_DIR)/$$(basename "$$skill")"; \
		if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$skill" ]; then legacy=$$((legacy + 1)); fi; \
	done; \
	echo ""; \
	if [ "$$legacy" -gt 0 ]; then \
		echo "Done. $$legacy per-skill symlinks from the old layout are still in place, so those skills load"; \
		echo "from them and do not show the $(PLUGIN_NAME): prefix yet. Running sessions depend on them:"; \
		echo "remove them with 'make unlink-legacy' only when no session on this host needs them."; \
	else \
		echo "Done. Skills load as the $(PLUGIN_NAME) plugin: /$(PLUGIN_NAME):<skill>, or the bare /<skill>."; \
	fi

# The per-skill symlinks ~/.claude/skills/<name> are the layout before the repo
# loaded as a plugin. A plugin skill that is the same file as one of them is
# dropped in its favour, so they are what keeps the prefix from showing.
unlink-legacy:
	@for skill in $(SKILL_DIRS); do \
		name=$$(basename "$$skill"); \
		target="$(TARGET_DIR)/$$name"; \
		if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$skill" ]; then \
			rm "$$target"; \
			echo "  unlink  $$name"; \
		elif [ -e "$$target" ]; then \
			echo "  SKIP  $$name — exists but not our symlink (not touching)"; \
		fi; \
	done

uninstall: unlink-legacy
	@if [ -L "$(PLUGIN_LINK)" ] && [ "$$(readlink "$(PLUGIN_LINK)")" = "$(CURDIR)" ]; then \
		rm "$(PLUGIN_LINK)"; \
		echo "  unlink  $(PLUGIN_NAME) plugin"; \
	else \
		echo "  ok  $(PLUGIN_NAME) plugin (not installed)"; \
	fi

install-hooks:
	@if [ ! -d "$(HOOKS_DST)" ]; then \
		echo "  SKIP  hooks — $(HOOKS_DST) doesn't exist (not a git checkout?)"; \
	else \
		for hook in $(HOOKS_SRC)/*; do \
			name=$$(basename "$$hook"); \
			target="$(HOOKS_DST)/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$hook" ]; then \
				echo "  ok  hook $$name (already linked)"; \
			elif [ -e "$$target" ]; then \
				echo "  SKIP  hook $$name — already exists at $$target (not overwriting)"; \
			else \
				ln -s "$$hook" "$$target"; \
				echo "  link  hook $$name → $$hook"; \
			fi; \
		done; \
	fi

check-pii:
	@bash $(CURDIR)/scripts/check-pii.sh --all

# The skills index: README § Skills and `/skills-list … brief`, generated from each
# skill's summary: and group: (scripts/skills-index.py).
readme-index:
	@python3 $(CURDIR)/scripts/skills-index.py readme

readme-check:
	@python3 $(CURDIR)/scripts/skills-index.py check

upstream-check:
	@bash $(CURDIR)/scripts/upstream-check.sh

upstream-skills:
	@git ls-tree -r --name-only upstream/main 2>/dev/null \
		| awk -F/ '$$1 == "skills" && NF >= 2 { print $$2 }' \
		| sort -u \
		|| echo "(no upstream remote configured — see 'git remote -v')"

list:
	@echo "Skills in this repo:"
	@for skill in $(SKILL_DIRS); do \
		name=$$(basename "$$skill"); \
		desc=$$(awk '/^description:/{sub(/^description: */, ""); print; exit}' "$$skill/SKILL.md" 2>/dev/null || echo "(no description)"); \
		echo "  $$name — $$desc"; \
	done
	@echo ""
	@echo "Installed symlinks in $(TARGET_DIR):"
	@for skill in $(SKILL_DIRS); do \
		name=$$(basename "$$skill"); \
		target="$(TARGET_DIR)/$$name"; \
		if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$$skill" ]; then \
			echo "  ✓ $$name"; \
		elif [ -e "$$target" ]; then \
			echo "  ✗ $$name (exists, not our link)"; \
		else \
			echo "  - $$name (not installed)"; \
		fi; \
	done

# The standard design/ layout lives in skills/design-directory/templates/standard/.
# This sets it up in a scratch directory and asks the reader (backlog-scan) what it
# sees, so the two cannot drift apart unnoticed.
design-directory-check:
	@python3 "$(SKILLS_DIR)/design-directory/design-directory.py" selfcheck
