#!/bin/bash
# Usage: scripts/transcribe_score.sh

langs=(
"en"
"ru"
"ru_translated"
)

games=(
"taboo"
"wordle"
"wordle_withclue"
"wordle_withcritic"
)

for lang in "${langs[@]}"; do
    for game in "${games[@]}"; do

        # custom experiment
        if [[ "$lang" == "ru_translated" && "$game" == wordle* ]]; then
            echo "Skipping game: $game for language: $lang"
            continue
        fi

        echo "Processing game: $game, language: $lang"

        python3 clemcore/cli.py transcribe -g "$game" -r "results/$lang"

        python3 clemcore/cli.py score -g "$game" -r "results/$lang"
    done
done


