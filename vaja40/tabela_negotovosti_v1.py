# made with heart by Gregor Zunic

from sympy import *
import matplotlib.pyplot as plt
from decimal import Decimal
import pandas as pd
from IPython.display import display, Latex, HTML

# todo
# adding custom latex names


class Negotovost:
    def __init__(self, data, function, floating_points=3):
        self.data = data
        self.function = sympify(function)
        self.floating_points = floating_points
        self.results = []
        self.formated_results = []
        self.vrednost_f = 0
        self.final_error = 0

    def __str__(self):
        return (str(self.data))

    def format_text(self, num):
        if num % 1 == 0:
            return num
        return str(f'%.{self.floating_points}E' % num).replace('+', '')

    def calculate_error(self):
        if not self.vrednost_f:
            values = [(x[0], x[1]) for x in self.data]

            for el in self.data:
                if el[2]:
                    deriv = Derivative(self.function, el[0])
                    res = deriv.doit()
                    deltaa = el[2]
                    error = (float(deriv.doit().subs(values) * deltaa))
                    latfunc = '$'+latex(res)+'$'
                    self.results.append((latfunc, deltaa, error))
                    self.formated_results.append(
                        (latfunc, self.format_text(deltaa), self.format_text(error)))

            self.vrednost_f = float(self.function.doit().subs(values))

            self.final_error = sqrt(
                sum([abs(float(x[2])**2) for x in self.results]))

        return (self.vrednost_f, self.final_error)

    def draw_table(self, variable='v', text_size=15, title='', units="", display_img=False):
        self.variable = variable
        self.text_size = text_size
        self.title = title

        self.calculate_error()

        columns = [r'$\frac{\partial %s}{\partial x_i}$' % self.variable,
                   r'$\sigma_i$', r'$\sigma_i \cdot \frac{\partial %s}{\partial x_i}$' % self.variable]
        rows = ['$'+latex(sympify(x[0]))+'$' for x in self.data if x[2]]

        latex_vrednost = self.format_text(self.vrednost_f)
        latex_error = self.format_text(self.final_error)
        final_output = r'$'+self.variable + \
            ' = (' + latex_vrednost + ' \pm ' + \
            latex_error + r") \:" + units + '$'
        final_function = '$'+self.variable+'=' + latex(self.function)+'$'

        if not display_img:

            #columns = [Math(x) for x in columns]
            #rows = [Math(x) for x in rows]
            format_results = [[latex(x) for x in y]
                              for y in self.formated_results]

            #print(columns, rows, format_results)

            make_bigger = HTML(
                '<style>table.dataframe{font-size: %dpx;}</style>' % text_size)
            display(make_bigger)
            pd.set_option('display.max_colwidth', None)
            df = pd.DataFrame(format_results, columns=columns, index=rows)

            display(Latex(final_function))
            display(df)
            display(Latex(final_output))

        else:
            print(latex_vrednost, '+-', latex_error)
            if self.title:
                plt.title(self.title)

            plt.xticks([])
            plt.yticks([])

            plt.subplots_adjust(left=0.03, bottom=0, right=0.97, top=0.94)

            plt.axis('off')

            table = plt.table(cellText=self.formated_results, loc='center left',
                              rowLabels=rows, colLabels=columns)

            plt.text(0.35, 0.9, final_function, fontsize=self.text_size+5)
            table.set_fontsize(self.text_size)
            table.scale(1.5, 2.5)
            table.auto_set_font_size(False)

            plt.text(0.02, 0.1, final_output, fontsize=self.text_size+4)

            plt.show()
