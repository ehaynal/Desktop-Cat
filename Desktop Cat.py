from PIL import Image, ImageTk
import tkinter as tk # Python 3
import random
import ctypes
import keyboard

root = tk.Tk()
root.title('Cat :)')

# The image must be stored to Tk or it will be garbage collected.
# Load the sprite sheet image with transparency
sprite_sheet_path = "cat_sprite_sheet.png"
sprite_sheet = Image.open(sprite_sheet_path)

# Define the sprite frame size (width and height)
frame_width = 32
frame_height = 32

# Extract individual frames from the sprite sheet
animations = []
for j in range(sprite_sheet.height // frame_height):
	frames = []
	for i in range(sprite_sheet.width // frame_width):
		x = i * frame_width
		y = j * frame_height  # Assuming the animation is in the top row of the sprite sheet
		frame_image = sprite_sheet.crop((x, y, x + frame_width, y + frame_height))
		frame_image = frame_image.resize((128, 128), Image.Resampling.BOX)
		frames.append(frame_image)
	animations.append(frames)

for i in [0,1,2,3,6]:
	animations[i] = animations[i][:4]
for i in [4,5,9]:
	animations[i] = animations[i][:8]
for i in [7,8]:
	animations[i] = animations[i][:i-1]
animations.append([elm.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for elm in animations[4]])
animations.append([elm.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for elm in animations[5]])
frame0 = ImageTk.PhotoImage(animations[0][0])

def clicked(*args):
	root.after_cancel(next_id)
	paw(clicked=True)

def on_mouse_down(event):
	global delta
	delta = 0
	root.after_cancel(animation_loop_id)
	root.after_cancel(next_id)
	root.after_cancel(motion_loop_id)
	frame_image = ImageTk.PhotoImage(animations[8][2])
	label.config(image=frame_image)
	label.image = frame_image  # Store the image reference to prevent garbage collection
	label.bind("<B1-Motion>", on_mouse_drag)
	label.bind("<ButtonRelease-1>", on_mouse_up)

def on_mouse_drag(event):
	root.geometry(f'+{root.winfo_pointerx()-60}+{root.winfo_pointery()-75}')

def on_mouse_up(event):
	label.unbind("<B1-Motion>")
	label.unbind("<ButtonRelease-1>")
	root.after(10,fall())

label = tk.Label(root, image=frame0, bg='white')
label.focus_set()  # Set focus on the label to enable mouse events
label.bind("<Button-2>", lambda event: root.destroy())  # Bind click event to close the window
label.bind("<Button-3>", clicked)
label.bind("<Button-1>", on_mouse_down)

frame_time = 200
current_animation = animations[0]
delta = 0
frame_index = 0
next_id = None
animation_loop_id = None
motion_loop_id = None

def handle_motion():
	global motion_loop_id
	x = root.winfo_x()
	y = root.winfo_y()
	new_x = x+delta
	if new_x >= root.winfo_screenwidth():
		new_x = -128
	elif new_x <= -128:
		new_x = root.winfo_screenwidth()
	if y+root.winfo_height() != root.winfo_screenheight():
		y = root.winfo_screenheight()-root.winfo_height()
	root.geometry(f'+{new_x}+{y}')
	motion_loop_id = root.after(frame_time, handle_motion)

def animate():
	global frame_index
	global animation_loop_id
	frame_image = ImageTk.PhotoImage(current_animation[frame_index])
	label.config(image=frame_image)
	label.image = frame_image  # Store the image reference to prevent garbage collection
	frame_index = (frame_index + 1) % len(current_animation)
	animation_loop_id = root.after(frame_time, animate)

def switch_animation(new_animation_index):
	global current_animation
	global frame_index
	current_animation = animations[new_animation_index]
	frame_index = 0

def walk_right():
	switch_animation(4)
	global delta
	global frame_time
	global next_id
	delta = 10
	frame_time = 100
	subseq = random.choice([run_right,idle,idle,idle])
	duration = random.randint(5,10)
	next_id = root.after(1000*duration,subseq)

def walk_left():
	switch_animation(10)
	global delta
	global frame_time
	global next_id
	delta = -10
	frame_time = 100
	subseq = random.choice([run_left,idle,idle,idle])
	duration = random.randint(5,10)
	next_id = root.after(1000*duration,subseq)

def run_right():
	switch_animation(5)
	global delta
	global frame_time
	global next_id
	delta = 30
	frame_time = 100
	subseq = random.choice([walk_right,idle])
	duration = random.randint(4,7)
	next_id = root.after(1000*duration,subseq)

def run_left():
	switch_animation(11)
	global delta
	global frame_time
	global next_id
	delta = -30
	frame_time = 100
	subseq = random.choice([walk_left,idle])
	duration = random.randint(4,7)
	next_id = root.after(1000*duration,subseq)

def idle():
	idle_choice = random.randint(0,1)
	switch_animation(idle_choice)
	global delta
	global frame_time
	global next_id
	delta = 0
	frame_time = 200
	subseq = random.choice([walk_right,walk_left,lick])
	duration = random.randint(5,10)
	next_id = root.after(1000*duration,subseq)

def lick():
	switch_animation(2)
	global delta
	global frame_time
	global next_id
	delta = 0
	frame_time = 200
	subseq = random.choice([wipe,idle])
	duration = random.randint(5,10)
	next_id = root.after(1000*duration,subseq)

def wipe():
	switch_animation(3)
	global delta
	global frame_time
	global next_id
	delta = 0
	frame_time = 200
	subseq = random.choice([lick,idle,sleep])
	duration = random.randint(5,10)
	next_id = root.after(1000*duration,subseq)

def paw(clicked=False):
	switch_animation(7)
	global delta
	global frame_time
	global next_id
	delta = 0
	frame_time = 100
	subseq = random.choice([walk_right,walk_left])
	duration = random.randint(5,10)
	if clicked:
		duration = 1.5
	next_id = root.after(int(1000*duration),subseq)

def sleep():
	switch_animation(6)
	global delta
	global frame_time
	global next_id
	delta = 0
	frame_time = 400
	subseq = random.choice([lick,wipe,sleep])
	duration = random.randint(5,10)
	next_id = root.after(1000*duration,subseq)

def fall():
	if root.winfo_y() < root.winfo_screenheight()-132:
		frame_image = ImageTk.PhotoImage(animations[8][3])
		label.config(image=frame_image)
		label.image = frame_image  # Store the image reference to prevent garbage collection
		root.geometry(f'+{root.winfo_x()}+{root.winfo_y()+10}')
		root.after(10,fall)
	else:
		root.after(100,land)

def land():
	root.geometry(f"+{root.winfo_x()}+{root.winfo_screenheight()-132}")
	handle_motion()
	animate()
	idle()	

root.overrideredirect(True)
root.geometry(f"+250+{root.winfo_screenheight()-132}")
root.lift()
root.wm_attributes("-topmost", True)
#root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")
root.resizable(False,False)
label.pack()

def bring_to_front():
	# Get the window handle
	hwnd = ctypes.windll.user32.GetForegroundWindow()
	# Bring the window to the front, including above the taskbar
	ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0003)
	root.lift()

def win_key_handler():
	root.after(1000,bring_to_front)

keyboard.add_hotkey('windows',win_key_handler)

bring_to_front()
handle_motion()
animate()
next_id = root.after(0, idle)



root.mainloop()