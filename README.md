# Knapsack-problem

Решение задачи о рюкзаке (с курса по Дискретной оптимизации на Coursera)

1) Формат ввода данных:

n W

v1 w1

v2 w2

...

n - число элементов

w - объем рюкзака

vi - цена i-ого элемента

wi - вес i-ого элемента

2) Формат вывода:

best_choice.value - итоговая цена заполненного рюкзака

Структура best_choice - Vertex:

def vertex_attributes(vrtx):

        print('Цена рюкзака: {}'.format(vrtx.value))

        print('Вес свободного места: {}'.format(vrtx.room))

        print('Оценка цены рюкзака: {}'.format(vrtx.estimate))
        
        print('Выбор элементов: {}'.format(vrtx.choice))
        
        print('Уровень дерева: {}'.format(vrtx.level))
        
        print('Конец дерева: {}'.format(vrtx.positive))
        
        print('Индекс левого сына: {}'.format(vrtx.lson_id))
        
        print('Индекс правого сына: {}'.format(vrtx.rson_id))
