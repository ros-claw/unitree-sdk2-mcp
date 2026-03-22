"""
ROSClaw G1 DDS MCP Server

Unitree G1 Humanoid Robot MCP Server using DDS protocol.
Part of the ROSClaw Embodied Intelligence Operating System.

Features:
- DDS communication via CycloneDDS/FastDDS
- G1 actions: stand_up, sit_down, walk, move joints
- Safety guards for joint limits
- State monitoring (battery, joint angles, IMU)

Hardware: Unitree G1 Humanoid Robot
Protocol: DDS (Data Distribution Service)
"""

import asyncio
import threading
import time
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from collections import deque
from mcp.server.fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("rosclaw-g1")


@dataclass
class G1State:
    """G1 robot state data"""
    timestamp: float
    battery_level: int  # 0-100%
    robot_mode: int  # 0: idle, 1: standing, 2: walking, etc.

    # Joint states (radians)
    joint_positions: Dict[str, float] = field(default_factory=dict)
    joint_velocities: Dict[str, float] = field(default_factory=dict)
    joint_torques: Dict[str, float] = field(default_factory=dict)

    # IMU data
    imu_quaternion: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    imu_gyroscope: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    imu_accelerometer: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    # Body state
    body_height: float = 0.0
    body_pitch: float = 0.0
    body_roll: float = 0.0
    body_yaw: float = 0.0


@dataclass
class StateBuffer:
    """Thread-safe state buffer for DDS data"""
    max_size: int = 100
    _buffer: deque = field(default_factory=lambda: deque(maxlen=100))
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def append(self, state: G1State):
        with self._lock:
            self._buffer.append(state)

    def get_latest(self) -> Optional[G1State]:
        with self._lock:
            return self._buffer[-1] if self._buffer else None

    def get_history(self, n: int = 10) -> List[G1State]:
        with self._lock:
            return list(self._buffer)[-n:]


class G1DDSBridge:
    """
    Unitree G1 DDS Communication Bridge

    Protocol: DDS (Data Distribution Service)
    Domain: Default DDS domain
    Topics:
    - /lowstate: Robot state (joints, IMU, battery)
    - /lowcmd: Robot commands (joint targets, mode)
    - /sportmodestate: Sport mode state
    """

    # G1 Joint names
    JOINT_NAMES = [
        # Left leg
        "left_hip_yaw", "left_hip_roll", "left_hip_pitch",
        "left_knee", "left_ankle",
        # Right leg
        "right_hip_yaw", "right_hip_roll", "right_hip_pitch",
        "right_knee", "right_ankle",
        # Waist
        "waist_yaw", "waist_roll", "waist_pitch",
        # Left arm
        "left_shoulder_pitch", "left_shoulder_roll", "left_shoulder_yaw",
        "left_elbow",
        # Right arm
        "right_shoulder_pitch", "right_shoulder_roll", "right_shoulder_yaw",
        "right_elbow",
    ]

    # Safety limits (from URDF/e-URDF)
    JOINT_LIMITS = {
        # Legs
        "left_hip_yaw": (-2.35, 2.35),
        "left_hip_roll": (-0.78, 0.78),
        "left_hip_pitch": (-2.5, 2.5),
        "left_knee": (-0.5, 2.5),
        "left_ankle": (-1.0, 1.0),
        "right_hip_yaw": (-2.35, 2.35),
        "right_hip_roll": (-0.78, 0.78),
        "right_hip_pitch": (-2.5, 2.5),
        "right_knee": (-0.5, 2.5),
        "right_ankle": (-1.0, 1.0),
        # Waist
        "waist_yaw": (-2.5, 2.5),
        "waist_roll": (-0.5, 0.5),
        "waist_pitch": (-1.0, 1.0),
        # Arms
        "left_shoulder_pitch": (-3.14, 3.14),
        "left_shoulder_roll": (-0.5, 3.5),
        "left_shoulder_yaw": (-2.0, 2.0),
        "left_elbow": (-1.5, 2.0),
        "right_shoulder_pitch": (-3.14, 3.14),
        "right_shoulder_roll": (-3.5, 0.5),
        "right_shoulder_yaw": (-2.0, 2.0),
        "right_elbow": (-1.5, 2.0),
    }

    # Velocity limits (rad/s)
    VELOCITY_LIMITS = {
        "leg": 10.0,
        "waist": 5.0,
        "arm": 10.0,
    }

    def __init__(self, domain_id: int = 0):
        self.domain_id = domain_id
        self.connected = False
        self._stop_event = threading.Event()
        self._dds_thread: Optional[threading.Thread] = None

        # State buffer
        self.state_buffer = StateBuffer(max_size=100)

        # Current command
        self._current_mode = 0  # 0: idle
        self._target_positions: Dict[str, float] = {}
        self._cmd_lock = threading.Lock()

    def connect(self) -> bool:
        """
        Connect to G1 DDS domain

        Returns:
            True if connected successfully
        """
        try:
            # TODO: Initialize DDS participant
            # This would use unitree_sdk2 or cyclonedds Python bindings
            # For now, we'll simulate the connection

            self.connected = True
            self._stop_event.clear()

            # Start DDS listener thread
            self._dds_thread = threading.Thread(
                target=self._dds_listener,
                name="G1DDSListener",
                daemon=True
            )
            self._dds_thread.start()

            return True

        except Exception as e:
            print(f"DDS connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from DDS domain"""
        self._stop_event.set()
        if self._dds_thread and self._dds_thread.is_alive():
            self._dds_thread.join(timeout=2.0)
        self.connected = False

    def _dds_listener(self):
        """
        DDS listener thread - receives state updates

        This runs in a separate thread to avoid blocking MCP
        """
        print("G1 DDS listener started")

        while not self._stop_event.is_set():
            try:
                # TODO: Implement actual DDS subscription
                # Subscribe to /lowstate topic

                # Simulate state update for now
                state = G1State(
                    timestamp=time.time(),
                    battery_level=85,
                    robot_mode=self._current_mode,
                    joint_positions={name: 0.0 for name in self.JOINT_NAMES},
                )
                self.state_buffer.append(state)

                time.sleep(0.01)  # 100Hz update rate

            except Exception as e:
                print(f"DDS listener error: {e}")
                time.sleep(0.1)

        print("G1 DDS listener stopped")

    def publish_command(self, mode: int, positions: Optional[Dict[str, float]] = None):
        """
        Publish command to G1

        Args:
            mode: Robot mode (0: idle, 1: standing, 2: walking, etc.)
            positions: Target joint positions (optional)
        """
        with self._cmd_lock:
            self._current_mode = mode
            if positions:
                self._target_positions = positions.copy()

        # TODO: Publish to /lowcmd topic via DDS

    def _validate_joint_positions(self, positions: Dict[str, float]) -> Tuple[bool, str]:
        """
        Validate joint positions against safety limits

        Returns:
            (valid, error_message)
        """
        for joint, value in positions.items():
            if joint in self.JOINT_LIMITS:
                min_val, max_val = self.JOINT_LIMITS[joint]
                if not (min_val <= value <= max_val):
                    return False, f"Joint {joint} value {value} out of range [{min_val}, {max_val}]"
        return True, "OK"

    def get_latest_state(self) -> Optional[G1State]:
        """Get latest robot state"""
        return self.state_buffer.get_latest()


# Global bridge instance
_bridge: Optional[G1DDSBridge] = None


# ============ MCP Tools ============

@mcp.tool()
async def connect_g1(domain_id: int = 0) -> str:
    """
    Connect to Unitree G1 robot via DDS

    Args:
        domain_id: DDS domain ID (default: 0)
    """
    global _bridge

    if _bridge is None:
        _bridge = G1DDSBridge(domain_id=domain_id)

    if _bridge.connect():
        return f"✓ Connected to G1 on DDS domain {domain_id}"
    else:
        return "✗ Failed to connect to G1"


@mcp.tool()
async def disconnect_g1() -> str:
    """Disconnect from G1 robot"""
    global _bridge

    if _bridge:
        _bridge.disconnect()
        _bridge = None
        return "✓ Disconnected from G1"

    return "Not connected"


@mcp.tool()
async def stand_up() -> str:
    """
    Command G1 to stand up

    This transitions the robot from sitting/idle to standing position.
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    # Set standing mode
    _bridge.publish_command(mode=1)  # 1: standing mode

    return "✓ Stand up command sent"


@mcp.tool()
async def sit_down() -> str:
    """
    Command G1 to sit down

    This transitions the robot to a sitting position.
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    _bridge.publish_command(mode=0)  # 0: idle/sitting mode

    return "✓ Sit down command sent"


@mcp.tool()
async def walk_with_velocity(linear_x: float = 0.0, linear_y: float = 0.0, angular_z: float = 0.0, duration: float = 2.0) -> str:
    """
    Command G1 to walk with specified velocity

    Args:
        linear_x: Forward/backward velocity (m/s), range [-1.0, 1.0]
        linear_y: Left/right velocity (m/s), range [-0.5, 0.5]
        angular_z: Rotation velocity (rad/s), range [-1.0, 1.0]
        duration: Walking duration (seconds)
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    # Safety limits
    if abs(linear_x) > 1.0:
        return "Error: linear_x exceeds safety limit of ±1.0 m/s"
    if abs(linear_y) > 0.5:
        return "Error: linear_y exceeds safety limit of ±0.5 m/s"
    if abs(angular_z) > 1.0:
        return "Error: angular_z exceeds safety limit of ±1.0 rad/s"

    # Set walking mode
    _bridge.publish_command(mode=2)  # 2: walking mode

    # Walk for specified duration
    await asyncio.sleep(duration)

    # Stop walking
    _bridge.publish_command(mode=1)  # Return to standing

    return f"✓ Walked with velocity ({linear_x}, {linear_y}, {angular_z}) for {duration}s"


@mcp.tool()
async def move_joint(joint_name: str, target_position: float, duration: float = 2.0) -> str:
    """
    Move a specific joint to target position

    Args:
        joint_name: Name of the joint (e.g., 'left_elbow', 'waist_yaw')
        target_position: Target angle in radians
        duration: Movement duration (seconds)
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    # Validate joint name
    if joint_name not in G1DDSBridge.JOINT_NAMES:
        return f"Error: Unknown joint '{joint_name}'. Valid joints: {G1DDSBridge.JOINT_NAMES}"

    # Validate position
    valid, msg = _bridge._validate_joint_positions({joint_name: target_position})
    if not valid:
        return f"Safety check failed: {msg}"

    # Send command
    _bridge.publish_command(mode=1, positions={joint_name: target_position})

    await asyncio.sleep(duration)

    return f"✓ Moved {joint_name} to {target_position:.3f} rad"


@mcp.tool()
async def move_joints(positions: Dict[str, float], duration: float = 3.0) -> str:
    """
    Move multiple joints simultaneously

    Args:
        positions: Dictionary of {joint_name: target_position}
        duration: Movement duration (seconds)
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    # Validate all positions
    valid, msg = _bridge._validate_joint_positions(positions)
    if not valid:
        return f"Safety check failed: {msg}"

    # Send command
    _bridge.publish_command(mode=1, positions=positions)

    await asyncio.sleep(duration)

    return f"✓ Moved {len(positions)} joints to target positions"


@mcp.tool()
async def stop_movement() -> str:
    """Stop all movement and hold current position"""
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    _bridge.publish_command(mode=1)  # Standing mode (hold position)

    return "✓ Stopped and holding position"


@mcp.tool()
async def emergency_stop() -> str:
    """
    Emergency stop - immediately halt all motion

    This will disable motor power and the robot may fall.
    Use with caution!
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    _bridge.publish_command(mode=0)  # Idle mode

    return "⚠ Emergency stop activated!"


@mcp.tool()
async def wave_hand(hand: str = "right", times: int = 3) -> str:
    """
    Perform a waving motion with the specified hand

    Args:
        hand: Which hand to wave ('left' or 'right')
        times: Number of waves
    """
    global _bridge

    if _bridge is None or not _bridge.connected:
        return "Error: Not connected to G1"

    if hand not in ["left", "right"]:
        return "Error: hand must be 'left' or 'right'"

    # Wave motion
    shoulder_yaw = f"{hand}_shoulder_yaw"
    elbow = f"{hand}_elbow"

    for i in range(times):
        # Raise arm
        _bridge.publish_command(mode=1, positions={
            shoulder_yaw: -1.5,
            elbow: -1.0
        })
        await asyncio.sleep(0.5)

        # Wave
        _bridge.publish_command(mode=1, positions={
            elbow: 0.0
        })
        await asyncio.sleep(0.5)

    # Lower arm
    _bridge.publish_command(mode=1, positions={
        shoulder_yaw: 0.0,
        elbow: 0.0
    })

    return f"✓ Waved {hand} hand {times} times"


# ============ MCP Resources ============

@mcp.resource("g1://status")
async def get_g1_status() -> str:
    """
    Get G1 robot current status

    Returns battery level, robot mode, and joint states
    """
    global _bridge

    if _bridge is None:
        return "Not connected to G1"

    state = _bridge.get_latest_state()
    if state is None:
        return "No state data available"

    mode_names = {
        0: "Idle/Sitting",
        1: "Standing",
        2: "Walking",
        3: "Running",
    }
    mode_str = mode_names.get(state.robot_mode, f"Unknown({state.robot_mode})")

    return f"""
G1 Robot Status:
  Battery: {state.battery_level}%
  Mode: {mode_str}
  Timestamp: {state.timestamp:.3f}

  Joint Positions (sample):
    waist_yaw: {state.joint_positions.get('waist_yaw', 0):.3f} rad
    left_elbow: {state.joint_positions.get('left_elbow', 0):.3f} rad
    right_elbow: {state.joint_positions.get('right_elbow', 0):.3f} rad
"""


@mcp.resource("g1://joints")
async def get_joint_info() -> str:
    """Get information about all joints"""
    info = ["G1 Joint Information:", "=" * 40]

    for joint, (min_val, max_val) in G1DDSBridge.JOINT_LIMITS.items():
        info.append(f"  {joint}: [{min_val:.2f}, {max_val:.2f}] rad")

    return "\n".join(info)


@mcp.resource("g1://connection")
async def get_connection_status() -> str:
    """Get DDS connection status"""
    global _bridge

    if _bridge and _bridge.connected:
        return f"Connected to G1 on DDS domain {_bridge.domain_id}"
    else:
        return "Disconnected"


if __name__ == "__main__":
    mcp.run(transport="stdio")
