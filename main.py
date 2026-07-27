import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MultipleLocator

from simluate_gen import draw_multi_pickup

UP_COUNT = 2 # 抽取角色数量
RUN_TIMES = 10000 # 模拟次数


result_old = []
result_new = []

for i in range(RUN_TIMES):
    result_new.append(draw_multi_pickup(UP_COUNT, True))
    result_old.append(draw_multi_pickup(UP_COUNT, False))

np_old = np.array(result_old)
np_new = np.array(result_new)

# np.save('np_old.npy', np.array(np_old, dtype=np.int64))
# np.save('np_new.npy', np.array(np_new, dtype=np.int64))
# quit()

# np_old = np.load('np_old.npy', mmap_mode='r')
# np_new = np.load('np_new.npy', mmap_mode='r')

plt.rcParams["font.family"] = "SimHei"


def plot_cumulative_prob(data1, data2, max_pulls):
    pulls = np.arange(0, max_pulls + 1)

    prob1 = [np.mean(data1 <= p) for p in pulls]
    prob2 = [np.mean(data2 <= p) for p in pulls]

    plt.figure(figsize=(12, 6))
    plt.plot(pulls, prob1, label="旧机制", linewidth=2, color="#1f77b4")
    plt.plot(pulls, prob2, label="新机制", linewidth=2, color="#ff7f0e")

    plt.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="50% 参考线")

    plt.xlabel("抽取数量", fontsize=12)
    plt.ylabel("概率", fontsize=12)
    plt.title(f"抽取 {UP_COUNT} 位角色，模拟 {RUN_TIMES} 次", fontsize=14)
    plt.legend()
    ax = plt.gca()
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    plt.grid(alpha=0.3)
    plt.xlim(0, max_pulls)
    plt.ylim(0, 1)

    median1 = np.median(data1)
    mean1 = np.mean(data1)
    median2 = np.median(data2)
    mean2 = np.mean(data2)
    stats_text = f"旧机制：中位数 = {median1:.1f} 抽，平均数 = {mean1:.1f} 抽\n" f"新机制：中位数 = {median2:.1f} 抽，平均数 = {mean2:.1f} 抽"
    plt.text(
        0.95,
        0.1,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(
            boxstyle="round",
            facecolor="white",
            alpha=0.8,
            edgecolor="gray",
        ),
    )  # 使用轴域坐标
    plt.savefig(f"Figure_{UP_COUNT}_{RUN_TIMES}.png", dpi=300)
    plt.show()


paint_x_max = max(np.max(i) for i in [np_old, np_new])
print(paint_x_max)
plot_cumulative_prob(np_old, np_new, paint_x_max)
