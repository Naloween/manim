from manim import *
from typing import Iterable
from pynput.keyboard import Key, Listener
import copy

class Player:
    def __init__(self, sequences: list, fullscreen=False, ThreeD = False):
        # Set manim config to show window
        config.renderer = RendererType.OPENGL
        config.write_to_movie = False
        config.preview = True

        config.fullscreen = fullscreen

        if ThreeD:
            self.scene = ThreeDScene()
        else:
            self.scene = Scene()
        self.sequences = sequences
        self.sequences_state = {}
        self.running = False
        self.current_sequence = 0
        self.play_sequences = [0]

        # Inputs

        def on_press(key):
            if key == Key.right:
                if self.current_sequence < len(self.sequences)-1:
                    self.current_sequence = self.current_sequence+1
                    self.play_sequences.append(self.current_sequence)

            elif key == Key.left:
                if self.current_sequence > 0:
                    self.current_sequence = self.current_sequence-1
                    self.play_sequences.append(self.current_sequence)


        def on_release(key):
            if key == Key.esc:
                self.running = False

        # Collect events until released
        self.listener = Listener(
                on_press=on_press,
                on_release=on_release,
                )
    
    def run(self):

        self.running = True
        self.listener.start()

        while self.running:
            if len(self.play_sequences) > 0:
                playing_sequence = self.play_sequences[0]
                self.play_sequences = self.play_sequences[1:]

                if len(self.play_sequences) > 0:
                    continue

                if playing_sequence < len(self.sequences) and playing_sequence > -1:
                    sequence_state = self.sequences_state.get(playing_sequence)

                    if sequence_state is None:
                        sequence_state = self.get_scene_state()
                        self.sequences_state[playing_sequence] = sequence_state
                    self.restore_scene_state(sequence_state)
                    self.sequences[playing_sequence](self)
                else:
                    self.running = False

        self.listener.stop()

    def find_mobj_by_name(self, name):
        for mobj in self.scene.mobjects:
            if mobj.name == name:
                return mobj
        return None
    
    def play(
        self,
        *args: Animation | Iterable[Animation],
        subcaption=None,
        subcaption_duration=None,
        subcaption_offset=0,
        **kwargs,
    ):
        self.scene.play(*args, subcaption=subcaption, subcaption_duration=subcaption_duration, subcaption_offset=subcaption_offset, **kwargs)
    
    def clear(self):
        self.scene.clear()
    
    def get_scene_state(self):
        return copy.deepcopy([
            self.scene.ambient_light,
            self.scene.animations,
            self.scene.camera_target,
            self.scene.foreground_mobjects,
            self.scene.last_t,
            self.scene.meshes,
            self.scene.mobjects,
            self.scene.moving_mobjects,
            self.scene.static_mobjects,
            self.scene.point_lights,
            self.scene.widgets,
            ])

    def restore_scene_state(self, state):
            state = copy.deepcopy(state)
            self.scene.ambient_light = state[0]
            self.scene.animations = state[1]
            self.scene.camera_target = state[2]
            self.scene.foreground_mobjects = state[3]
            self.scene.last_t = state[4]
            self.scene.meshes = state[5]
            self.scene.mobjects = state[6]
            self.scene.moving_mobjects = state[7]
            self.scene.static_mobjects = state[8]
            self.scene.point_lights = state[9]
            self.scene.widgets = state[10]
