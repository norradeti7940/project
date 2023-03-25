from sys import path
path.append('./project/my_tk')

import tkinter as tk
from tkinter import filedialog
from ctypes import windll
from functools import partial
from typing import Tuple

from my_tk_theme import dark_theme, set_color_t
from my_tk_widget import Scrollbar


def dir_selector():
    app = tk.Tk()
    result = __dir_selector(master=app)
    app.mainloop()
    return result.dir


class __dir_selector:

    __RV_COORD: tuple[int] = (20, 600, 10, 80, 10, 80, 10, 50, 20)
    __RV_HEIGHT: int = 35
    __RV_DIST: int = 10
    __RV_WALLS_OFFSET = 10
    __FRAME_HEIGHT: int = 400
    __FRAME_WIDTH: int = sum(__RV_COORD)
    __CF_HEIGHT: int = 35
    __WINDOW_WIDTH: int = __FRAME_WIDTH
    __WINDOW_HEIGHT: int = __RV_HEIGHT + __FRAME_HEIGHT + __CF_HEIGHT
    __WINDOW_POS_X: int = 100
    __WINDOW_POS_Y: int = 100
    __HEAD_BAR_HEIGHT: int = 35
    __SCROLLBAR_WIDTH: int = 15
    __THEME = dark_theme

    class __root_voice:
        def __init__(self, label: tk.Label, add_btn: tk.Button, sub_btn: tk.Button, del_btn: tk.Button) -> None:
            self.label = label
            self.add_btn = add_btn
            self.sub_btn = sub_btn
            self.del_btn = del_btn

        def get_all(self) -> Tuple[tk.Label, tk.Button, tk.Button, tk.Button]:
            return (self.label, self.add_btn, self.sub_btn, self.del_btn)

        def delate(self) -> None:
            for temp in self.get_all():
                temp.destroy()
            del self

    def __init__(self, master: tk.Tk) -> None:
        # resolve dpi scaling problem
        windll.shcore.SetProcessDpiAwareness(1)

        # window parameter
        master.overrideredirect(1)
        master.geometry(f'{self.__WINDOW_WIDTH}x{self.__WINDOW_HEIGHT}+{self.__WINDOW_POS_X}+{self.__WINDOW_POS_Y}')
        master.resizable(False, False)
        self.master = master

        # head bar
        head_bar = tk.Frame(self.master, background=self.__THEME.head_bar_color)
        head_bar.bind('<Button-1>', self.startMove)
        head_bar.bind('<B1-Motion>', self.moving)
        exit_btn = tk.Button(head_bar, text=' X ', bg=self.__THEME.head_bar_color, fg='white', borderwidth=0, activebackground='red', activeforeground='black', font=('helvetica neue', 13), cursor='hand2', command= self.exit)
        exit_btn.bind('<Enter>', lambda _: exit_btn.config(bg='red'))
        #exit_btn.bind('<Enter>', partial(exit_btn.config, bg='red'))
        exit_btn.bind('<Leave>', lambda _: exit_btn.config(bg=self.__THEME.head_bar_color))
        exit_btn.pack(side='right', padx=1, pady=1)
        title = tk.Label(head_bar, text='directory selector', fg='white', bg=self.__THEME.head_bar_color, font=('calibri', 11))
        title.pack(side='left', padx=5)
        head_bar.place(anchor='nw', height=self.__HEAD_BAR_HEIGHT, width=self.__FRAME_WIDTH)

        #control frame
        cf = tk.Frame(self.master, bg=self.__THEME.cf_color)
        cf.place(anchor='sw', rely=1.0, width=self.__FRAME_WIDTH, height=self.__CF_HEIGHT)
        ok_btn= tk.Button(cf, text='OK', command= partial(self.exit, result=True))
        set_color_t(ok_btn, t=self.__THEME)
        ok_btn.pack(side='right', ipadx=15, padx=(10,20), pady=2)
        cancel_btn= tk.Button(cf, text='CANCEL', command= self.exit)
        set_color_t(cancel_btn, t=self.__THEME)
        cancel_btn.pack(side='right', ipadx=15, pady=2)

        # main fraim
        mf = tk.Frame(self.master, bg=self.__THEME.bg_color)
        mf.place(y=self.__HEAD_BAR_HEIGHT, width=self.__FRAME_WIDTH, height=self.__FRAME_HEIGHT)
        mf.lower(head_bar)
        mf.lower(cf)
        self.mf = mf
        
        a=Scrollbar(master=mf, height=self.__FRAME_HEIGHT)
        """def set_as_child(p,w):
            if p._w in w._w:
                bindtag='child of '+p._w
                if bindtag not in w.bindtags():
                    w.bindtags(w.bindtags()+(bindtag,))
        a.bind_all('<Map>',lambda _:set_as_child(a, _.widget))
        a.bind_class('child of '+a._w, '<1>', lambda _: print('a'))"""
        a.set_color_t(t=self.__THEME)
        #a.bind('<Configure>',lambda _: print('a'))
        #a.place(x=0,y=0,height=300)
        a.pack(side='right', pady=2, padx=(0,2))
        self.a=a
        #a.place(x=0,y=0)

        # scrollbar
        sb_frame = tk.Frame(mf, bg=self.__THEME.bg_color, height=self.__FRAME_HEIGHT, width=self.__SCROLLBAR_WIDTH)
        sb_frame.place(anchor='ne', relx=1, x=0)#self.__SCROLLBAR_WIDTH)
        sb = tk.Scale(sb_frame, showvalue=False, bg=self.__THEME.w_bg_disable_color, highlightthickness=0, troughcolor=self.__THEME.bg_color, activebackground=self.__THEME.w_bg_select_color, borderwidth=0, sliderrelief='flat', command=lambda x: self.place_voice(offset=int(x), update_sb=False))
        sb.place(anchor='w', x=4, rely=0.5, height=self.__FRAME_HEIGHT-40, width=5)
        up = tk.Button(sb_frame, text='△', font='-size 8 -weight bold', borderwidth=0, command=lambda: sb.set(sb.get()-1), repeatdelay=sb['repeatdelay'], repeatinterval=sb['repeatinterval'])
        set_color_t(up, t=self.__THEME, use=(self.__THEME.bg_color, self.__THEME.bg_color, False, self.__THEME.w_bg_select_color, self.__THEME.bg_color, self.__THEME.w_bg_active_color))
        up.place(anchor='nw',y=2, height=15, width=self.__SCROLLBAR_WIDTH)
        down = tk.Button(sb_frame, text='▽', font='-size 8 -weight bold', borderwidth=0, command=lambda: sb.set(sb.get()+1), repeatdelay=sb['repeatdelay'], repeatinterval=sb['repeatinterval'])
        set_color_t(down, t=self.__THEME, use=(self.__THEME.bg_color, self.__THEME.bg_color, False, self.__THEME.w_bg_select_color, self.__THEME.bg_color, self.__THEME.w_bg_active_color))
        down.place(anchor='sw', rely=1, y=-2, height=15,width=self.__SCROLLBAR_WIDTH)
        sb_frame.bind('<Enter>', lambda _: (
            up.config(fg=self.__THEME.w_bg_enable_color),
            down.config(fg=self.__THEME.w_bg_enable_color),
            sb.config(bg=self.__THEME.w_bg_enable_color)
        ))
        sb_frame.bind('<Leave>', lambda _: (
            up.config(fg=self.__THEME.bg_color),
            down.config(fg=self.__THEME.bg_color),
            sb.config(bg=self.__THEME.w_bg_disable_color)
        ))
        sb.bind('<Button-1>', lambda _: sb.config(activebackground=self.__THEME.w_bg_active_color))
        sb.bind('<ButtonRelease-1>', lambda _: sb.config(activebackground=self.__THEME.w_bg_select_color))
        self.sb = sb
        self.sb_frame = sb_frame
        self.sb_e = False

        # button
        self.gd_btn = tk.Button(master=mf, text='add dir', command=self.get_directory)
        set_color_t(self.gd_btn, self.__THEME)

        # class parameter
        self.root_voices:  list[__dir_selector.__root_voice] = []
        self.dir: dict[str, str] = dict()

        self.place_voice()

    def exit(self, *, result : bool = False):
        if not result:
            self.dir= None
        self.master.destroy()

    def get_directory(self):
        new_dir = filedialog.askdirectory()
        if not new_dir:
            return
        for dir in self.dir.copy():
            if dir in new_dir:
                return
        for voice in self.root_voices.copy():
            if new_dir in voice.label['text']:
                self.del_voice(voice)
        self.dir[new_dir] = None
        self.add_voice(new_dir)
        self.place_voice()

    def place_voice(self, offset: int = 0, update_sb: bool = True):
        if not self.root_voices:
            self.gd_btn.place(x=self.__FRAME_WIDTH//2, y=self.__FRAME_HEIGHT//2, anchor='center', height=self.__RV_HEIGHT)
            return
        l = len(self.root_voices)
        total_height = (l+1)*self.__RV_HEIGHT+l*self.__RV_DIST
        display_window = self.__FRAME_HEIGHT-2*self.__RV_WALLS_OFFSET
        y = (self.__FRAME_HEIGHT-total_height)//2
        if y < self.__RV_WALLS_OFFSET:
            y = self.__RV_WALLS_OFFSET-offset
            if not self.sb_e:
                self.sb_frame.place(x=0)
                self.sb_frame.bind_all("<MouseWheel>", self._on_mousewheel)
                self.sb_e = True
            if update_sb:
                self.master.update()
                self.sb.config(sliderlength=(self.__FRAME_HEIGHT-2*self.__RV_WALLS_OFFSET) * self.sb.winfo_height()/total_height, from_=0, to=total_height-display_window)
                self.sb.set(self.sb['to'])
        elif self.sb_e:
            self.sb_frame.place(x=self.__SCROLLBAR_WIDTH)
            self.sb_frame.unbind_all("<MouseWheel>")
            self.sb_e = False
        for voice in self.root_voices:
            lbl, add, sub, delb = voice.get_all()
            lbl.place(x=sum(self.__RV_COORD[:1]), y=y, width=self.__RV_COORD[1], height=self.__RV_HEIGHT)
            add.place(x=sum(self.__RV_COORD[:3]), y=y, width=self.__RV_COORD[3], height=self.__RV_HEIGHT)
            sub.place(x=sum(self.__RV_COORD[:5]), y=y, width=self.__RV_COORD[5], height=self.__RV_HEIGHT)
            delb.place(x=sum(self.__RV_COORD[:7]), y=y, width=self.__RV_COORD[7], height=self.__RV_HEIGHT)
            y += self.__RV_HEIGHT+self.__RV_DIST
        self.gd_btn.place(y=y, anchor='n', height=self.__RV_HEIGHT)

    def add_voice(self, dir: str):
        lab = tk.Label(master=self.mf, text=dir, font=(
            'Calibri', 9), anchor='w', relief='raised')
        add = tk.Button(master=self.mf, text='add child')
        sub = tk.Button(master=self.mf, text='sub child')
        delb = tk.Button(master=self.mf, text='del')
        set_color_t(lab, self.__THEME, use=(True, True, False, False))
        set_color_t(add, self.__THEME)
        set_color_t(sub, self.__THEME)
        set_color_t(delb, self.__THEME)
        new_root_voice = self.__root_voice(lab, add, sub, delb)
        delb.config(command=lambda: self.del_voice(new_root_voice))
        self.root_voices.append(new_root_voice)

    def del_voice(self, root_voice: __root_voice):
        self.root_voices.remove(root_voice)
        del self.dir[root_voice.label['text']]
        root_voice.delate()
        self.place_voice()

    def startMove(self, event: tk.Event):
        self.master.x = event.x
        self.master.y = event.y

    def moving(self, event: tk.Event):
        x = (event.x_root - self.master.x)
        y = (event.y_root - self.master.y)
        self.master.geometry(f'+{x}+{y}')

    def _on_mousewheel(self, event):
        self.sb.set(self.sb.get()-1*(event.delta/10))


if __name__ == '__main__':
    print(dir_selector())
    '''app = tk.Tk()
    __dir_selector(master=app)
    app.mainloop()'''
