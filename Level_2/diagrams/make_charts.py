import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/claude/elvo-python-programming-internship-program/Level_2/diagrams/"
BLUE, RED, AMBER, GREY, GREEN = "#2f6fdb", "#d64545", "#e0a21b", "#8a94a6", "#2e9e6b"
plt.rcParams.update({"font.size": 13, "axes.spines.top": False, "axes.spines.right": False})

# data from the inventory demo
names = ["USB Cable", "Keyboard", "Milk 1L", "Yoghurt"]
qty = [35, 4, 20, 12]
price = [5.99, 29.50, 1.40, 0.90]
status = ["OK", "LOW STOCK", "EXPIRES SOON", "EXPIRED"]
col = {"OK": GREEN, "LOW STOCK": RED, "EXPIRES SOON": AMBER, "EXPIRED": GREY}
colors = [col[s] for s in status]

# 1. stock levels
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(names, qty, color=colors)
ax.axhline(5, color=RED, ls="--", lw=1.5)
ax.set_xlim(-0.6, 4.2); ax.text(3.5, 5.6, "low-stock\nthreshold (5)", color=RED, ha="left", va="bottom", fontsize=11)
for b, s, q in zip(bars, status, qty):
    ax.text(b.get_x() + b.get_width() / 2, max(q, 5) + 0.8, f"{q}\n{s}", ha="center", fontsize=11)
ax.set_ylim(0, 46); ax.set_ylabel("Units in stock")
ax.set_title("Inventory stock levels and alerts", fontweight="bold", loc="left")
fig.tight_layout(); fig.savefig(OUT + "inventory_stock_levels.png", dpi=200, facecolor="white")

# 2. value share
value = [q * p for q, p in zip(qty, price)]
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(names[::-1], value[::-1], color=[BLUE] * 4)
for b, v in zip(bars, value[::-1]):
    ax.text(v + 3, b.get_y() + b.get_height() / 2, f"${v:,.2f}", va="center")
ax.set_xlim(0, max(value) * 1.2); ax.set_xlabel("Stock value ($)")
ax.set_title(f"Inventory value by product (total ${sum(value):,.2f})", fontweight="bold", loc="left")
fig.tight_layout(); fig.savefig(OUT + "inventory_value.png", dpi=200, facecolor="white")

# 3. organizer before/after
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 7))
def draw(ax, title, lines, c):
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.02, 0.97, title, fontsize=15, fontweight="bold", color=c, va="top")
    for i, (txt, kind) in enumerate(lines):
        color = {"d": BLUE, "f": "#222", "n": GREEN}[kind]
        ax.text(0.04, 0.88 - i * 0.068, txt, family="monospace", fontsize=12, color=color,
                va="top", fontweight="bold" if kind == "d" else "normal")
draw(a, "BEFORE", [("downloads/", "d"), ("  report.pdf", "f"), ("  photo.jpg", "f"), ("  notes.txt", "f"),
                   ("  notes.txt   <- same name", "f"), ("  budget.xlsx", "f"), ("  README", "f")], RED)
draw(b, "AFTER", [("downloads/", "d"), ("  pdf/", "d"), ("    report.pdf", "f"), ("  jpg/", "d"), ("    photo.jpg", "f"),
                  ("  txt/", "d"), ("    notes.txt", "f"), ("    notes_1.txt  <- kept, not overwritten", "n"),
                  ("  xlsx/", "d"), ("    budget.xlsx", "f"), ("  no_extension/", "d"), ("    README", "f")], GREEN)
fig.suptitle("File organizer: sorted by extension, nothing overwritten", fontweight="bold", fontsize=15, x=0.02, ha="left")
fig.tight_layout(); fig.savefig(OUT + "organizer_before_after.png", dpi=200, facecolor="white")
