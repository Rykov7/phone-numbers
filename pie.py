import matplotlib.pyplot as plt
from matplotlib import rcParams


def make_plot(filename, title, valid, dubbed, errors=0):
    """ Строит круговой график и сохраняет в PNG. """
    # data
    x = [valid, dubbed, errors]
    valid_percent = round(valid / (sum(x) / 100))
    dubbed_percent = round(dubbed / (sum(x) / 100))
    errors_percent = round(errors / (sum(x) / 100))

    colors = ['#52a756', '#2c9aef', '#e51c24']

    labels = f'Номера ({valid_percent}%)', f'Повторные ({dubbed_percent}%)', f'Некорректные ({errors_percent}%)'

    # plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(x, colors=colors, radius=1, startangle=90, counterclock=False,
           normalize=True,
           wedgeprops={"linewidth": 3, "edgecolor": "white", 'width': 0.5}, frame=False)

    ax.legend(labels, facecolor='red', bbox_to_anchor=(.75, .8), bbox_transform=fig.transFigure,
              labelcolor='#59595b', fontsize=9, markerfirst=True, borderpad=0,
              edgecolor=rcParams["axes.edgecolor"], frameon=False, handleheight=1.0
              )
    ax.axis('equal')
    ax.set_title(title, loc='left', fontdict={'fontsize': 9, 'color': '#59595b'})
    plt.savefig(f'{filename}[plot].png')


if __name__ == '__main__':
    make_plot('numbers.csv', 1955, 300, 250)
    plt.show()
    # plt.savefig('result.png')