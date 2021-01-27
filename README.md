# spectrs

Программное обеспечение для анализа спектров люминесценции

Программа написана на языке программирования Python 3. В ней использовались библиотеки OpenCV2, для чтения изображения пленки и библиотека Matplotlib для построения графиков и вычисления длин волн. На вход программы подается изображение формата .BMP, для корректного считывания яркости каждого пикселя. Затем пользователь обозначает исследуемые границы изображения и начальную длину волны выбранного интервала. В программе имеется словарь вида пиксель-длинна волны. На основании полученного ранее от пользователя начальной длинны волны, программа отсекает часть словаря, не используемая для вывода результата, и интерполирует значения методом Лагранжа. Исходное изображение так же кадрируется до нужных пределов и вычисляется среднее арифметическое значение каждого столбца пикселей изображения для определения средней относительной яркости пикселя, чтобы уменьшить влияние шумов на изображении. Интерполированное значение длинны волны от пикселя сопоставляется с каждым пикселем исследуемой части изображения. Таким образом, суть работы программы на данном этапе такова: из исследуемого изображения последовательно берутся пиксели и сопоставляются интерполированному значению пиксель-длина волны, каждая полученная таким образом пара пиксель-длинна волны записываются в массив. После чего полученная база значений выводится в виде графика, где по оси ординат представленная относительная яркость пикселя, а по оси абсцисс – длинна волны в ангстремах. Построение графиков с помощью библиотеки Matplotlib так же позволяет отмечать на графике длину волны точечно, а также масштабировать полученный график.

**Пример результата работы программы:**
![Image alt](https://github.com/shixw-null/spectrs/blob/main/expamle.png)


**Инструкция** 
Нв вход программе дается скан пленки в формате .BMP, затем необходимо выбрать область исследования спектра, путем двойного нажатия левой, затем правой клавишей мыши в разных краях будущей прямоугольной области, чтобы получить белую рамку прямоугольника. При необходимости - повторить действия. Если выбранная область устраивает - необходимо нажать в английской раскаладке клавишу "a" на клавиатуре. Затем в консоле выбрать начальную точку исследования спектра и увидеть график- результат работы программы. На нем ,двойным кликом, можно размещать вертикальные подписи с длинной волны , а так же менять масштаб и сохранять график.
