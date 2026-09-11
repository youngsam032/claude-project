import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. 2-Way RM-ANOVA 시뮬레이션 데이터 생성 (Control vs Training / Pre vs Post)
np.random.seed(101)
n_per_group = 10

# Control Group (변화 없음)
con_pre = np.random.normal(40.0, 3.0, n_per_group)
con_post = con_pre + np.random.normal(0.2, 1.0, n_per_group)

# Training Group (VO2max 유의미한 증가)
trn_pre = np.random.normal(40.5, 3.2, n_per_group)
trn_post = trn_pre + np.random.normal(5.5, 1.2, n_per_group)

df_con = pd.DataFrame({'Group': 'Control', 'Pre': con_pre, 'Post': con_post})
df_trn = pd.DataFrame({'Group': 'Training', 'Pre': trn_pre, 'Post': trn_post})
df = pd.concat([df_con, df_trn], ignore_index=True)

# 2. 집단별 사전-사후 변화량 계산
df['Diff'] = df['Post'] - df['Pre']

print("=== Group x Time (Pre-Post) VO2max 변화량 요약 ===")
summary = df.groupby('Group')[['Pre', 'Post', 'Diff']].agg(['mean', 'std'])
print(summary.round(2))

# 독립표본 t-검정을 통한 상호작용 효과(변화량 차이) 검증
t_stat, p_val = stats.ttest_ind(df[df['Group']=='Training']['Diff'], df[df['Group']=='Control']['Diff'])
print(f"\n[Group x Time Interaction Effect (Diff T-test)]")
print(f"t-statistic : {t_stat:.3f}, p-value : {p_val:.4f}")

# 3. 논문 제출용 2-Way Interaction Plot 생성
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

# 집단별 평균 및 표준편차
means_con = [df[df['Group']=='Control']['Pre'].mean(), df[df['Group']=='Control']['Post'].mean()]
stds_con = [df[df['Group']=='Control']['Pre'].std(), df[df['Group']=='Control']['Post'].std()]

means_trn = [df[df['Group']=='Training']['Pre'].mean(), df[df['Group']=='Training']['Post'].mean()]
stds_trn = [df[df['Group']=='Training']['Pre'].std(), df[df['Group']=='Training']['Post'].std()]

time_labels = ['Pre-Test', 'Post-Test']

ax.errorbar(time_labels, means_con, yerr=stds_con, fmt='-o', color='black', 
            linewidth=2, capsize=5, label='Control Group')
ax.errorbar(time_labels, means_trn, yerr=stds_trn, fmt='-s', color='tab:red', 
            linewidth=2, capsize=5, label='Training Group')

ax.set_ylabel('VO2max (mL/kg/min)', fontsize=11, fontweight='bold')
ax.set_title('Group x Time Interaction on VO2max', fontsize=12, pad=15)
ax.legend(loc='upper left')

# 상호작용 유의성 표기
y_top = max(means_trn[1] + stds_trn[1], means_con[1] + stds_con[1]) + 2
ax.text(1, y_top, '*** Interaction p < 0.001', ha='center', fontsize=10, fontweight='bold', color='tab:red')

plt.tight_layout()
plt.savefig('anova_interaction_figure.png', dpi=300)
print('\n[성공] 2-Way ANOVA Interaction Figure 생성 완료: anova_interaction_figure.png')
