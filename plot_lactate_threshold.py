import numpy as np
import matplotlib.pyplot as plt

# 운동생리학 예시 데이터: 점증적 부하 운동 검사 (Watts, Lactate, VO2)
workload = np.array([100, 140, 180, 220, 260, 300, 340])
lactate = np.array([1.2, 1.4, 1.8, 2.3, 3.8, 6.5, 10.2])
vo2 = np.array([1.8, 2.3, 2.9, 3.5, 4.1, 4.6, 4.8])

fig, ax1 = plt.subplots(figsize=(8, 5), dpi=300)

# Blood Lactate Curve
color = 'tab:red'
ax1.set_xlabel('Workload (Watts)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Blood Lactate (mmol/L)', color=color, fontsize=11, fontweight='bold')
ax1.plot(workload, lactate, color=color, marker='o', linewidth=2, label='Lactate')
ax1.tick_params(axis='y', labelcolor=color)
ax1.axvline(x=240, color='gray', linestyle='--', label='Lactate Threshold (~240W)')

# VO2 Curve
ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('VO2 (L/min)', color=color, fontsize=11, fontweight='bold')
ax2.plot(workload, vo2, color=color, marker='s', linewidth=2, linestyle=':', label='VO2')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Incremental Exercise Test: Lactate Threshold and VO2 Response', fontsize=13, pad=12)
fig.tight_layout()
plt.savefig('lactate_threshold_figure.png', dpi=300)
print('[성공] 논문용 Figure 파일 생성 완료: lactate_threshold_figure.png')
