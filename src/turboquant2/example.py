"""
TurboQuant - k에 RHT 적용 + QJL(1-bit) 양자화 과정 시각화

핵심:
  - k in R^D, ||k||=1 이면 k의 각 좌표는 (1 - x^2)^((D-3)/2) ~ shifted/scaled Beta((D-1)/2,(D-1)/2)
  - RHT  m = (1/sqrt(D)) * H @ diag(s),  H: Hadamard, s ~ Rademacher
  - m 은 직교행렬:  m^T m = I
  - outlier 가 있는 k 를 L2 정규화 후 m 을 곱하면 outlier 에너지가 모든 좌표로 퍼져 Beta 분포를 따름

QJL (Quantized Johnson-Lindenstrauss, Zandieh et al. 2024):
  - 키는 1-bit 부호 양자화:  c_k = sign(m @ k)
  - 쿼리는 풀-프리시전 투영:   y_q = m @ q
  - 내적 추정:   <q, k> ≈ ||k|| * sqrt(pi/(2D)) * <y_q, c_k>
  - 근거: (a, b) ~ N(0, Σ) 이면 E[a sign(b)] = sqrt(2/π) σ_a ρ
          RHT 출력 좌표가 Beta 분포(≈Gaussian)이므로 위 관계가 근사적으로 성립
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


# ---------- 7. QJL: 1-bit sign quantization of  m @ k_norm ----------
# 저장: 부호 비트  c_k = sign(m @ k_norm)  (1 bit/coord)  +  스칼라  ||k||
c_k = np.sign(y).astype(np.float64)            # shape [B, L, D]  in {-1, +1}
k_norms = np.linalg.norm(k, axis=-1)           # [B, L]   원본 k 노름 (스케일 복원용)

fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
vmax_y = np.abs(y).max()
im0 = axes[0].imshow(y[0], aspect='auto', cmap='RdBu_r', vmin=-vmax_y, vmax=vmax_y)
axes[0].set_title('continuous projection   m @ k_norm')
axes[0].set_ylabel('L')
plt.colorbar(im0, ax=axes[0])

im1 = axes[1].imshow(c_k[0], aspect='auto', cmap='RdBu_r', vmin=-1, vmax=1)
axes[1].set_title('step 7.  QJL 1-bit code   sign(m @ k_norm)')
axes[1].set_xlabel('D'); axes[1].set_ylabel('L')
plt.colorbar(im1, ax=axes[1])
plt.tight_layout()
plt.show()


# ---------- 8. QJL 내적 추정:  <q, k> ≈ ||k|| sqrt(pi/(2D)) <m q, sign(m k_norm)> ----------
# 모든 (i, j) 쌍에 대해 true vs estimated inner product 비교
# query 는 풀-프리시전 투영(원본 스케일), key 는 1-bit 부호코드 + 노름 스칼라만 저장
K   = k[0]                                       # [L, D]  원본 (outlier 포함)
mQ  = np.einsum('ij,lj->li', m, K)               # [L, D]  쿼리측: 원본 q 의 풀-프리시전 투영
cK  = c_k[0]                                     # [L, D]  키측: sign(m @ k_norm) 1-bit
nrm = k_norms[0]                                 # [L]     키 노름 ||k|| (스케일 복원)

scale = np.sqrt(np.pi / (2.0 * D))
inner_qjl  = scale * nrm[None, :] * (mQ @ cK.T)         # [L_q, L_k]   QJL 추정
inner_true = K @ K.T                                     # [L_q, L_k]   참값 <q, k>

err_abs = np.abs(inner_qjl - inner_true)
rel_err = np.linalg.norm(inner_qjl - inner_true) / np.linalg.norm(inner_true)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
vmax_ip = np.abs(inner_true).max()
im0 = axes[0].imshow(inner_true, cmap='RdBu_r', vmin=-vmax_ip, vmax=vmax_ip)
axes[0].set_title('true   <k_i, k_j>')
plt.colorbar(im0, ax=axes[0])

im1 = axes[1].imshow(inner_qjl, cmap='RdBu_r', vmin=-vmax_ip, vmax=vmax_ip)
axes[1].set_title('step 8.  QJL estimate')
plt.colorbar(im1, ax=axes[1])

axes[2].scatter(inner_true.flatten(), inner_qjl.flatten(),
                s=12, alpha=0.6, edgecolor='k', linewidth=0.3)
lo, hi = inner_true.min(), inner_true.max()
axes[2].plot([lo, hi], [lo, hi], 'r--', lw=1.5, label='y = x')
axes[2].set_xlabel('true  <k_i, k_j>')
axes[2].set_ylabel('QJL  estimate')
axes[2].set_title(f'rel. err  = {rel_err:.3f}')
axes[2].legend(); axes[2].grid(alpha=0.3)
plt.tight_layout()
plt.show()


# ---------- 9. QJL 분산 vs 투영차원 m_proj  (m_proj 키울수록 추정 분산 감소) ----------
# JL 차원을 D 보다 크게 잡으려면 가우시안 행렬 S in R^{m_proj x D} 사용
# (RHT 는 정확히 D x D 직교행렬이라 차원 변경 불가)
m_list = [64, 128, 256, 512, 1024, 2048]
n_trials = 20

# 단위벡터 두 개의 참 내적값 = cos(theta)
Kn_mat = k_norm[0]                              # [L, D]  단위벡터
true_cos_pairs = (Kn_mat @ Kn_mat.T)            # [L, L]
mask = ~np.eye(L, dtype=bool)
true_vals = true_cos_pairs[mask]                # 모든 비대각 쌍

mse_curve = []
for m_proj in m_list:
    errs = []
    for t in range(n_trials):
        # rows ~ N(0, I_D / m_proj)  =>  ||S k||^2 ≈ ||k||^2  (JL 평균 보존)
        S = np.random.randn(m_proj, D) / np.sqrt(m_proj)
        Sk = Kn_mat @ S.T                        # [L, m_proj]
        cSk = np.sign(Sk)                        # 1-bit code
        # 추정자:  <q,k> ≈ sqrt(pi/(2 m_proj)) * ||k|| * <S q, sign(S k)>
        # 단위벡터이므로 ||k||=1, 같은 S 를 쿼리에도 사용
        est = np.sqrt(np.pi / (2.0 * m_proj)) * (Sk @ cSk.T)
        errs.append((est[mask] - true_vals) ** 2)
    mse_curve.append(np.mean(errs))

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.loglog(m_list, mse_curve, 'o-', label='empirical MSE  (avg over pairs/trials)')
# 이론: Var ~ C / m_proj  (1/m 감소)
c_fit = mse_curve[0] * m_list[0]
ax.loglog(m_list, [c_fit / mp for mp in m_list], 'r--',
          label=r'$\propto 1/m_{proj}$  reference')
ax.set_xlabel(r'projection dim  $m_{proj}$')
ax.set_ylabel(r'MSE of  $\widehat{\langle q,k \rangle}$')
ax.set_title('step 9.  QJL variance decreases as 1 / m_proj')
ax.grid(True, which='both', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()


# ---------- 10. 콘솔 요약 ----------
print('='*60)
print('QJL property check')
print('='*60)
print(f'D            = {D}')
print(f'#pairs       = {L*L}')
print(f'rel. L2 err  = {rel_err:.4f}    (RHT projection, 1-bit keys)')
print(f'mean |err|   = {err_abs.mean():.4f}')
print(f'max  |err|   = {err_abs.max():.4f}')
print(f'storage/key  : {D} bits + 1 float (||k||)   vs  {D} floats original')
print('='*60)
