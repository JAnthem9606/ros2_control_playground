# ros2_control_playground

An educational companion to [ros-controls/ros2_control](https://github.com/ros-controls/ros2_control)
and [ros-controls/ros2_control_demos](https://github.com/ros-controls/ros2_control_demos).

**Not affiliated with or endorsed by the ros-controls or MoveIt maintainers.**
This project exists to lower the ramp into those tools — not to replace them.
If you're building a production robot, use `ros2_control_demos` and MoveIt directly.

---

## Why this exists

`ros2_control` and MoveIt are powerful, professionally maintained, and deliberately
minimal in their official examples — which makes total sense for a production-grade
framework, but leaves a real gap for beginners. Small mistakes (a wrong joint origin,
a missed `setup.py` entry, a mismatched controller name) tend to fail silently or with
cryptic errors, and there's no beginner-paced walkthrough of *why* things work the way
they do.

This package is that walkthrough — built by making (and fixing) those mistakes myself,
across several manipulator archetypes, from scratch.

---

## Status: Work in Progress

| Manipulator | Type | Status |
|---|---|---|
| Cartesian gantry | PPP (3 prismatic) | ✅ Done |
| RRBot | RR planar (2 revolute) | ✅ Done |
| SCARA-style arm | RRP (2 revolute + 1 prismatic) | ✅ Done |
| Spherical wrist | RRR non-planar | ⏳ Planned |
| Delta / parallel manipulator | Closed-loop | ⏳ Planned |
| 6-DOF general arm | RRRRRR | ⏳ Planned |

---

## What's included, per manipulator

Each manipulator package follows the same structure:

- **URDF** with correct joint/visual origins, collision geometry, inertial
  properties, and joint dynamics (damping/friction)
- **`view_robot.launch.py`** — RViz + `joint_state_publisher_gui`, so you can
  move the robot with sliders with zero `ros2_control` knowledge required
- **`display.launch.py`** — full `ros2_control` setup: `controller_manager`,
  `joint_state_broadcaster`, and both `joint_trajectory_controller` and
  `forward_position_controller` (loaded together, switchable at runtime)
- **Pure-Python kinematics** — forward/inverse kinematics functions with
  zero ROS imports, so you can test the math directly in a plain Python
  REPL before ever touching ROS
- **Console scripts** for interactive control:
  - `<robot>_fk` — live forward kinematics from `/joint_states`
  - `<robot>_ik` — enter a target position, get computed joint values
  - `<robot>_command_publisher` — manually enter joint values, publish + verify
  - `<robot>_error_analyzer` — compares commanded vs. actual joint/Cartesian error

---

## Quick start

### 1. Clone into your workspace

```bash
cd ~/ros2_ws/src
git clone https://github.com/JAnthem9606/ros2_control_playground.git
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 2. See it move — no ros2_control required

```bash
ros2 launch scara_bot view_robot.launch.py
```

Drag the sliders in the `joint_state_publisher_gui` window. This is the
simplest way to explore a robot's geometry and joint limits before
touching any controller configuration.

### 3. Full control via ros2_control

```bash
ros2 launch scara_bot scara_bot.launch.py
```

Then, in another terminal:

```bash
ros2 run scara_bot scara_ik
```

Enter a target `x, y, z` and watch the arm move there via
`joint_trajectory_controller`.

Swap `scara_bot` for `rrbot_kinematics` or `three_prismatic_description`
to try the other manipulators — same commands, same structure.

---

## Switching controllers

Both `joint_trajectory_controller` (smooth, timed motion) and
`forward_position_controller` (direct passthrough, no interpolation) are
loaded at launch — only one is active at a time.

```bash
ros2 control list_controllers

ros2 control switch_controllers \
  --deactivate joint_trajectory_controller \
  --activate forward_position_controller
```

See [`docs/controllers.md`](docs/controllers.md) for a fuller explanation
of when to use which.

---

## Common pitfalls (learned the hard way)

See [`docs/pitfalls.md`](docs/pitfalls.md) for a running list of the
mistakes that ate the most debugging time while building this — joint
origin vs. visual origin, `ament_python` packaging gotchas, controller
name mismatches, and stray nested workspaces from running `colcon build`
in the wrong directory.

---

## Contributing

Issues, corrections, and additional manipulator archetypes are welcome.
This is explicitly a learning project — if something's wrong, unclear,
or could be explained better, please open an issue.

## License

Apache-2.0 — matching `ros2_control`'s license, so anything genuinely
reusable can be upstreamed without a licensing mismatch.
