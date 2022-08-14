""" Module pie.py - build pie chart. """


def make_plot(filename, title, green, blue, grey=None):
    """ Build pie plot and save to PNG. """
    import matplotlib.pyplot as plt
    from colored import bg, attr

    # Data.
    if grey is not None:
        x = [green, blue, grey]
        labels = f'Номера ({green:,})', f'Повторы ({blue:,})', f'Мусор ({grey:,})'
    else:
        x = [green, blue]
        labels = f'Оригиналы ({green:,})', f'Пересечения ({blue:,})'

    colors = ['#52a756', '#e51c24', '#a9a9ab']

    # Plot.
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.pie(x, colors=colors, radius=1, startangle=90, counterclock=False,
           normalize=True,
           wedgeprops={"linewidth": 3, "edgecolor": "white", 'width': 0.5}, frame=False)

    ax.legend(labels, bbox_to_anchor=(.74, .6), bbox_transform=fig.transFigure,
              labelcolor='#59595b', fontsize=9,
              frameon=False, handleheight=2.0, handlelength=1.6, handletextpad=0.5,
              )
    ax.axis('equal')
    ax.set_title(title, loc='center', fontdict={'fontsize': 9, 'color': '#59595b'})

    plt.savefig(filename)
    print(f'{bg("dodger_blue_3")}[PNG] График {filename}{attr("reset")}')


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from colored import bg, attr
    make_plot('numbers.png', 'numbers.csv', 1955, 300, 50)
    plt.show()
