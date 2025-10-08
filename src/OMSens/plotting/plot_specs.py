class PlotSpecs():
    def __init__(self, setup_specs, lines_specs):
        self.setup_specs = setup_specs
        self.lines_specs = lines_specs


class PlotSetupSpecs():
    def __init__(self, title, subtitle, footer, x_label, y_label, extra_ticks):
        self.title       = title
        self.subtitle    = subtitle
        self.footer      = footer
        self.x_label     = x_label
        self.y_label     = y_label
        self.extra_ticks = extra_ticks


class PlotLineSpecs():
    def __init__(self, df, x_var, y_var, linewidth, linestyle, markersize, marker, label, color):
        self.df         = df
        self.x_var      = x_var
        self.y_var      = y_var
        self.linewidth = linewidth
        self.linestyle  = linestyle
        self.markersize = markersize
        self.marker     = marker
        self.label      = label
        self.color      = color
