import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. 운동 트레이닝 처치 전후 예시 데이터 (VO2max)
np.random.seed(42)
n_participants = 12
pre_vo2 = np.random.normal(loc=42.5, scale=3.0, size=n_participants)
post_vo2 = pre_vo2 + np.random.normal(loc=4.2, scale=1.2, size=n_participants)

df = pd.DataFrame({
    'Subject': [f'S{i+1:02d}' for i in range(n_participants)],
    'Pre': pre_vo2,
    'Post': post_vo2
})

# 2. Paired t-test 및 Effect Size(Cohen's d) 계산
t_stat, p_val = stats.ttest_rel(df['Pre'], df['Post'])
diff = df['Post'] - df['Pre']
cohen_d = np.mean(diff) / np.std(diff, ddof=1)

print("=== 운동 처치 전후 VO2max 대응표본 t-검정 결과 ===")
print(f"Pre VO2max  : {df['Pre'].mean():.2f} ± {df['Pre'].std():.2f} mL/kg/min")
print(f"Post VO2max : {df['Post'].mean():.2f} ± {df['Post'].std():.2f} mL/kg/min")
print(f"t-statistic : {t_stat:.3f}")
print(f"p-value     : {p_val:.4f}")
print(f"Cohen's d   : {cohen_d:.3f}")

# 3. 논문용 개별 변화 추이 그래프 (Paired Plot) 생성
fig, ax = plt.subplots(figsize=(6, 5), dpi=300)

# 개별 피험자 반응 선 그래프
for i in range(n_participants):
    ax.plot(['Pre-Training', 'Post-Training'], [df.loc[i, 'Pre'], df.loc[i, 'Post']], 
            color='gray', alpha=0.5, marker='o', linewidth=1.5)

# 평균 ± 표준편차 표시
means = [df['Pre'].mean(), df['Post'].mean()]
stds = [df['Pre'].std(), df['Post'].std()]
ax.errorbar(['Pre-Training', 'Post-Training'], means, yerr=stds, 
            color='black', fmt='-s', linewidth=2.5, markersize=8, capsize=5, label='Mean ± SD')

# 유의성 표시 (* p < 0.001)
y_max = max(df['Pre'].max(), df['Post'].max()) + 1.5
ax.plot([0, 0, 1, 1], [y_max, y_max+0.3, y_max+0.3, y_max], color='black', lw=1.2)
ax.text(0.5, y_max+0.4, '*** (p < 0.001)', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('VO2max (mL/kg/min)', fontsize=11, fontweight='bold')
ax.set_title('Effect of 8-Week Training on VO2max', fontsize=12, pad=15)
ax.set_ylim(35, y_max + 3)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('stat_results_figure.png', dpi=300)
print('[성공] 통계 시각화 Figure 생성 완료: stat_results_figure.png')
