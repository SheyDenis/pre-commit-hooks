ISORT = isort
YAPF = yapf
CONFIGS_PATH = personal_pre_commit_hooks/configs

isort:
	${ISORT} --settings-file ${CONFIGS_PATH}/isort.cfg --src personal_pre_commit_hooks/ --src tools/ .

format:
	${YAPF} --in-place --style ${CONFIGS_PATH}/yapf_style --recursive personal_pre_commit_hooks/ tools/

all: isort format
