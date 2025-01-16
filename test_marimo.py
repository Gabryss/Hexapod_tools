import marimo

__generated_with = "0.10.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import math

    def inverse_kinematics(x, y, z, L1, L2):
        """
        Compute the inverse kinematics for a 3-DoF hexapod leg.
        
        Parameters:
            x, y, z: Target foot position in the robot's coordinate frame.
            L1: Length of the femur.
            L2: Length of the tibia.
        
        Returns:
            theta1: Hip joint angle (in radians).
            theta2: Femur joint angle (in radians).
            theta3: Tibia joint angle (in radians).
        """
        # Step 1: Calculate hip rotation (theta1)
        theta1 = math.atan2(y, x)  # Angle to project onto the x-y plane
        
        # Step 2: Calculate the distance from the hip joint to the target position
        horizontal_dist = math.sqrt(x**2 + y**2)
        total_dist = math.sqrt(horizontal_dist**2 + z**2)
        
        # Step 3: Check reachability
        if total_dist > (L1 + L2):
            raise ValueError("Target is out of reach!")
        if total_dist < abs(L1 - L2):
            raise ValueError("Target is within the minimum workspace!")
        
        # Step 4: Compute angles for femur and tibia using trigonometry
        # Angle of the leg plane to horizontal
        leg_angle = math.atan2(z, horizontal_dist)
        
        # Law of cosines to find femur and tibia angles
        cos_angle2 = (L1**2 + total_dist**2 - L2**2) / (2 * L1 * total_dist)
        theta2 = leg_angle - math.acos(cos_angle2)  # Subtract for correct femur angle
        
        cos_angle3 = (L1**2 + L2**2 - total_dist**2) / (2 * L1 * L2)
        theta3 = math.pi - math.acos(cos_angle3)  # Pi minus the included angle
        
        return theta1, theta2, theta3

    return inverse_kinematics, math


@app.cell
def _(inverse_kinematics, math):
     # Define leg parameters
    L1 = 10.0  # Femur length
    L2 = 15.0  # Tibia length

    # Target foot position
    x = 5.0
    y = 5.0
    z = -10.0

    try:
        theta1, theta2, theta3 = inverse_kinematics(x, y, z, L1, L2)
        print(f"Joint Angles:")
        print(f"Theta1 (Hip): {math.degrees(theta1):.2f}°")
        print(f"Theta2 (Femur): {math.degrees(theta2):.2f}°")
        print(f"Theta3 (Tibia): {math.degrees(theta3):.2f}°")
    except ValueError as e:
        print(e)
    return L1, L2, theta1, theta2, theta3, x, y, z


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 22)
    return (slider,)


@app.cell
def _(mo, slider):
    mo.md(
        f"""
        Please select the amount of gears: {slider}.

        {slider.value}
        """
    )
    return


@app.cell
def _(mo):
    icon = mo.ui.dropdown(["🍃", "🌊", "✨"], value="🍃")
    return (icon,)


@app.cell
def _(mo):
    number = mo.ui.number(start=1, stop=10, step=1)
    number
    return (number,)


@app.cell
def _(number):
    number.value
    return


@app.cell
def _(mo):
    checkbox = mo.ui.checkbox(label="checkbox")
    checkbox
    return (checkbox,)


@app.cell
def _(checkbox):
    checkbox.value
    return


@app.cell
def _(mo):
    text = mo.ui.text(placeholder="type some text ...")
    text
    return (text,)


@app.cell
def _(text):
    text.value
    return


@app.cell
def _(mo):
    text_area = mo.ui.text_area(placeholder="type some text ...")
    text_area
    return (text_area,)


@app.cell
def _(text_area):
    text_area.value
    return


@app.cell
def _(mo):
    dropdown = mo.ui.dropdown(["wormgear", "direct drive", "cables"])
    dropdown
    return (dropdown,)


@app.cell
def _(dropdown):
    dropdown.value
    return


@app.cell
def _(mo):
    run_button = mo.ui.run_button(label="click me")
    run_button
    return (run_button,)


@app.cell
def _(basic_ui_elements, construct_element, show_element):
    selected_element = construct_element(basic_ui_elements.value)
    show_element(selected_element)
    return (selected_element,)


@app.cell
def _(mo):
    # Might be usefull
    dictionary = mo.ui.dictionary(
        {
            "text": mo.ui.text(),
            "slider": mo.ui.slider(start=1, stop=10),
            "date": mo.ui.date(),
        }
    )
    dictionary
    return (dictionary,)


@app.cell
def _():
    def wormgear_corrected_angle(input_angle, gear_ratio):
        """
        Calculate the output angle of a worm gear mechanism.
        
        Parameters:
            input_angle (float): The angle of rotation applied to the worm (in degrees).
            gear_ratio (float): The worm gear ratio (e.g., 40 for a 40:1 gear ratio).
            
        Returns:
            float: The corrected output angle of the worm gear (in degrees).
        """
        if gear_ratio <= 0:
            raise ValueError("Gear ratio must be a positive value.")
        
        # Calculate output angle
        output_angle = input_angle / gear_ratio
        return output_angle
    return (wormgear_corrected_angle,)


@app.cell
def _():
    def apply_wormgear_correction(theta, gear_ratio):
        """
        Corrects the joint angle for a worm gear system.
        
        Parameters:
            theta (float): Desired joint angle (degrees).
            gear_ratio (float): Worm gear ratio (e.g., 40:1).
        
        Returns:
            float: Motor input angle needed to achieve the desired joint angle.

        Example:
            Input Angle = Desired Angle × Gear Ratio = 90×40 = 3600
            So, the motor must rotate 3600° (10 full rotations) to achieve the desired joint angle.
        """
        return theta * gear_ratio
    return (apply_wormgear_correction,)


@app.cell
def _(mo):
    _gears = mo.vstack(
        [
            mo.md("**Edit gears**"),
            mo.ui.text(label="Worm gear"),
            mo.ui.text(label="Number of gears"),
        ]
    )

    _Hexa = mo.vstack(
        [
            mo.md("**Edit Hexa**"),
            mo.ui.text(label="Hexa Name"),
            mo.ui.number(label="Number of Hexa", start=0, stop=1000),
        ]
    )

    mo.ui.tabs(
        {
            "🧙‍♀ Gears": _gears,
            "🏢 Hexa": _Hexa,
        }
    )
    return


if __name__ == "__main__":
    app.run()
