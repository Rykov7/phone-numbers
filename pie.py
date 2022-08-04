""" Модуль pie.py построение круговой диаграммы. """


def make_plot(filename, title, valid, dubbed, errors=None):
    """ Строит круговую диаграмму и сохраняет в PNG. """
    import matplotlib.pyplot as plt
    from colored import bg, attr

    # data
    if errors is not None:
        x = [valid, dubbed, errors]
        labels = f'Номера ({valid})', f'Повторы ({dubbed})', f'Мусор ({errors})'
    else:
        x = [valid, dubbed]
        labels = f'Номера ({valid})', f'Повторы ({dubbed})'

    colors = ['#52a756', '#e51c24', '#a9a9ab']

    # plot
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.pie(x, colors=colors, radius=1, startangle=90, counterclock=False,
           normalize=True,
           wedgeprops={"linewidth": 3, "edgecolor": "white", 'width': 0.5}, frame=False)

    ax.legend(labels, bbox_to_anchor=(.75, .6), bbox_transform=fig.transFigure,
              labelcolor='#59595b', fontsize=9,
              frameon=False, handleheight=2.6,

              )
    ax.axis('equal')
    ax.set_title(title, loc='center', fontdict={'fontsize': 9, 'color': '#59595b'})

    plt.savefig(filename)
    print(f'{bg("blue")}[СОХРАНЕНО] График {filename}{attr("reset")}')


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from colored import bg, attr
    make_plot('numbers.png', 'numbers.csv', 1955, 300, 50)
    plt.show()
    # plt.savefig('result.png')