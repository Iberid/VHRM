from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Español",
    "pt-BR": "Português (Brasil)",
    "zh-CN": "中文（简体）",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "VHRM — Veeam Hardened Repository Manager",
        "manager_title": "Modern Linux Hardened Repository Manager",
        "hero_subtitle": "Read-first dashboard · security audit · storage visibility · Veeam readiness",
        "language": "Language",
        "system": "SYSTEM",
        "audit": "AUDIT",
        "veeam": "VEEAM",
        "security_audit": "Security audit",
        "storage": "Storage",
        "about": "About",
        "status": "Status",
        "check": "Check",
        "detail": "Detail",
        "device": "Device",
        "size": "Size",
        "type": "Type",
        "filesystem": "Filesystem",
        "mount": "Mount",
        "model": "Model",
        "pass": "pass",
        "warnings": "warnings",
        "refresh_hint": "Press R to refresh",
        "not_detected": "Not detected",
        "quit": "Quit",
        "refresh": "Refresh",
        "about_text": "VHRM is a community project for auditing and preparing Linux hosts used as Veeam Hardened Repositories. It is not affiliated with or endorsed by Veeam Software.\n\nDestructive storage actions are intentionally represented as reviewable plans. The operator remains responsible for validating device names, backups and change control.",
    },
    "es": {
        "app_title": "VHRM — Administrador de Repositorios Hardened para Veeam",
        "manager_title": "Administrador moderno de repositorios Linux Hardened",
        "hero_subtitle": "Panel de solo lectura · auditoría de seguridad · almacenamiento · preparación para Veeam",
        "language": "Idioma",
        "system": "SISTEMA",
        "audit": "AUDITORÍA",
        "veeam": "VEEAM",
        "security_audit": "Auditoría de seguridad",
        "storage": "Almacenamiento",
        "about": "Acerca de",
        "status": "Estado",
        "check": "Comprobación",
        "detail": "Detalle",
        "device": "Dispositivo",
        "size": "Tamaño",
        "type": "Tipo",
        "filesystem": "Sistema de archivos",
        "mount": "Montaje",
        "model": "Modelo",
        "pass": "correctos",
        "warnings": "advertencias",
        "refresh_hint": "Presione R para actualizar",
        "not_detected": "No detectado",
        "quit": "Salir",
        "refresh": "Actualizar",
        "about_text": "VHRM es un proyecto comunitario para auditar y preparar hosts Linux utilizados como Veeam Hardened Repositories. No está afiliado, patrocinado ni respaldado por Veeam Software.\n\nLas acciones destructivas sobre almacenamiento se representan deliberadamente como planes revisables. El operador sigue siendo responsable de validar los dispositivos, las copias de seguridad y el control de cambios.",
    },
    "pt-BR": {
        "app_title": "VHRM — Gerenciador de Repositórios Hardened para Veeam",
        "manager_title": "Gerenciador moderno de repositórios Linux Hardened",
        "hero_subtitle": "Painel somente leitura · auditoria de segurança · armazenamento · preparação para Veeam",
        "language": "Idioma",
        "system": "SISTEMA",
        "audit": "AUDITORIA",
        "veeam": "VEEAM",
        "security_audit": "Auditoria de segurança",
        "storage": "Armazenamento",
        "about": "Sobre",
        "status": "Status",
        "check": "Verificação",
        "detail": "Detalhe",
        "device": "Dispositivo",
        "size": "Tamanho",
        "type": "Tipo",
        "filesystem": "Sistema de arquivos",
        "mount": "Montagem",
        "model": "Modelo",
        "pass": "aprovados",
        "warnings": "alertas",
        "refresh_hint": "Pressione R para atualizar",
        "not_detected": "Não detectado",
        "quit": "Sair",
        "refresh": "Atualizar",
        "about_text": "VHRM é um projeto comunitário para auditar e preparar hosts Linux usados como Veeam Hardened Repositories. Não é afiliado, patrocinado ou endossado pela Veeam Software.\n\nAções destrutivas de armazenamento são intencionalmente representadas como planos revisáveis. O operador continua responsável por validar dispositivos, backups e o controle de mudanças.",
    },
    "zh-CN": {
        "app_title": "VHRM — Veeam 强化存储库管理器",
        "manager_title": "现代 Linux 强化存储库管理器",
        "hero_subtitle": "只读优先仪表板 · 安全审计 · 存储可视化 · Veeam 就绪检查",
        "language": "语言",
        "system": "系统",
        "audit": "审计",
        "veeam": "VEEAM",
        "security_audit": "安全审计",
        "storage": "存储",
        "about": "关于",
        "status": "状态",
        "check": "检查项",
        "detail": "详细信息",
        "device": "设备",
        "size": "容量",
        "type": "类型",
        "filesystem": "文件系统",
        "mount": "挂载点",
        "model": "型号",
        "pass": "通过",
        "warnings": "警告",
        "refresh_hint": "按 R 刷新",
        "not_detected": "未检测到",
        "quit": "退出",
        "refresh": "刷新",
        "about_text": "VHRM 是一个社区项目，用于审计和准备作为 Veeam Hardened Repository 使用的 Linux 主机。本项目与 Veeam Software 无隶属、赞助或官方认可关系。\n\n具有破坏性的存储操作会刻意以可审查的计划形式呈现。操作人员仍需负责核实设备名称、备份状态以及变更控制流程。",
    },
}


def config_path() -> Path:
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "vhrm" / "config.json"


def load_language() -> str:
    try:
        data = json.loads(config_path().read_text(encoding="utf-8"))
        language = str(data.get("language", DEFAULT_LANGUAGE))
        return language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    except (OSError, ValueError, TypeError):
        return DEFAULT_LANGUAGE


def save_language(language: str) -> None:
    if language not in SUPPORTED_LANGUAGES:
        return
    path = config_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"language": language}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        # Language selection should still work for the current session on read-only systems.
        pass


def tr(language: str, key: str) -> str:
    selected = TRANSLATIONS.get(language, TRANSLATIONS[DEFAULT_LANGUAGE])
    return selected.get(key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))
