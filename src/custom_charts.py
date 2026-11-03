import flet_charts as fch
import flet as ft
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
                                                                                       color=ft.Colors.WHITE
                                                                                   )
                                                                                   )))

    line = fch.LineChartData(color=ft.Colors.BLUE_GREY_300,
                             curved=False,
                             points=points)

    axis_labels = []
    for h in range(0, 24, 3):
        label_text = f"{h:02d}:00"
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

                          ))

    return chart
