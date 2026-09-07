# VHRM — Veeam Hardened Repository Manager

[English](README.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | **中文**

一个现代化、开源的终端界面，用于审计和准备作为 **Veeam Hardened Repository** 使用的 Linux 系统。

> **状态：** 早期社区版本 / 技术预览。请先在实验环境中使用。任何存储变更都必须由管理员验证。

## 为什么创建这个项目

VHRM 的工作流程受到 [`tdewin/veeamhubrepo`](https://github.com/tdewin/veeamhubrepo) 的启发。该项目采用 MIT 许可证，最初用于在 Veeam 实验环境中快速准备 Linux 不可变存储库。

VHRM 没有继续扩展其 2021 年基于 `dialog` 的实现，而是采用了**独立重构实现**，重点关注现代、可维护的用户体验以及“先审计、后变更”的安全模型。

## 主要改进

| 领域 | veeamhubrepo 的方式 | VHRM 的方式 |
|---|---|---|
| 界面 | 传统 dialog 向导 | 基于 Textual 的现代 TUI 仪表板 |
| 目标基线 | Ubuntu 20.04 / Veeam V11 时代 | 识别 Ubuntu 20.04/22.04/24.04/26.04 |
| 安全性 | 向导直接执行变更 | 优先只读审计；破坏性命令先生成可审查计划 |
| 可视化 | 菜单和对话框 | 系统、安全和存储实时仪表板 |
| 架构 | 大型过程式脚本 | UI 与系统、审计和规划逻辑分离 |
| 存储库检查 | 以部署为中心 | XFS、权限、SSH、防火墙和 Veeam 服务审计 |
| 维护方式 | 固定旧版依赖 | 使用 `pyproject.toml` 的现代 Python 打包方式 |
| 多语言 | 单一界面语言 | English、Español、Português、中文，可持久保存选择 |

## 当前功能

- 现代键盘操作终端仪表板。
- 内置语言选择器。
- 语言偏好保存在 `~/.config/vhrm/config.json`。
- 显示 Linux 发行版、内核、CPU、RAM 和根文件系统摘要。
- 使用 `lsblk` 盘点块设备。
- 安全性与就绪状态审计，包括：
  - Ubuntu 目标版本识别；
  - 防火墙管理器检测；
  - SSH 服务状态；
  - Veeam Transport 和 Immutability 服务状态；
  - 存储库目录是否存在；
  - `0700` 权限检查；
  - XFS 文件系统检测。
- 生成可审查的存储库配置计划。
- v0.1.x 系列不会自动格式化磁盘。

## 安装

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip xfsprogs
python3 -m venv .venv
source .venv/bin/activate
pip install .
vhrm
```

## 推荐运行模型

VHRM **不能替代** Veeam 官方文档或 Veeam Infrastructure Appliance。对于手动配置的 Linux 存储库，在投入生产前，应始终根据当前 Veeam Backup & Replication 的要求验证主机。

对于 Hardened Repository，应使用专用块存储；当需要 Fast Clone 时优先考虑 XFS。存储库所有权和权限、一次性凭据、防火墙策略、SSH 生命周期以及 Veeam 服务都应纳入变更管理流程。

## 路线图

- [ ] 带双重破坏性确认的引导式存储库配置。
- [ ] 格式化前通过序列号/WWN 识别设备。
- [ ] XFS/Reflink 验证。
- [ ] UFW/firewalld 策略检查器。
- [ ] SSH 暴露计时器和加入 Veeam 后的自动锁定助手。
- [ ] Veeam 组件和端口诊断。
- [ ] 存储容量和 inode 趋势。
- [ ] 面向 RMM/SIEM 的 JSON 审计导出。
- [ ] 在当前 Veeam 版本支持时加入 Debian/RHEL/Rocky 配置文件。
- [ ] `.deb` 打包以及 GitHub Actions 发布流程。

## 致谢

项目最初的理念和工作流程灵感来自：

- Thomas De Win (`tdewin`) 的 **veeamhubrepo** — https://github.com/tdewin/veeamhubrepo

VHRM 不复制原始 Python 实现。它是针对同一运维问题进行的独立、全新结构化实现。

## 免责声明

Veeam® 是 Veeam Software Group GmbH 的商标。本社区项目与 Veeam Software 无隶属、赞助或官方认可关系。

磁盘格式化、文件系统创建、防火墙变更和账户变更都可能导致数据丢失或无法访问。请验证所有命令，并首先在非生产环境中进行测试。

## 许可证

MIT。请参阅 [LICENSE](LICENSE)。
