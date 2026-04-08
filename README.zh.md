# rosclaw-g1-dds-mcp

[English](./README.md) | **中文**

ROSClaw MCP Server for **Unitree G1 人形机器人** via DDS 协议。

Part of the [ROSClaw](https://github.com/ros-claw) Embodied Intelligence Operating System.

## 概述

This MCP server enables LLM agents (Claude, GPT-4, etc.) to control a Unitree G1 humanoid robot through the Model Context Protocol. It communicates with the robot using DDS (Data Distribution Service) — the same protocol used by Unitree's official SDK.

```
LLM Agent  ──MCP──►  rosclaw-g1-dds-mcp  ──DDS──►  Unitree G1
```

## SDK 信息

| 属性 | 值 |
|----------|-------|
| **SDK 名称** | unitree_sdk2 |
| **SDK 版本** | 2.1.0+ |
| **协议** | DDS (Data Distribution Service) |
| **源码仓库** | [github.com/unitreerobotics/unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) |
| **文档** | [support.unitree.com](https://support.unitree.com/home/zh/developer) |
| **许可证** | BSD-3-Clause |
| **生成日期** | 2026-04-07 |

## 硬件规格

| 规格 | 值 |
|--------------|-------|
| **机器人类型** | Unitree G1 人形机器人 |
| **自由度** | 23 (G1-23D) / 43 (G1-43D) |
| **高度** | ~1.32m (站立) |
| **重量** | ~35kg |
| **电池续航** | ~2.5 小时 |
| **最大行走速度** | 2m/s |
| **通信** | DDS over Ethernet/WiFi |
| **DDS Domain ID** | 0 (可配置) |
| **状态更新频率** | 100 Hz |

### 关节配置

| 身体部位 | 关节 | 数量 |
|-----------|--------|-------|
| 左腿 | left_hip_yaw, left_hip_roll, left_hip_pitch, left_knee, left_ankle | 5 |
| 右腿 | right_hip_yaw, right_hip_roll, right_hip_pitch, right_knee, right_ankle | 5 |
| 腰部 | waist_yaw, waist_roll, waist_pitch | 3 |
| 左臂 | left_shoulder_pitch, left_shoulder_roll, left_shoulder_yaw, left_elbow | 4 |
| 右臂 | right_shoulder_pitch, right_shoulder_roll, right_shoulder_yaw, right_elbow | 4 |
| **总计** | | **23** |

## 功能特性

- **全身控制**: 23 个关节 (腿、腰、臂)
- **高级动作**: 站立、坐下、行走、挥手
- **安全保护**: 每个命令执行前强制执行关节限制
- **实时状态**: 电池、模式、关节位置、IMU 100Hz 更新
- **DDS 协议**: 兼容 CycloneDDS / FastDDS
- **异步设计**: 非阻塞 MCP 工具，后台状态线程

## 安装

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

### 依赖

```bash
# Required: Unitree SDK2
# Download from: https://github.com/unitreerobotics/unitree_sdk2

# DDS Middleware (choose one)
pip install cyclonedds  # or fastdds
```

## 快速开始

### 作为 MCP Server 运行

```bash
# stdio transport (for Claude Desktop / MCP clients)
python src/g1_mcp_server.py

# Or using the installed entry point
rosclaw-g1-mcp
```

### Claude Desktop 配置

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

### MCP Inspector (测试)

```bash
mcp dev src/g1_mcp_server.py
```

## 可用工具

| 工具 | 描述 |
|------|-------------|
| `connect_g1` | 通过 DDS domain 连接 G1 |
| `disconnect_g1` | 断开 G1 连接 |
| `stand_up` | 命令 G1 站立 |
| `sit_down` | 命令 G1 坐下 |
| `walk_with_velocity` | 以线速度/角速度行走 |
| `move_joint` | 移动单个关节到目标角度 |
| `move_joints` | 同时移动多个关节 |
| `stop_movement` | 停止并保持当前位置 |
| `emergency_stop` | 紧急停止 (谨慎使用!) |
| `wave_hand` | 执行挥手动作 |

## 可用资源

| 资源 | 描述 |
|----------|-------------|
| `g1://status` | 电池、模式、关节位置 |
| `g1://joints` | 所有 23 个关节的关节限制 |
| `g1://connection` | DDS 连接状态 |

## 关节参考

```
左腿:   left_hip_yaw, left_hip_roll, left_hip_pitch, left_knee, left_ankle
右腿:  right_hip_yaw, right_hip_roll, right_hip_pitch, right_knee, right_ankle
腰部:      waist_yaw, waist_roll, waist_pitch
左臂:   left_shoulder_pitch, left_shoulder_roll, left_shoulder_yaw, left_elbow
右臂:  right_shoulder_pitch, right_shoulder_roll, right_shoulder_yaw, right_elbow
```

### 关节限制

| 关节 | 范围 (rad) | 速度限制 (rad/s) |
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

## 安全信息

**警告:** This MCP server controls a 35kg humanoid robot. Improper use can cause:
- 设备损坏
- 人身伤害
- 财产损失

### 安全特性

| 特性 | 描述 |
|---------|-------------|
| **关节限制** | 所有命令都根据硬件限制进行验证 |
| **速度限制** | 腿部 ≤ 10 rad/s, 腰部 ≤ 5 rad/s, 臂部 ≤ 10 rad/s |
| **紧急停止** | `emergency_stop()` 立即禁用电机 |

### 安全级别

| 级别 | 颜色 | 描述 |
|-------|-------|-------------|
| **CRITICAL** | 🔴 | 立即危险 (摔倒、碰撞) |
| **HIGH** | 🟠 | 潜在硬件损坏 |
| **MEDIUM** | 🟡 | 操作问题 |
| **LOW** | 🟢 | 信息提示 |

### 紧急程序

1. **立即停止**: 使用 `emergency_stop()` 或按下物理紧急停止按钮
2. **断电**: 如果安全，断开电池
3. **检查状态**: 使用 `g1://status` 资源

## 错误处理

### 错误代码

| 代码 | 名称 | 严重级别 | 描述 |
|------|------|----------|-------------|
| -1 | CONNECTION_FAILED | 🟠 error | 无法连接到 DDS domain |
| -2 | TIMEOUT | 🟠 error | 操作超时 |
| -3 | INVALID_PARAMETER | 🟠 error | 无效的关节名称或值 |
| -4 | SAFETY_VIOLATION | 🔴 critical | 命令超出关节限制 |
| -5 | NOT_INITIALIZED | 🟠 error | 未连接到机器人 |

### 故障排除

| 问题 | 可能原因 | 解决方案 |
|-------|---------------|----------|
| 连接失败 | 机器人断电 | 检查电池和电源开关 |
| 连接失败 | 错误的 DDS domain | 验证 domain_id 参数 |
| 命令被拒绝 | 关节限制超出 | 检查关节限制表 |
| 响应缓慢 | 网络延迟 | 检查 WiFi/Ethernet 连接 |

## 依赖

- Python 3.10+
- `mcp[fastmcp]` — MCP 框架
- `unitree_sdk2` — Unitree DDS SDK (从硬件包单独安装)
- `cyclonedds` or `fastdds` — DDS 中间件

## 架构

```
g1_mcp_server.py
├── SDK_METADATA      — SDK 版本和源码信息
├── G1State           — 机器人状态数据类
├── StateBuffer       — DDS 数据的线程安全环形缓冲区
├── G1DDSBridge       — DDS 通信桥接
│   ├── connect()     — 初始化 DDS participant
│   ├── _dds_listener() — 100Hz 后台线程
│   └── publish_command() — 发送 /lowcmd
└── MCP Tools         — FastMCP 工具定义
```

## DDS Topics

| Topic | 方向 | 描述 |
|-------|-----------|-------------|
| `/lowstate` | Subscribe | 机器人状态 (关节、IMU、电池) |
| `/lowcmd` | Publish | 机器人命令 (关节目标、模式) |
| `/sportmodestate` | Subscribe | 运动模式状态 |

## 参考

- [Unitree SDK2 GitHub](https://github.com/unitreerobotics/unitree_sdk2)
- [Unitree Developer Docs](https://support.unitree.com/home/zh/developer)
- [Unitree G1 Product Page](https://www.unitree.com/products/g1)
- [DDS Specification](https://www.dds-foundation.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 许可证

MIT License — See [LICENSE](LICENSE)

## Part of ROSClaw

- [rosclaw-g1-dds-mcp](https://github.com/ros-claw/rosclaw-g1-dds-mcp) — Unitree G1 (DDS)
- [rosclaw-ur-ros2-mcp](https://github.com/ros-claw/rosclaw-ur-ros2-mcp) — UR5 arm (ROS2)
- [rosclaw-gimbal-mcp](https://github.com/ros-claw/rosclaw-gimbal-mcp) — GCU Gimbal (Serial)
- [rosclaw-ur-rtde-mcp](https://github.com/ros-claw/rosclaw-ur-rtde-mcp) — UR5 via RTDE

---

**Generated by ROSClaw SDK-to-MCP Transformer**

*SDK Version: unitree_sdk2 2.1.0+ | Protocol: DDS*
