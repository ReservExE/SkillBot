import seaborn as sns
import matplotlib.pyplot as mp
import time

def visualize_skills(df):
    plot_path = 'F:/SkillBot/data/__plots/plot.' + str(time.time()) + '.png'
    df['Skill'] = df.index
    sample_size = 0
    sns.set_theme()
    mp.figure(figsize=(9, 5))
    mp.tight_layout()
    plot = sns.barplot(data=df,
                       x='Occurrence',
                       y='Skill')
    plot.set_yticklabels(plot.get_yticklabels(), rotation=40, ha="right", fontsize=8)
    plot.set_title(f"Data based on {sample_size} user-imitated searches", fontsize=12)
    mp.savefig(plot_path, bbox_inches='tight')

    return plot_path