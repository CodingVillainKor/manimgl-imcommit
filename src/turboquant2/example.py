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

