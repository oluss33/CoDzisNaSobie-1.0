import flet_charts as fch
import flet as ft
import datetime

from flet import Offset


def create_chart(hourly_temps):
    points = []
    for i in range(len(hourly_temps)):
        hour = f"{i:02d}:00"
        temp = f"{hourly_temps[i]}°C"

        points.append(fch.LineChartDataPoint(x=i, y=hourly_temps[i],
                                             tooltip=fch.LineChartDataPointTooltip(text=f"{hour} : {temp}",
                                                                                   text_style=ft.TextStyle(
                                                                                       size=16,
                                                                                       weight=ft.FontWeight.BOLD,
                                                                                       color=ft.Colors.WHITE,
                                                                                       shadow=ft.BoxShadow(
                                                                                           spread_radius=1,
                                                                                           blur_radius=4,
                                                                                           color=ft.Colors.BLACK,
                                                                                           offset=Offset(0, 0),
                                                                                       )
                                                                                   )
                                                                                   )))

    line = fch.LineChartData(color=ft.Colors.BLUE_GREY_300,
                             curved=False,
                             points=points)

    axis_labels = []
    for h in range(0, 24, 3):
        label_text = f"{int(h):02d}:00"
        axis_labels.append(
            fch.ChartAxisLabel(
                value=h,
                label=ft.Text(label_text, size=10, color=ft.Colors.GREY_400)
            )
        )

    bottom_axis = fch.ChartAxis(
        labels=axis_labels,
    )

    chart = fch.LineChart(data_series=[line], width=500, height=150, bottom_axis=bottom_axis,
                          tooltip=fch.LineChartTooltip(
                              bgcolor=ft.Colors.TRANSPARENT,
                              fit_inside_horizontally=True,
                              fit_inside_vertically=True
                          ))

    return chart

def create_bar_chart(precipitation):
    labels = []
    for h in range(0, 24, 3):
        label = fch.ChartAxisLabel(value=h, label=ft.Text(f"{h:02d}:00"))
        labels.append(label)

    groups = []
    for i in range(len(precipitation)):
        value = precipitation[i]


        rod = fch.BarChartRod(to_y = value, width=10)
        group = fch.BarChartGroup(x=i, rods=[rod])
        groups.append(group)

    max_y_value = max(precipitation) if precipitation else 0
    chart = fch.BarChart(
        width=1000,
        height=300,
        max_y = max(max_y_value * 1.2, 1), # 20% zapasu zeby slupek nie dotykal gornej krawedzi
        min_y = 0,
        bottom_axis=fch.ChartAxis(labels=labels, label_size=30),
        left_axis=fch.ChartAxis(label_size=50),
        groups=groups
    )

    return chart