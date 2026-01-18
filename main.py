import tkinter as tk
import turtle
import colorsys

# ---------------- L-SYSTEM ENGINE ---------------- #

def expand_lsystem(axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        next_string = ""
        for symbol in current:
            next_string += rules.get(symbol, symbol)
        current = next_string
    return current


def parse_and_draw(t, commands, angle, step=5):
    stack = []
    length = len(commands)

    t.tracer(0, 0)
    t.penup()
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()

    for i, cmd in enumerate(commands):
        # Gradient color based on progress
        hue = i / length
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        t.pencolor(r, g, b)

        if cmd == "F":
            t.forward(step)
        elif cmd == "+":
            t.right(angle)
        elif cmd == "-":
            t.left(angle)
        elif cmd == "[":
            stack.append((t.position(), t.heading()))
        elif cmd == "]":
            pos, heading = stack.pop()
            t.penup()
            t.goto(pos)
            t.setheading(heading)
            t.pendown()

    turtle.update()


# ---------------- GUI LOGIC ---------------- #

def generate():
    t.clear()
    axiom = axiom_entry.get()
    rules_input = rules_entry.get()
    angle = float(angle_entry.get())
    iterations = int(iter_entry.get())

    rules = {}
    for rule in rules_input.split(","):
        key, value = rule.split(":")
        rules[key.strip()] = value.strip()

    result = expand_lsystem(axiom, rules, iterations)
    parse_and_draw(t, result, angle)


# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("L-System Fractal Architect")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10)

canvas = tk.Canvas(root, width=700, height=700)
canvas.pack(side=tk.RIGHT)

screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)
t.speed(0)
t.hideturtle()

# ---------------- INPUT DASHBOARD ---------------- #

tk.Label(frame, text="Axiom").pack()
axiom_entry = tk.Entry(frame)
axiom_entry.insert(0, "F")
axiom_entry.pack()

tk.Label(frame, text="Rules (F:F+F--F+F)").pack()
rules_entry = tk.Entry(frame)
rules_entry.insert(0, "F:F+F--F+F")
rules_entry.pack()

tk.Label(frame, text="Angle").pack()
angle_entry = tk.Entry(frame)
angle_entry.insert(0, "60")
angle_entry.pack()

tk.Label(frame, text="Iterations").pack()
iter_entry = tk.Entry(frame)
iter_entry.insert(0, "4")
iter_entry.pack()

tk.Button(frame, text="Generate", command=generate).pack(pady=10)

root.mainloop()
