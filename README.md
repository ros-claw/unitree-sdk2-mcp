# rosclaw-g1-dds-mcp

🌐 **English** | [中文](./README.zh.md)

ROSClaw MCP Server for **Unitree G1 Humanoid Robot** via DDS protocol.

Part of the [ROSClaw](https://github.com/ros-claw) Embodied Intelligence Operating System.

## Overview

This MCP server enables LLM agents (Claude, GPT-4, etc.) to control a Unitree G1 humanoid robot through the Model Context Protocol. It communicates with the robot using DDS (Data Distribution Service) — the same protocol used by Unitree's official SDK.

```
LLM Agent  ──MCP──►  rosclaw-g1-dds-mcp  ──DDS──►  Unitree G1
```

## SDK Information

| Property | Value |
|----------|-------|
| **SDK Name** | unitree_sdk2 |
| **SDK Version** | 2.1.0+ |
| **Protocol** | DDS (Data Distribution Service) |
| **Source Repository** | [github.com/unitreerobotics/unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) |
| **Documentation** | [support.unitree.com](https://support.unitree.com/home/zh/developer) |
| **License** | BSD-3-Clause |
| **Generated** | 2026-04-07 |

## Hardware Specification

| Specification | Value |
|--------------|-------|
| **Robot Model** | Unitree G1 Humanoid |
| **Degrees of Freedom** | 23 (G1-23D) / 43 (G1-43D) |
| **Height** | ~1.32m (standing) |
| **Weight** | ~35kg |
| **Battery Life** | ~2.5 hours |
| **Max Walking Speed** | 2m/s |
| **Communication** | DDS over Ethernet/WiFi |
| **DDS Domain ID** | 0 (configurable) |
| **State Update Rate** | 100 Hz |

### Joint Configuration

| Body Part | Joints | Count |
|-----------|--------|-------|
| Left Leg | left_hip_yaw, left_hip_roll, left_hip_pitch, left_knee, left_ankle | 5 |
| Right Leg | right_hip_yaw, right_hip_roll, right_hip_pitch, right_knee, right_ankle | 5 |
| Waist | waist_yaw, waist_roll, waist_pitch | 3 |
| Left Arm | left_shoulder_pitch, left_shoulder_roll, left_shoulder_yaw, left_elbow | 4 |
| Right Arm | right_shoulder_pitch, right_shoulder_roll, right_shoulder_yaw, right_elbow | 4 |
| **Total** | | **23** |

## Features

- **Full body control**: 23 joints (legs, waist, arms)
- **High-level actions**: stand, sit, walk, wave hand
- **Safety guards**: joint limits enforced before every command
- **Real-time state**: battery, mode, joint positions, IMU at 100Hz
- **DDS protocol**: CycloneDDS / FastDDS compatible
- **Async design**: non-blocking MCP tools with background state thread

## Installation

```bash
# Clone
git clone https://github.com/ros-claw/rosclaw-g1-dds-mcp.git
cd rosclaw-g1-dds-mcp

# Install with uv (recommended)
uv venv --python python3.10
source .venv/bin/activate
uv pip install -e .

# Or with pip
pip install -e .
```

### Dependencies

```bash
# Required: Unitree SDK2
# Download from: https://github.com/unitreerobotics/unitree_sdk2

# DDS Middleware (choose one)
pip install cyclonedds  # or fastdds
```

## Quick Start

### Run as MCP Server

```bash
# stdio transport (for Claude Desktop / MCP clients)
python src/g1_mcp_server.py

# Or using the installed entry point
rosclaw-g1-mcp
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rosclaw-g1": {
      "command": "python",
      "args": ["/path/to/rosclaw-g1-dds-mcp/src/g1_mcp_server.py"],
      "transportType": "stdio",
      "description": "Unitree G1 Humanoid via DDS",
      "sdk_version": "2.1.0",
      "sdk_source": "https://github.com/unitreerobotics/unitree_sdk2"
    }
  }
}
```

### MCP Inspector (Testing)

```bash
mcp dev src/g1_mcp_server.py
```

## Available Tools

| Tool | Description |
|------|-------------|
| `connect_g1` | Connect to G1 via DDS domain |
| `disconnect_g1` | Disconnect from G1 |
| `stand_up` | Command G1 to stand up |
| `sit_down` | Command G1 to sit down |
| `walk_with_velocity` | Walk with linear/angular velocity |
| `move_joint` | Move a single joint to target angle |
| `move_joints` | Move multiple joints simultaneously |
| `stop_movement` | Stop and hold current position |
| `emergency_stop` | Emergency halt (use with caution!) |
| `wave_hand` | Perform waving gesture |

## Available Resources

| Resource | Description |
|----------|-------------|
| `g1://status` | Battery, mode, joint positions |
| `g1://joints` | Joint limits for all 23 joints |
| `g1://connection` | DDS connection status |

## Joint Reference

```
Left Leg:   left_hip_yaw, left_hip_roll, left_hip_pitch, left_knee, left_ankle
Right Leg:  right_hip_yaw, right_hip_roll, right_hip_pitch, right_knee, right_ankle
Waist:      waist_yaw, waist_roll, waist_pitch
Left Arm:   left_shoulder_pitch, left_shoulder_roll, left_shoulder_yaw, left_elbow
Right Arm:  right_shoulder_pitch, right_shoulder_roll, right_shoulder_yaw, right_elbow
```

### Joint Limits

| Joint | Range (rad) | Velocity Limit (rad/s) |
|-------|-------------|------------------------|
| left_hip_yaw | [-2.35, 2.35] | 10 |
| left_hip_roll | [-0.78, 0.78] | 10 |
| left_hip_pitch | [-2.5, 2.5] | 10 |
| left_knee | [-0.5, 2.5] | 10 |
| left_ankle | [-1.0, 1.0] | 10 |
| right_hip_yaw | [-2.35, 2.35] | 10 |
| right_hip_roll | [-0.78, 0.78] | 10 |
| right_hip_pitch | [-2.5, 2.5] | 10 |
| right_knee | [-0.5, 2.5] | 10 |
| right_ankle | [-1.0, 1.0] | 10 |
| waist_yaw | [-2.5, 2.5] | 5 |
| waist_roll | [-0.5, 0.5] | 5 |
| waist_pitch | [-1.0, 1.0] | 5 |
| left_shoulder_pitch | [-3.14, 3.14] | 10 |
| left_shoulder_roll | [-0.5, 3.5] | 10 |
| left_shoulder_yaw | [-2.0, 2.0] | 10 |
| left_elbow | [-1.5, 2.0] | 10 |
| right_shoulder_pitch | [-3.14, 3.14] | 10 |
| right_shoulder_roll | [-3.5, 0.5] | 10 |
| right_shoulder_yaw | [-2.0, 2.0] | 10 |
| right_elbow | [-1.5, 2.0] | 10 |

## Safety Information

**WARNING:** This MCP server controls a 35kg humanoid robot. Improper use can cause:
- Equipment damage
- Personal injury
- Property damage

### Safety Features

| Feature | Description |
|---------|-------------|
| **Joint Limits** | All commands validated against hardware limits |
| **Velocity Limits** | Legs ≤ 10 rad/s, waist ≤ 5 rad/s, arms ≤ 10 rad/s |
| **Emergency Stop** | `emergency_stop()` disables motors immediately |

### Safety Levels

| Level | Color | Description |
|-------|-------|-------------|
| **CRITICAL** | 🔴 | Immediate danger (falling, collision) |
| **HIGH** | 🟠 | Potential hardware damage |
| **MEDIUM** | 🟡 | Operational issue |
| **LOW** | 🟢 | Informational |

### Emergency Procedures

1. **Immediate Stop**: Use `emergency_stop()` or press physical E-stop
2. **Power Off**: Disconnect battery if safe
3. **Check Status**: Use `g1://status` resource

## Error Handling

### Error Codes

| Code | Name | Severity | Description |
|------|------|----------|-------------|
| -1 | CONNECTION_FAILED | 🟠 error | Failed to connect to DDS domain |
| -2 | TIMEOUT | 🟠 error | Operation timed out |
| -3 | INVALID_PARAMETER | 🟠 error | Invalid joint name or value |
| -4 | SAFETY_VIOLATION | 🔴 critical | Command exceeds joint limits |
| -5 | NOT_INITIALIZED | 🟠 error | Not connected to robot |

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Connection failed | Robot powered off | Check battery and power switch |
| Connection failed | Wrong DDS domain | Verify domain_id parameter |
| Command rejected | Joint limit exceeded | Check joint limits table |
| Slow response | Network latency | Check WiFi/Ethernet connection |

## Dependencies

- Python 3.10+
- `mcp[fastmcp]` — MCP framework
- `unitree_sdk2` — Unitree DDS SDK (install separately from hardware package)
- `cyclonedds` or `fastdds` — DDS middleware

## Architecture

```
g1_mcp_server.py
├── SDK_METADATA      — SDK version and source info
├── G1State           — Robot state dataclass
├── StateBuffer       — Thread-safe ring buffer for DDS data
├── G1DDSBridge       — DDS communication bridge
│   ├── connect()     — Initialize DDS participant
│   ├── _dds_listener() — Background thread at 100Hz
│   └── publish_command() — Send /lowcmd
└── MCP Tools         — FastMCP tool definitions
```

## DDS Topics

| Topic | Direction | Description |
|-------|-----------|-------------|
| `/lowstate` | Subscribe | Robot state (joints, IMU, battery) |
| `/lowcmd` | Publish | Robot commands (joint targets, mode) |
| `/sportmodestate` | Subscribe | Sport mode state |

## References

- [Unitree SDK2 GitHub](https://github.com/unitreerobotics/unitree_sdk2)
- [Unitree Developer Docs](https://support.unitree.com/home/zh/developer)
- [Unitree G1 Product Page](https://www.unitree.com/products/g1)
- [DDS Specification](https://www.dds-foundation.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## License

MIT License — See [LICENSE](LICENSE)

## Part of ROSClaw

- [rosclaw-g1-dds-mcp](https://github.com/ros-claw/rosclaw-g1-dds-mcp) — Unitree G1 (DDS)
- [rosclaw-ur-ros2-mcp](https://github.com/ros-claw/rosclaw-ur-ros2-mcp) — UR5 arm (ROS2)
- [rosclaw-gimbal-mcp](https://github.com/ros-claw/rosclaw-gimbal-mcp) — GCU Gimbal (Serial)
- [rosclaw-ur-rtde-mcp](https://github.com/ros-claw/rosclaw-ur-rtde-mcp) — UR5 via RTDE

---

**Generated by ROSClaw SDK-to-MCP Transformer**

*SDK Version: unitree_sdk2 2.1.0+ | Protocol: DDS*
