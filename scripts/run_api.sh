#!/bin/bash
# Usage: scripts/run_api.sh

source prepare_path.sh
mkdir -p logs

echo
echo "==================================================="
echo "RUNNING: api, taboo+wordle x en+ru"
echo "==================================================="
echo "==================================================="
echo

models=(
"llama-3.1-8b-openrouter"
"gpt-4o-2024-11-20-openrouter"
"claude-3-5-sonnet-2024-10-22-openrouter"
"qwen-2.5-72B-Instruct-openrouter"
)

inst_taboo_en=(
"instances_v2.0_en_conceptnet"
)

inst_taboo_ru=(
"instances_v2.0_ru_manual"
)

inst_taboo_ru_translated=(
"instances_v2.0_ru_conceptnet_translated"
)


inst_wordle_en=(
"instances_v2.0_en"
"instances_v2.0_en_withclue"
"instances_v2.0_en_withcritic"
)

inst_wordle_en=(
"instances_v2.0_ru"
"instances_v2.0_ru_withclue"
"instances_v2.0_ru_withcritic"
)


#for model in gpt-4o-2024-11-20-openrouter claude-3-5-sonnet-2024-10-22-openrouter qwen-2.5-72B-Instruct-openrouter llama-3.1-8b-openrouter; do
for model in "${models[@]}"; do

    for inst in "${inst_taboo_en[@]}"; do
        echo "==================================================="
        echo "Running EN taboo on model: $model, inst: $inst"
        echo "==================================================="
        { time python3 clemcore/cli.py run -g taboo -m $model -i instances_v2.0_en_conceptnet -r results/en; } 2>&1 | tee "logs/run.taboo.en.${model}.log"
    done

    for inst in "${inst_taboo_ru[@]}"; do
        echo "==================================================="
        echo "Running RU taboo on model: $model, inst: $inst"
        echo "==================================================="
        { time python3 clemcore/cli.py run -g taboo -m $model -i instances_v2.0_en_conceptnet -r results/ru; } 2>&1 | tee "logs/run.taboo.ru.${model}.log"
    done

    for inst in "${inst_taboo_ru_translated[@]}"; do
        echo "==================================================="
        echo "Running RU TRANSLATED taboo on model: $model, inst: $inst"
        echo "==================================================="
        { time python3 clemcore/cli.py run -g taboo -m $model -i $inst -r results/ru_translated; } 2>&1 | tee "logs/run.taboo.ru_translated.${model}.log"
    done

    for inst in "${inst_wordle_en[@]}"; do
        echo "==================================================="
        echo "Running EN wordle on model: $model, inst: $inst"
        echo "==================================================="
        { time python3 clemcore/cli.py run -g wordle -m $model -i $inst -r results/en; } 2>&1 | tee "logs/run.wordle.en.${model}.log"
    done

    for inst in "${inst_wordle_ru[@]}"; do
        echo "==================================================="
        echo "Running RU wordle on model: $model, inst: $inst"
        echo "==================================================="
        { time python3 clemcore/cli.py run -g wordle -m $model -i $inst -r results/ru; } 2>&1 | tee "logs/run.wordle.ru.${model}.log"
    done
done

echo "==================================================="
echo "==================================================="
echo "FINISHED: api, taboo+wordle x en+ru"
echo "==================================================="
echo "==================================================="