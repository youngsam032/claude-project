import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. 운동검사 원천 샘플 CSV 데이터 자동 생성
np.random.seed(2026)
n_per_group = 10
raw_data = {
    'Subject_ID': [f'Sub_{i+1:02d}' for i in range(n_per_group * 2)],
    'Group': ['Control']*n_per_group + ['Training']*n_per_group,
    'Pre_VO2': np.round(np.random.normal(41.0, 3.0, n_per_group * 2), 1),
    'Post_VO2': np.append(np.round(np.random.normal(41.2, 3.1, n_per_group), 1), 
                          np.round(np.random.normal(46.8, 2.9, n_per_group), 1)),
    'Pre_Lactate': np.round(np.random.normal(8.5, 1.2, n_per_group * 2), 1),
    'Post_Lactate': np.append(np.round(np.random.normal(8.4, 1.1, n_per_group), 1),
                              np.round(np.random.normal(10.2, 1.4, n_per_group), 1))
}
df_raw = pd.DataFrame(raw_data)
df_raw.to_csv('raw_exercise_data.csv', index=False, encoding='utf-8-sig')
print('[완료] 원천 측정 데이터 파일 생성: raw_exercise_data.csv')

# 2. CSV 파일 자동 파싱 및 변수 계산
df = pd.read_csv('raw_exercise_data.csv')
df['VO2_Diff'] = df['Post_VO2'] - df['Pre_VO2']
df['Lactate_Diff'] = df['Post_Lactate'] - df['Pre_Lactate']

# 3. 정규성 검정 (Shapiro-Wilk Test)
_, p_norm_con = stats.shapiro(df[df['Group']=='Control']['VO2_Diff'])
_, p_norm_trn = stats.shapiro(df[df['Group']=='Training']['VO2_Diff'])

print('\n=== 데이터 정규성 검정 (Shapiro-Wilk Test) ===')
print(f'Control Group VO2 Diff Normality p-value  : {p_norm_con:.4f}')
print(f'Training Group VO2 Diff Normality p-value : {p_norm_trn:.4f}')

# 4. 요약 통계표 엑셀 자동 내보내기
summary = df.groupby('Group')[['Pre_VO2', 'Post_VO2', 'VO2_Diff', 'Pre_Lactate', 'Post_Lactate', 'Lactate_Diff']].agg(['mean', 'std']).round(2)
summary.to_excel('analysis_summary_report.xlsx')
print('\n[완료] 논문 제출용 요약 통계 엑셀 보고서 생성: analysis_summary_report.xlsx')
