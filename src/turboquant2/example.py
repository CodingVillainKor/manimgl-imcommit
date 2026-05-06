"""
TurboQuant (Zandieh et al. 2025, arXiv:2504.19874) - 2-stage 양자화 시각화

핵심:
  - k in R^D, ||k||=1 이면 k의 각 좌표는 (1 - x^2)^((D-3)/2) ~ shifted/scaled Beta((D-1)/2,(D-1)/2)
  - RHT  m = (1/sqrt(D)) * H @ diag(s),  H: Hadamard, s ~ Rademacher
  - m 은 직교행렬:  m^T m = I
  - outlier 가 있는 k 를 L2 정규화 후 m 을 곱하면 outlier 에너지가 모든 좌표로 퍼져 Beta 분포를 따름

TurboQuant_prod (unbiased inner-product variant) — b bits/coord:
  - Stage 1 (b-1 bits): y = m @ k_norm 의 각 좌표에 Beta 분포 최적 Lloyd-Max 스칼라 양자화
                        → 정수 코드 Q_mse(y), 디코드 dequantized_y
  - Stage 2 (1  bit ): 잔차 r = y - dequantized_y 에 QJL 부호 비트
                        → sign(r) 1bit/coord  +  스칼라 ||r||_2
  - 키 1개 저장량:  D 개의 b-bit 코드 + 2 floats (||k||, ||r||)

  - 내적 추정 (m 직교 → m m^T = I 이용해 같은 m 으로 QJL 적용):
      <q, k_norm> ≈ <m@q, dequantized_y>  +  sqrt(pi/(2D)) * ||r|| * <m@q, sign(r)>
      <q, k>     = ||k|| * <q, k_norm>

  - b=1 (특수 케이스) 이면 dequantized_y = 0, ||r|| = 1, sign(r) = sign(y) 로
    Zandieh et al. 2024 의 순수 QJL 과 동치
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

np.random.seed(41)

B, L, D = 1, 30, 256


# ---------- 1. k ~ N(0,1),  shape [B, L, D] ----------
k = np.random.randn(B, L, D).astype(np.float64)


# ---------- 2. L 마다 D 좌표 중 2개에 outlier 주입 ( |15~20| ) ----------
for b in range(B):
    for l in range(L):
        idx = np.random.choice(D, size=2, replace=False)
        signs = np.random.choice([-1, 1], size=2)
        mags = np.random.uniform(15, 20, size=2)
        k[b, l, idx] = signs * mags

fig, ax = plt.subplots(figsize=(12, 4))
vmax = np.abs(k).max()
im = ax.imshow(k[0], aspect='auto', cmap='RdBu_r', vmin=-vmax, vmax=vmax)
ax.set_title('step 2.  k  (outliers injected, 2 per row)')
ax.set_xlabel('D'); ax.set_ylabel('L')
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.show()


# ---------- 3. L2 normalize along D ----------
k_norm = k / np.linalg.norm(k, axis=-1, keepdims=True)

fig, ax = plt.subplots(figsize=(12, 4))
vmax = np.abs(k_norm).max()
im = ax.imshow(k_norm[0], aspect='auto', cmap='RdBu_r', vmin=-vmax, vmax=vmax)
ax.set_title('step 3.  k / ||k||   (outliers still concentrated in 2 coords)')
ax.set_xlabel('D'); ax.set_ylabel('L')
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.show()


# ---------- 4. RHT matrix  m = (1/sqrt(D)) * H @ diag(s) ----------
def hadamard(n):
    H = np.array([[1.0]])
    while H.shape[0] < n:
        H = np.block([[H, H], [H, -H]])
    return H

H = hadamard(D)
s = np.random.choice([-1, 1], size=D).astype(np.float64)
m = (H * s) / np.sqrt(D)

fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(m, cmap='RdBu_r', vmin=-m.max(), vmax=m.max())
ax.set_title(f'step 4.  RHT  m  ({D}x{D})')
plt.tight_layout()
plt.show()


# ---------- 5. m^T m = I  =>  m^T (m k) == k ----------
y = np.einsum('ij,blj->bli', m, k_norm)        # y = m @ k_norm
k_round = np.einsum('ji,blj->bli', m, y)       # m^T @ y = m^T m k = k

fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
vmax = np.abs(k_norm).max()
for ax, data, title in zip(
    axes, [k_norm[0], k_round[0]],
    ['original  k_norm', 'm^T @ m @ k_norm   (should equal k_norm)']
):
    im = ax.imshow(data, aspect='auto', cmap='RdBu_r', vmin=-vmax, vmax=vmax)
    ax.set_title(title); ax.set_ylabel('L')
    plt.colorbar(im, ax=ax)
axes[-1].set_xlabel('D')
fig.suptitle(f'step 5.  max|k - m^T m k| = {np.abs(k_norm - k_round).max():.2e}')
plt.tight_layout()
plt.show()


# ---------- 6.  m @ k_norm  좌표는 Beta 분포 ----------
# y 는 단위구 위 벡터 (|| y || = || k_norm || = 1) 의 좌표
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

vmax = np.abs(y).max()
im = axes[0].imshow(y[0], aspect='auto', cmap='RdBu_r', vmin=-vmax, vmax=vmax)
axes[0].set_title('m @ k_norm   (outlier energy spread uniformly)')
axes[0].set_xlabel('D'); axes[0].set_ylabel('L')
plt.colorbar(im, ax=axes[0])

axes[1].hist(y.flatten(), bins=80, density=True, alpha=0.6,
             edgecolor='black', label='empirical  (m k)_i')
xs = np.linspace(-1, 1, 400)
a = (D - 1) / 2
pdf = beta.pdf((xs + 1) / 2, a, a) / 2       # (x+1)/2 ~ Beta(a,a)
axes[1].plot(xs, pdf, 'r-', lw=2,
             label=f'shifted Beta(a,a), a=(D-1)/2={a:.1f}')
axes[1].set_xlim(-0.3, 0.3)
axes[1].set_title('step 6.  coordinate distribution of m @ k_norm')
axes[1].set_xlabel('value'); axes[1].set_ylabel('density')
axes[1].legend()
plt.tight_layout()
plt.show()


# ---------- 7. High-bias scenario: build (q, k) where outliers align ----------
# 같은 좌표 · 같은 부호의 outlier 가 있는 (q, k) → <q, k> 가 매우 큼
# → Stage-1 quant 가 그 진폭을 centroid 쪽으로 깎음 (systematic shrink, biased)
# → 잘려나간 양 = ||k|| · <m·q, r>  (= 정확히 bias 의 크기)
# 정렬 안된 (EASY) 페어는 <q, k> 자체가 작아 잘려나갈 것도 거의 없음.
def lloyd_max_1d(samples, n_levels, n_iter=200, tol=1e-9):
    s = np.asarray(samples).flatten()
    if n_levels == 1:
        return np.array([s.mean()]), np.array([])
    qs = (np.arange(n_levels) + 0.5) / n_levels
    centroids = np.quantile(s, qs)
    for _ in range(n_iter):
        bnds = (centroids[:-1] + centroids[1:]) / 2
        idx = np.searchsorted(bnds, s)
        new = np.array([s[idx == i].mean() if np.any(idx == i) else centroids[i]
                        for i in range(n_levels)])
        if np.max(np.abs(new - centroids)) < tol:
            centroids = new; break
        centroids = new
    return centroids, (centroids[:-1] + centroids[1:]) / 2

# Stage-1: 2-bit Lloyd-Max (b_mse = 2 → 4 centroids)
n_levels        = 4
centroids, bnds = lloyd_max_1d(y.flatten(), n_levels)

# Target key: 첫 번째 row.  outlier 가 박힌 두 좌표를 찾아둔다.
k_t         = k[0, 0]
k_t_norm    = np.linalg.norm(k_t)
outlier_idx = np.argsort(np.abs(k_t))[-2:]
outlier_sgn = np.sign(k_t[outlier_idx])

# Stage-1 dequantize on y[0, 0]  -> residual r_t (projected space)
y_t      = y[0, 0]
codes_t  = np.searchsorted(bnds, y_t)
y_dq_t   = centroids[codes_t]
r_t      = y_t - y_dq_t
norm_r_t = np.linalg.norm(r_t)

# 두 query: HARD (정렬), EASY (다른 좌표에 outlier)
rng       = np.random.default_rng(7)
q_hard    = rng.standard_normal(D)
q_hard[outlier_idx] = outlier_sgn * rng.uniform(15, 20, size=2)     # 같은 좌표·같은 부호

other_idx = np.setdiff1d(np.arange(D), outlier_idx)
easy_idx  = rng.choice(other_idx, size=2, replace=False)
q_easy    = rng.standard_normal(D)
q_easy[easy_idx] = rng.choice([-1, 1], size=2) * rng.uniform(15, 20, size=2)

scenarios = [('HARD  (q,k outliers aligned)', q_hard),
             ('EASY  (outliers on different coords)', q_easy)]

# 분해:  <q, k> = ||k|| · <m·q, dequantized_y>     (Stage-1, biased)
#                + ||k|| · <m·q, r_t>               (= -bias, missing piece)
print('=' * 78)
print(f'Stage-1 (b_mse=2 bit, {n_levels} levels)  decomposition for target k[0,0]')
print(f'  ||k_t|| = {k_t_norm:.2f},  ||r_t|| = {norm_r_t:.4f}  '
      f'(residual norm: scenario-independent)')
print('=' * 78)
print(f'                                            true        Stage-1     '
      f'residual ip   |bias|')
results = []
for lab, q in scenarios:
    mq       = m @ q
    true_ip  = q @ k_t
    s1_ip    = (mq @ y_dq_t) * k_t_norm
    res_ip   = (mq @ r_t)    * k_t_norm                  # = true - stage1 = -bias
    results.append((lab, mq, true_ip, s1_ip, res_ip))
    print(f'  {lab:42s}  {true_ip:+9.2f}   {s1_ip:+9.2f}   '
          f'{res_ip:+9.2f}   {abs(s1_ip-true_ip):7.2f}')
print('=' * 78)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
for ax, (lab, mq, true_ip, s1_ip, res_ip) in zip(axes, results):
    bias = s1_ip - true_ip
    bars = ['true  <q, k>',
            'Stage-1 est\n||k||*<m.q, dequant>',
            'residual ip\n||k||*<m.q, r>']
    vals = [true_ip, s1_ip, res_ip]
    cols = ['gray', 'C1', 'C2']
    ax.bar(bars, vals, color=cols, edgecolor='black')
    ax.axhline(0, color='black', lw=0.6)
    ax.set_title(f'{lab}\nbias = Stage1 - true = {bias:+.2f}'
                 f'   |   residual = {res_ip:+.2f}')
    ax.set_ylabel('inner product')
    ax.tick_params(axis='x', labelsize=9)

fig.suptitle('step 7.  Aligned outliers -> large <q,k> -> Stage-1 shrinks it -> '
             'residual ip ||k||*<m.q, r> carries the missing piece (= -bias)',
             fontsize=11)
plt.tight_layout()
plt.show()


# ---------- 8. QJL on residual: sketch alone looks random, but mean(sketch * q_proj) ----------
# 잔차 r_t (projected space) 와 query 측 (m·q) 에 같은 Gaussian projection G 를 걸어서:
#   sketch_i = sign(G_i^T · r_t)         <- 키 측에 1 bit 씩 저장 (key 만으로 결정)
#   q_proj_i = G_i^T · (m · q)            <- query 시점에 즉석 계산 (full-precision)
# 한 항의 곱  sketch_i * q_proj_i  은 (X = G_i·m·q,  Y = G_i·r_t) 가 joint Gaussian 이라
#   E[X · sign(Y)] = sqrt(2/pi) * <m·q, r_t> / ||r_t||
# 이 평균값을 ||r_t|| · ||k|| · sqrt(pi/2) 배 하면 정확히 ||k||·<m·q, r_t> = -bias.
# 핵심:
#   (1) sketch 자체는 그냥 ±1 noise 처럼 보임 (q 와 무관, key 만으로 결정).
#   (2) HARD 는 <m·q, r_t> 가 큼  -> mean(sketch * q_proj) 가 0 에서 멀어짐.
#   (3) EASY 는 <m·q, r_t> 가 작음 -> 같은 평균이 0 근처에서 진동.
m_proj = 4096
G      = rng.standard_normal((m_proj, D))

sketch     = np.sign(G @ r_t)                        # [m_proj]   ±1
mq_hard    = m @ q_hard
mq_easy    = m @ q_easy
qproj_hard = G @ mq_hard                             # [m_proj]   continuous
qproj_easy = G @ mq_easy
prod_hard  = sketch * qproj_hard
prod_easy  = sketch * qproj_easy

sqrt_2_pi      = np.sqrt(2 / np.pi)
sqrt_pi_over_2 = np.sqrt(np.pi / 2)

# E[ mean(sketch * q_proj) ]  =  sqrt(2/pi) * <m·q, r_t> / ||r_t||
target_mean_hard = (mq_hard @ r_t) / norm_r_t * sqrt_2_pi
target_mean_easy = (mq_easy @ r_t) / norm_r_t * sqrt_2_pi

# 최종 QJL 추정 (||r||·||k||·sqrt(pi/2)·mean)  ≈  ||k||·<m·q, r>  (= -bias)
est_hard = norm_r_t * k_t_norm * sqrt_pi_over_2 * prod_hard.mean()
est_easy = norm_r_t * k_t_norm * sqrt_pi_over_2 * prod_easy.mean()

# step 7 의 참 residual ip
res_ip_hard = (mq_hard @ r_t) * k_t_norm
res_ip_easy = (mq_easy @ r_t) * k_t_norm

print('=' * 78)
print(f'QJL recovery of residual ip   (m_proj={m_proj},  G ~ N(0, I_D))')
print('=' * 78)
print(f'                            mean(sketch*q_proj)    target       '
      f'QJL est       true res ip')
print(f'  HARD                      {prod_hard.mean():+9.4f}        '
      f'{target_mean_hard:+9.4f}    {est_hard:+8.2f}      {res_ip_hard:+8.2f}')
print(f'  EASY                      {prod_easy.mean():+9.4f}        '
      f'{target_mean_easy:+9.4f}    {est_easy:+8.2f}      {res_ip_easy:+8.2f}')
print('=' * 78)

# Visualization
fig = plt.figure(figsize=(14, 8.5))
gs  = fig.add_gridspec(4, 1, height_ratios=[0.4, 0.4, 0.4, 2.4], hspace=0.7)

n_show = min(m_proj, 256)                            # 처음 256 개만 시각화 (가독성)
qmax   = max(abs(qproj_hard[:n_show]).max(), abs(qproj_easy[:n_show]).max())

# Strip 1: sketch
ax = fig.add_subplot(gs[0])
ax.imshow(sketch[:n_show].reshape(1, -1), aspect='auto', cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_yticks([]); ax.set_xticks([])
ax.set_title(f'sketch = sign(G @ r_t)   (length {m_proj}, showing first {n_show})  '
             '... pure +/-1 noise, depends only on key',
             fontsize=10, loc='left')

# Strip 2: q_projected HARD
ax = fig.add_subplot(gs[1])
ax.imshow(qproj_hard[:n_show].reshape(1, -1), aspect='auto',
          cmap='RdBu_r', vmin=-qmax, vmax=qmax)
ax.set_yticks([]); ax.set_xticks([])
ax.set_title('q_projected HARD = G @ (m * q_hard)   '
             '... continuous, also looks Gaussian',
             fontsize=10, loc='left')

# Strip 3: q_projected EASY
ax = fig.add_subplot(gs[2])
ax.imshow(qproj_easy[:n_show].reshape(1, -1), aspect='auto',
          cmap='RdBu_r', vmin=-qmax, vmax=qmax)
ax.set_yticks([])
ax.set_title('q_projected EASY = G @ (m * q_easy)   '
             '... also Gaussian, no visible difference vs HARD by eye',
             fontsize=10, loc='left')
ax.set_xlabel('projection index')

# Bottom: running mean (the pattern that emerges from the elementwise product)
ax = fig.add_subplot(gs[3])
xs           = np.arange(1, m_proj + 1)
running_hard = np.cumsum(prod_hard) / xs
running_easy = np.cumsum(prod_easy) / xs
ax.plot(xs, running_hard, color='C3', lw=1.6,
        label=f'HARD  running mean(sketch * q_proj)   '
              f'->  target {target_mean_hard:+.3f}   '
              f'(QJL est = {est_hard:+.2f}, true res ip = {res_ip_hard:+.2f})')
ax.plot(xs, running_easy, color='C0', lw=1.6,
        label=f'EASY  running mean(sketch * q_proj)   '
              f'->  target {target_mean_easy:+.3f}   '
              f'(QJL est = {est_easy:+.2f}, true res ip = {res_ip_easy:+.2f})')
ax.axhline(target_mean_hard, color='C3', ls='--', lw=1, alpha=0.6)
ax.axhline(target_mean_easy, color='C0', ls='--', lw=1, alpha=0.6)
ax.axhline(0, color='black', lw=0.6)
ax.set_xlabel('# projections used  (m_proj cumulative)')
ax.set_ylabel('mean(sketch * q_proj)')
ax.set_title('mean(sketch * q_proj)  ->  sqrt(2/pi) * <m.q, r_t> / ||r_t||     '
             '(HARD large, EASY ~ 0)',
             fontsize=11)
ax.legend(loc='best', fontsize=9)
ax.grid(alpha=0.3)

fig.suptitle('step 8.  sketch alone is +/-1 noise; '
             'elementwise product with q_proj reveals correlation -> recovers residual ip',
             fontsize=12)
plt.show()

