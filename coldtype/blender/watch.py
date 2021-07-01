import bpy
from pathlib import Path
from runpy import run_path
import traceback

from coldtype.renderer.reader import SourceReader
from coldtype.blender import _walk_to_b3d

#from coldtype.blender.watch import watch; watch()

# original idea: https://blender.stackexchange.com/questions/15670/send-instructions-to-blender-from-external-application

class ColdtypeWatchingOperator(bpy.types.Operator):
    bl_idname = "wm.coldtype_watching_operator"
    bl_label = "Coldtype Watching Operator"

    _timer = None
    file = Path("~/.coldtype-blender.txt").expanduser()
    sr = None
    current_frame = -1

    def render_current_frame(self):
        for r, res in self.sr.frame_results(
            self.current_frame,
            class_filters=[r"^b3d_.*$"]
            ):
            print(">", r)
            _walk_to_b3d(res)

    def modal(self, context, event):
        if event.type == 'TIMER':
            if not self.file.exists():
                return {'PASS_THROUGH'}
            
            for line in self.file.read_text().splitlines():
                line = line.rstrip("\n")
                cmd,arg = line.split(",")
                if cmd == 'import':                    
                    try:
                        self.sr = SourceReader(arg)
                        self.sr.unlink()

                        def _frame_update_handler(scene):
                            if scene.frame_current != self.current_frame:
                                self.current_frame = scene.frame_current
                                self.render_current_frame()
                        
                        bpy.app.handlers.frame_change_post.clear()
                        bpy.app.handlers.frame_change_post.append(_frame_update_handler)
                        self.current_frame = bpy.context.scene.frame_current
                        self.render_current_frame()
                    
                    except Exception as e:
                        self.current_frame = -1
                        bpy.app.handlers.frame_change_post.clear()
                        stack = traceback.format_exc()
                        print("---"*10)
                        print(stack)
                    
                    print(f"ran {arg}")
                elif cmd == 'cancel':
                    self.cancel( context )
                else:
                    print('unknown request=%s arg=%s' % (cmd,arg))
            self.file.unlink()

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print('timer removed')

def register_watcher():
    bpy.utils.register_class(ColdtypeWatchingOperator)

def unregister_watcher():
    bpy.utils.unregister_class(ColdtypeWatchingOperator)

def watch():
    register_watcher()
    bpy.ops.wm.coldtype_watching_operator()