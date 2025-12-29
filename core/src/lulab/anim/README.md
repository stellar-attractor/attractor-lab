# how the animation notebook should look like:

from anim.anim_defaults import *

fig, ax = make_fig()
ax.set_xlim(0, 14)
ax.set_ylim(-2.0, 0.7)

sc = ax.scatter([], [], s=3, alpha=0.15)

ani = animation.FuncAnimation(
    fig, update, frames=N_FRAMES, blit=True
)

save_anim(fig, ani, "ANIM_age_feh_boulet")