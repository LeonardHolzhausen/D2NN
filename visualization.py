import dataset
from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self, image):
        self.image = image

    def visualize_image(self, label_name=None, ax=None):
        """Show a single dataset image, optionally with its class as a title.

        Pass an existing `ax` to draw into part of a larger figure (used by
        show_sample_grid below); omit it to display this image on its own.
        """

        standalone = ax is None
        if standalone:
            _, ax = plt.subplots()

        # vmin/vmax fixed to the binary range so the same code also works
        # once the generator produces grey edge pixels; "nearest" keeps
        # the individual pixels sharp at low resolutions like 16x16.
        ax.imshow(self.image, cmap="gray", vmin=0, vmax=1,
                  interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])

        if label_name is not None:
            ax.set_title(label_name, fontsize=10)

        # Only draw the window when this image is the whole figure --
        # otherwise the grid would pop up one window per subplot.
        if standalone:
            plt.show()


def show_sample_grid(samples, rows=2, cols=4):
    #Display several dataset samples at once, each labelled with its class.

    fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 3 * rows))

    for ax, sample in zip(axes.flat, samples):
        Visualizer(sample["image"]).visualize_image(
            label_name=sample["label_name"],
            ax=ax
        )

    # Hide any unused subplot slots if fewer samples than grid cells.
    for ax in axes.flat[len(samples):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = dataset.Dataset(8, image_size=16, seed=0).dataset

    show_sample_grid(data)