from sys import path

path.append('./project/')

from my_tk_theme import dft_theme, dark_theme, set_color_t
import tkinter as tk
from functools import partial, wraps
from typing import Any
from my_util.util import limit_concurrency

class Scrollbar(tk.Frame):

    def __init__(self,*args, command=None, width=15, height=15, orient='vertical', modifier='' , **kwargs) -> None:
        super().__init__(*args, width= width, height=height, **kwargs)
        sb = tk.Scale(self, showvalue=False, bg='red', highlightthickness=0, troughcolor=self['bg'], borderwidth=0, width=5, sliderlength=60, sliderrelief='flat', command=command)
        decrease_btn = tk.Button(self,anchor='n',  font='-size 8', borderwidth=0, command= lambda: sb.set(value = sb.get()-1), repeatdelay=sb['repeatdelay'], repeatinterval=sb['repeatinterval'])
        increase_btn = tk.Button(self,anchor='s', font='-size 8', borderwidth=0, command=lambda: sb.set(sb.get()+1), repeatdelay=sb['repeatdelay'], repeatinterval=sb['repeatinterval'])
        self.wheel_tag= 'weel tag of ' + self._w
        self.internal_whell_tag= internal_class_tag= 'internal wheel tag of ' + self._w
        self.bindtags(tagList= self.bindtags()+(internal_class_tag,))
        sb.bindtags(tagList= sb.bindtags()+(internal_class_tag,))
        decrease_btn.bindtags(tagList= decrease_btn.bindtags()+(internal_class_tag,))
        increase_btn.bindtags(tagList= increase_btn.bindtags()+(internal_class_tag,))
        self.bind_class(internal_class_tag, f"<{modifier}MouseWheel>", self.__on_mousewheel)
        self.sb = sb
        self.modifier = modifier
        self.decrease_btn = decrease_btn
        self.increase_btn = increase_btn
        self.__set_orient(orient)

    def bind_external_mousewheel(self):
        self.bind_class(self.wheel_tag, f"<{self.modifier}MouseWheel>", self.__on_mousewheel)

    def unbind_external_mousewheel (self):
        self.unbind_class(self.wheel_tag, f"<{self.modifier}MouseWheel>")

    def __set_orient(self, orient):
        self.sb.config(orient= orient)
        self.update()
        if orient == 'vertical':
            self.decrease_btn.config(text=' △', font= '-size 8 -weight normal', anchor='center')#▲  -weight bold
            self.increase_btn.config(text=' ▽', font= '-size 8 -weight normal', anchor='center')#▼
            self.decrease_btn.place(anchor='nw', height=15, width=15)
            self.increase_btn.place(anchor='sw', height=15, width=15, rely=1)
            self.sb.place(anchor='w', x=5, rely=0.5, width=5)#, height=self.winfo_height()-34)
        else:
            self.decrease_btn.config(text='◁', font= '-weight normal', anchor='center')#◀-size 8 
            self.increase_btn.config(text='▷', font= '-weight normal', anchor='center')#▶-size 8
            self.decrease_btn.place(y=0, height=15, width=15)#anchor='nw',
            self.increase_btn.place(anchor='ne', y=0, height=15, width=15, relx=1)
            self.sb.place(anchor='n', y=5, relx=0.5)#, height=5, width=self.winfo_width()-34)

    def configure(self, cnf : dict[str,Any]=None, *args: Any, **kwds: Any) -> Any:
        if cnf:
            kwds.update(cnf)
        for k, v in kwds.copy().items():
            match k:
                case 'bg' | 'background':
                    self.decrease_btn.config(bg = v)
                    self.increase_btn.config(bg = v)
                    self.sb.config(troughcolor = v)
                case 'fg' | 'forground':
                    self.decrease_btn.config(fg = v)
                    self.increase_btn.config(fg = v)
                    self.sb.config(bg = v)
                    kwds.pop(k)
                case 'activebackground':
                    self.decrease_btn.config(activebackground = v)
                    self.config(activebackground = v)
                    self.sb.config(activebackground = v)
                    kwds.pop(k)
                case 'activeforeground':
                    self.decrease_btn.config(activeforeground = v)
                    self.increase_btn.config(activeforeground = v)
                    kwds.pop(k)
                case 'height':
                    self.sb.config(length = v-34)
                case 'command':
                    self.sb.config(command = v)
                    kwds.pop(k)
                case 'sliderlength':
                    if v > 1:
                        self.sb.config(sliderlength = v)
                    else:
                        self.sb.update()
                        if self.sb['orient']=='vertical':
                            self.sb.config(sliderlength= int(v * self.sb.winfo_height()))
                        else:
                            #self.sb.config(sliderlength= int(v * self.sb.winfo_width()))
                            self.sb.config(sliderlength= v * self.sb.winfo_width())
                    kwds.pop(k)
                case 'to':
                    self.sb.config(to = v)
                    #self.sb.__setattr__('to', v)
                    kwds.pop(k)
                case 'from_':
                    self.sb.config(from_ = v)
                    kwds.pop(k)
        super().configure(*args,**kwds)
    
    config = configure

    def __setitem__(self, key, value):
        self.configure(cnf={key: value})
    
    def __getitem__(self, key: str) -> Any:
        match key:
            case 'fg' | 'foreground':
                return self.decrease_btn[key]
            case 'activebackground':
                return self.decrease_btn[key]
            case 'activeforeground':
                return self.decrease_btn[key]
            case 'command':
                return self.sb[key]
            case 'sliderlength':
                return self.sb[key]
            case 'to':
                return self.sb[key]
            case 'from_':
                return self.sb[key]
        return super().__getitem__(key)


    @wraps(tk.Place.place_configure)
    def place_config(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.__update_sb()
        self['height'] = self.winfo_height()
        self['width'] = self.winfo_width()

    place = place_config
    
    @wraps(tk.Pack.pack_configure)
    def pack_configure(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.__update_sb()
        self['height'] = self.winfo_height()
        self['width'] = self.winfo_width()

    pack = pack_configure

    def __update_sb(self):
        self.update_idletasks()
        if self.sb['orient'] == 'vertical':
            self.sb.place(height= self.winfo_height()-34)
        else:
            self.sb.place(width= self.winfo_width()-34)
    
    def set_color_t(self, t: dft_theme):
        self['bg']=t.bg_color
        self.sb.config(bg=t.w_bg_disable_color, troughcolor=t.bg_color, activebackground=t.w_bg_select_color)
        set_color_t(self.decrease_btn, t=t, use=(t.bg_color, t.bg_color, False, t.w_bg_select_color, t.bg_color, t.w_bg_active_color))
        set_color_t(self.increase_btn, t=t, use=(t.bg_color, t.bg_color, False, t.w_bg_select_color, t.bg_color, t.w_bg_active_color))
        def __internal_color_set(*_,up_fg,down_fg,sb_bg):
            self.decrease_btn.config(fg=up_fg),
            self.increase_btn.config(fg=down_fg),
            self.sb.config(bg=sb_bg)
            return
        self.bind('<Enter>', partial(__internal_color_set, up_fg=t.w_bg_enable_color, down_fg=t.w_bg_enable_color, sb_bg=t.w_bg_enable_color))
        self.bind('<Leave>', partial(__internal_color_set, up_fg=t.bg_color, down_fg=t.bg_color, sb_bg=t.w_bg_disable_color))
        self.sb.bind('<Button-1>', lambda _: self.sb.config(activebackground=t.w_bg_active_color))
        self.sb.bind('<ButtonRelease-1>', lambda _: self.sb.config(activebackground=t.w_bg_select_color))

    def __on_mousewheel(self, event: tk.Event):
        if not self.modifier and event.state not in [0,2,8,10]:
            return
        self.sb.set(self.sb.get()-1*(event.delta/10))

class Scrollframe(tk.Frame):

    __prev_dimension = [0,0]

    def __init__(self, master : tk.Misc= None, smaller : list[bool,bool]= [False, False], wall_offset : list = [20, 20], **kwargs) -> None:
        self.smaller = smaller
        self.wall_offset = wall_offset

        super().__init__(master, **kwargs)
        self.visible_area_frame= visible_area_frame = self
        
        if 'width' in kwargs:
            if smaller[1]:
                kwargs.pop('width')
            else:
                kwargs['width'] = max(0,kwargs['width']-wall_offset[0] * 2)
        if 'height' in kwargs:
            if smaller[0]:
                kwargs.pop('height')
            else:
                kwargs['height'] = max(0,kwargs['height']-wall_offset[1] * 2)

        main_frame= tk.Frame(visible_area_frame, cnf= kwargs)
        self.main_frame = main_frame
        main_frame.place(x= wall_offset[0], y= wall_offset[1])
        self.CHILD_BINDTAG= child_binding = 'child of ' + main_frame._w
        self.bind('<Configure>', self.__set_scrollbar_visibility)
        main_frame.bind('<Configure>', self.__set_scrollbar_visibility)
        main_frame.bind_all('<Map>' , self.__tag_as_child)
        main_frame.bind_class(child_binding, '<Map>', self.__incremente_frame)
        main_frame.bind_class(child_binding, '<Configure>', self.__resize_frame)
        main_frame.bind_class(child_binding, '<Unmap>', self.__resize_frame)

        scrollbar_y = Scrollbar(visible_area_frame, command= lambda x: main_frame.place(y = self.wall_offset[1] - int(x)))
        scrollbar_x = Scrollbar(visible_area_frame, orient= 'horizontal', modifier='Control-', command= lambda x: main_frame.place(x = self.wall_offset[0] - int(x)))
        main_frame.bindtags(main_frame.bindtags() + (scrollbar_y.wheel_tag,scrollbar_x.wheel_tag))
        self.scrollbar_y = scrollbar_y
        self.scrollbar_x = scrollbar_x

    def __tag_as_child(self, e: tk.Event):
        w: tk.Widget = e.widget
        if w == self.main_frame:
            return
        if self.main_frame._w in w._w:
                if self.CHILD_BINDTAG not in w.bindtags():
                    w.bindtags(w.bindtags()+(self.CHILD_BINDTAG,))
                    self.__incremente_frame(e=e)
    
    def __incremente_frame(self, e : tk.Event):
        w: tk.Widget = e.widget
        width= w.winfo_x() + w.winfo_width()
        height = w.winfo_y() + w.winfo_height()
        minx = self.winfo_width() - self.wall_offset[0] * 2 if not self.smaller[0] else 0
        miny = self.winfo_height() - self.wall_offset[1] * 2 if not self.smaller[1] else 0
        self.main_frame.update()
        self.main_frame.place(width= max(minx, width, self.main_frame.winfo_width()), height= max(miny, height, self.main_frame.winfo_height()))

    def __resize_frame(self, *_):
        minx = self.winfo_width() - self.wall_offset[0] * 2 if not self.smaller[0] else 0
        miny = self.winfo_height() - self.wall_offset[1] * 2 if not self.smaller[1] else 0
        width, height = 0, 0
        for w in self.main_frame.winfo_children():
            if w.winfo_ismapped():
                width = max(width, w.winfo_x() + w.winfo_width())
                height = max(height, w.winfo_y() + w.winfo_height())
        self.main_frame.place(width= max(minx,width), height= max(miny,height))

    @limit_concurrency(1)
    def __set_scrollbar_visibility(self, e: tk.Event):
        if e.width == self.__prev_dimension[0] and e.height == self.__prev_dimension[1]:
            return
        self.__prev_dimension[0] = e.width
        self.__prev_dimension[1] = e.height
        max_height= self.winfo_height() - self.wall_offset[1] * 2
        max_width= self.winfo_width() - self.wall_offset[0] * 2
        c_height= self.main_frame.winfo_height()
        c_width= self.main_frame.winfo_width()
        if c_height > max_height:
            if not self.scrollbar_y.winfo_ismapped():
                """if not self.scrollbar_x.winfo_ismapped():
                    self.scrollbar_y.place(anchor='ne', relx=1 , x=-2, y=2, height=self.winfo_height()-4)
                else:
                    self.scrollbar_x.place(width = self.scrollbar_x.winfo_width()-17)
                    self.scrollbar_y.place(anchor='ne', relx=1 , x=-2, y=2, height=self.winfo_height()-21)"""
                if self.scrollbar_x.winfo_ismapped():
                    self.scrollbar_x.place(width = self.scrollbar_x.winfo_width()-17)
                a=tk.Frame(self, bg='red')
                a.place(anchor='ne', relx=1, width= 17 , relheight=1)
                a.lower(self.scrollbar_y)
                self.scrollbar_y.place(anchor='ne', relx=1 , x=-2, y=2, height=self.winfo_height()-4)
                self.__tag_mf_child(self.scrollbar_y.wheel_tag)
                self.scrollbar_y.bind_external_mousewheel()
            self.scrollbar_y['to'] = c_height - max_height
            self.scrollbar_y['sliderlength'] = max_height/c_height
        elif self.scrollbar_y.winfo_ismapped():
            self.scrollbar_y.place_forget()
            self.scrollbar_y.unbind_external_mousewheel()
            if self.scrollbar_x.winfo_ismapped():
                self.scrollbar_x.place(width = self.scrollbar_x.winfo_width()+17)
        if c_width > max_width:
            if not self.scrollbar_x.winfo_ismapped():
                if not self.scrollbar_y.winfo_ismapped():
                    self.scrollbar_x.place(anchor='sw', rely=1 , x=2, y=-2, width=self.winfo_width()-4)
                else:
                    self.scrollbar_x.place(anchor='sw', rely=1 , x=2, y=-2, width=self.winfo_width()-21)
                """else:
                    self.scrollbar_y.place(height= self.scrollbar_y.winfo_height()-17)
                    self.scrollbar_x.place(anchor='sw', rely=1 , x=2, y=-2, width=self.winfo_width()-21)"""
                self.__tag_mf_child(self.scrollbar_x.wheel_tag)
                self.scrollbar_x.bind_external_mousewheel()
            self.scrollbar_x['to'] = c_width - max_width
            self.main_frame.update()
            self.scrollbar_x['sliderlength'] = max_width/c_width
        elif self.scrollbar_x.winfo_ismapped():
            self.scrollbar_x.place_forget()
            self.scrollbar_x.unbind_external_mousewheel ()
            """if self.scrollbar_y.winfo_ismapped():
                self.scrollbar_y.place(height= self.scrollbar_y.winfo_height()+17)"""
            
    def __tag_mf_child(self, tag: str, widget: tk.Widget = None):
        if not widget:
            widget = self.main_frame
        for w in widget.winfo_children():
            if tag not in w.bindtags():
                w.bindtags(w.bindtags()+(tag,))
            if w.winfo_children():
                self.__tag_mf_child(tag, w)
        
    def set_color_t(self, t: dft_theme):
        self.config(bg= t.bg_color)
        self.main_frame.config(bg= t.bg_color)
        self.scrollbar_y.set_color_t(t)
        self.scrollbar_x.set_color_t(t)
        
class head_bar(tk.Frame):
    
    def __init__ (self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.bind('<Button-1>', self.startMove)
        self.bind('<B1-Motion>', self.moving)
        exit_btn = tk.Button(self, text=' X ', bg=self.__THEME.head_bar_color, fg='white', borderwidth=0, activebackground='red', activeforeground='black', font=('helvetica neue', 13), cursor='hand2', command= self.exit)
        exit_btn.bind('<Enter>', lambda _: exit_btn.config(bg='red'))
        exit_btn.bind('<Leave>', lambda _: exit_btn.config(bg=self.__THEME.head_bar_color))
        exit_btn.pack(side='right', padx=1, pady=1)
        title = tk.Label(head_bar, text='directory selector', fg='white', bg=self.__THEME.head_bar_color, font=('calibri', 11))
        title.pack(side='left', padx=5)
        head_bar.place(anchor='nw', height=self.__HEAD_BAR_HEIGHT, width=self.__FRAME_WIDTH)

    def startMove(self, event: tk.Event):
        self.master.x = event.x
        self.master.y = event.y

    def moving(self, event: tk.Event):
        x = (event.x_root - self.master.x)
        y = (event.y_root - self.master.y)
        self.master.geometry(f'+{x}+{y}')

if __name__ == '__main__':
    def change_state(w:tk.Widget):
        if w.winfo_ismapped():
            w.place_forget()
        else:
            w.place(x=0 if w.winfo_x() == 0 else x, y=0 if w.winfo_y() == 0 else y, width=w.winfo_width(), height= w.winfo_height())

    def move(delta, axe):
        global x, y 
        active= 1 if hv_label.winfo_ismapped() else 0
        if axe == 'x':
            x+=delta
            active+= 2 if h_label.winfo_ismapped() else 0
            if active>1:
                h_label.place(x=x)
            if active%2 == 1:
                hv_label.place(x=x)
        if axe == 'y':
            y+=delta
            active+= 2 if v_label.winfo_ismapped() else 0
            if active>1:
                v_label.place(y=y)
            if active%2 == 1:
                hv_label.place(y=y)
    
    test= tk.Tk('test')
    test.geometry('300x400')
    test.config(bg='gray10')
    mf= Scrollframe(test, width=300, height=300, bg='red')
    mf.set_color_t(dark_theme)
    mf.place(anchor='sw', rely=1)
    h_label= tk.Label(mf.main_frame, text='◀ ▶')
    v_label= tk.Label(mf.main_frame, text='▲\n▼')
    hv_label= tk.Label(mf.main_frame, text='▲\n◀ ▶\n▼')
    #left_btn= tk.Button(test, text='◀', repeatdelay=1, repeatinterval=4, command= lambda : (h_label.place(x=h_label.winfo_x()-1) if h_label.winfo_ismapped() else None, hv_label.place(x=h_label.winfo_x()-1) if hv_label.winfo_ismapped() else None))
    left_btn= tk.Button(test, text='◀', repeatdelay=1, repeatinterval=4, command= partial(move, delta=-1, axe='x'))
    right_btn= tk.Button(test, anchor='center', text='▶', repeatdelay=1, repeatinterval=4, command= partial(move, delta=+1, axe='x'))
    #right_btn= tk.Button(test, text='▶', command= lambda : (h_label.place(x=h_label.winfo_x()+1), hv_label.place(x=h_label.winfo_x()+1)))
    up_btn= tk.Button(test, text='▲', repeatdelay=1, repeatinterval=4, command= partial(move, delta=-1, axe='y'))
    down_btn= tk.Button(test, text='▼', repeatdelay=1, repeatinterval=4, command= partial(move, delta=+1, axe='y'))
    up_btn.place(x=35, y=10, width=20, height=20)
    down_btn.place(x=35, y=60, width=20, height=20)
    left_btn.place(x=10, y=35, width=20, height=20)
    right_btn.place(x=60, y=35, width=20, height=20)
    x, y = 25, 25
    #x, y = 25, 300
    h_label.place(x=x, y=0, width=40, height=20)
    v_label.place(x=0, y=y, width=20, height=40)
    hv_label.place(x=x, y=y, width=40, height=40)
    h_btn=tk.Button(test, text='◀ ▶', command=partial(change_state, w=h_label))
    v_btn=tk.Button(test, text='▲\n▼', command=partial(change_state, w=v_label))
    hv_btn=tk.Button(test, text='▲\n◀ ▶\n▼', command=partial(change_state, w=hv_label))
    h_btn.place(x=130, y=10, height=20, width=40)
    v_btn.place(x=100, y=40, height=40, width=20)
    hv_btn.place(x=130, y=40, height=40, width=40)
    test.mainloop()