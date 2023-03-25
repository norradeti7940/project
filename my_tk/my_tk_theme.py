from tkinter import Widget


class dft_theme():

    bg_color = None
    cf_color = None
    w_bg_enable_color = None
    w_fg_enable_color = None
    w_bg_disable_color = None
    w_fg_disable_color = None
    w_bg_select_color = None
    w_fg_select_color = None
    w_bg_active_color = None
    w_fg_active_color = None
    text_color = None
    text_font = None
    head_bar_color = None
    head_bar_font = None


class dark_theme (dft_theme):

    bg_color = '#202020'
    cf_color = 'gray20'
    w_bg_enable_color = 'gray35'
    w_fg_enable_color = 'gray85'
    w_bg_disable_color = 'gray10'
    w_fg_disable_color = 'gray60'
    w_bg_select_color = 'gray25'
    w_fg_select_color = 'gray75'
    w_bg_active_color = 'gray17'
    w_fg_active_color = 'gray67'
    text_color = 'white'
    text_font = 'calibri'
    head_bar_color = 'gray7'
    head_bar_font = 'calibri'


def set_color_t(w: Widget, t: dft_theme, use: tuple = None, enable: bool = True):
    '''
        bg = None, fg = None, bg_selected = None, fg_selected = None, bg_active = None, fg_active = None
    '''
    val = {'bg': t.w_bg_enable_color if enable else t.w_bg_disable_color,
           'fg': t.w_fg_enable_color if enable else t.w_fg_disable_color,
           'bg_selected': t.w_bg_select_color,
           'fg_selected': t.w_fg_select_color,
           'bg_active': t.w_bg_active_color,
           'fg_active': t.w_fg_active_color}
    if use:
        for c, v in zip(use, val.copy()):
            if c != True:
                if not c:
                    del val[v]
                else:
                    val[v] = c
    set_color(w, **val)


def set_color(w: Widget, bg=None, fg=None, bg_selected=None, fg_selected=None, bg_active=None, fg_active=None):
    cfn = dict()
    if bg:
        cfn['bg'] = bg
    if fg:
        cfn['fg'] = fg
    if bg_active:
        cfn['activebackground'] = bg_active
    if fg_active:
        cfn['activeforeground'] = fg_active
    w.configure(cfn)
    if bg_selected or fg_selected:
        _before = [None, None]
        w.bind('<Enter>', lambda _: (on_enter(w, bg_selected, fg=fg_selected, result=_before)))
        w.bind('<Leave>', lambda _: w.config(bg=_before[0], fg=_before[1]))


def on_enter(w: Widget, bg, fg, result):
    _bg, _fg = w['bg'], w['fg']
    w.config(bg=bg, fg=fg)
    result[0] = _bg if bg else None
    result[1] = _fg if fg else None
