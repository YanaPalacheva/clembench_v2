from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

import evaluation.evalutils as utils
import evaluation.makingtables as tables
import evaluation.plotting as plotting
import clemcore.clemgame.metrics as clemmetrics

MODELS = ["llama", "ruadapt", "saiga", "vikhr", "aya", "tower", "gpt", "claude", "qwen"]
LANGS = ['en', 'ru', 'ru_translated']
GAMES = ['taboo', 'wordle', 'wordle_withclue', 'wordle_withcritic']

# rename model players to short names (only for self-play)
def map_model_names(raw_model):
    for model in MODELS:
        if raw_model.lower().startswith(model):
            return model
    print(f"No alias for model {raw_model}")
    return raw_model


def make_general_plots(df_episode_scores, df_paper, df_clem, lang: str):
    zero_one_scores = utils.get_metrics_in_zero_one(df_episode_scores)

    df_01, df_other = utils.filter_metrics_in_zero_one(df_episode_scores,
                                                       zero_one_scores)
    if not df_01.empty:
        plotting.plot_escore_benchmark(df_01, '_in01', lang)       # (2a)
    if not df_other.empty:
        plotting.plot_escore_benchmark(df_other, '_other', lang)   # (2b)

    # Stacked bar plots with success, lose and aborted
    # micro average
    plotting.plot_stacked_micro_bar(df_episode_scores, df_clem, lang)
    # macro_average
    plotting.plot_stacked_macro_bar(df_episode_scores, df_clem, lang)

    # scatter plots with (% played, quality score) for each model
    # we generate for the benchmark, for each game and for each experiment
    plotting.plot_paper_scatter(df_paper, lang)

    # lineplots with quality score for each model across experiments
    plotting.plot_lines(df_episode_scores, lang)

    # barplots with clem score for each model
    plotting.plot_clem_score(df_clem, lang)

def make_game_plots(df_episode_scores: pd.DataFrame):
    for game in GAMES:
        act_df = df_episode_scores[df_episode_scores.game == game]
        # overview of all episode scores
        plotting.plot_escores_game(act_df, game)
        plotting.plot_escores_line_game(act_df, game)

        zero_one_scores = utils.get_metrics_in_zero_one(df_episode_scores)
        # one plot for each metric
        for metric, metric_df in act_df.groupby('metric'):
            lims = utils.get_metric_lims(metric, zero_one_scores)
            plotting.plot_escores_game_metric(metric_df, game, metric, lims)
            plotting.plot_escores_line_game_metric(metric_df, game, metric, lims)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--results_path",
                        type=str,
                        default='./results',
                        help="Path to the results folder containing scores.")
    parser.add_argument('--no_plots', action='store_true',
                        help='Do not generate plots.')
    args = parser.parse_args()

    episode_scores = []
    for lang in LANGS:
        results_path = f'{args.results_path}/{lang}'
        # Read raw episode scores into a df
        scores = utils.load_scores(path=results_path)
        utils.create_eval_tree(scores.keys(), lang)
        df_episode_scores = pd.read_csv(Path(results_path) / f'raw.csv')
        df_episode_scores.drop(df_episode_scores.columns[0], axis=1, inplace=True)
        df_episode_scores['lang'] = lang
        episode_scores.append(df_episode_scores)

        df_episode_scores['model'] = df_episode_scores['model'].map(lambda x: map_model_names(x))

        if lang == 'ru_translated':  # consider only for taboo-specific analysis
            continue

        print(f'\t Generating tables and plots for episode-level scores, language: {lang}...')
        df_paper = tables.save_paper_table(df_episode_scores, lang)
        df_clem = tables.save_clem_score_table(df_paper, lang)
        # Games vs. models with episode scores dispersion metrics across all episodes and experiments
        df_bench_table = tables.make_stats_table(df_episode_scores, lang)

        if not args.no_plots:
            make_general_plots(df_episode_scores, df_paper, df_clem, lang)

    df_all_episode_scores = pd.concat(episode_scores, ignore_index=True)

    print('\n Generating tables and plots for games...')
    # taboo: also add analysis for ru_translated
    # One table for each game aggregated by experiment
    tables.make_overview_by_game(df_all_episode_scores)
    if not args.no_plots:
        make_game_plots(df_all_episode_scores)







