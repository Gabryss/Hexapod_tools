import marimo as mo
import math

# Inverse Kinematics function
def inverse_kinematics(x, y, z, L1, L2):
    try:
        theta1 = math.atan2(y, x)
        horizontal_dist = math.sqrt(x**2 + y**2)
        total_dist = math.sqrt(horizontal_dist**2 + z**2)

        if total_dist > (L1 + L2) or total_dist < abs(L1 - L2):
            raise ValueError("Target is out of reachable workspace!")

        leg_angle = math.atan2(z, horizontal_dist)
        cos_angle2 = (L1**2 + total_dist**2 - L2**2) / (2 * L1 * total_dist)
        theta2 = leg_angle - math.acos(cos_angle2)

        cos_angle3 = (L1**2 + L2**2 - total_dist**2) / (2 * L1 * L2)
        theta3 = math.pi - math.acos(cos_angle3)

        return math.degrees(theta1), math.degrees(theta2), math.degrees(theta3)
    except Exception as e:
        return str(e)

# Input fields
x_input = mo.ui.text(label="X Coordinate")
y_input = mo.ui.text(label="Y Coordinate")
z_input = mo.ui.text(label="Z Coordinate")
L1_input = mo.ui.text(label="Femur Length (L1)")
L2_input = mo.ui.text(label="Tibia Length (L2)")

# Output display using a label
output_display = mo.ui.text(value="Results will appear here.")

# Compute button callback
def compute_angles():
    try:
        x = float(x_input.value)
        y = float(y_input.value)
        z = float(z_input.value)
        L1 = float(L1_input.value)
        L2 = float(L2_input.value)

        result = inverse_kinematics(x, y, z, L1, L2)
        if isinstance(result, str):
            output_display.text = f"Error: {result}"
        else:
            theta1, theta2, theta3 = result
            output_display.text = (
                f"θ1: {theta1:.2f}°, θ2: {theta2:.2f}°, θ3: {theta3:.2f}°"
            )
    except ValueError:
        output_display.text = "Error: Please enter valid numeric values!"

# Compute button
compute_button = mo.ui.button(label="Compute Angles", on_click=compute_angles)

# Layout
layout = mo.ui.column(
    x_input,
    y_input,
    z_input,
    L1_input,
    L2_input,
    compute_button,
    output_display,
)

# App definition
app = mo.App("Hexapod IK Calculator")
app.main = layout

# Run the app
if __name__ == "__main__":
    app.run()
