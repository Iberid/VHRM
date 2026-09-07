# VHRM — Veeam Hardened Repository Manager

**Español** | [English](README.md) | [Português](README.pt-BR.md) | [中文](README.zh-CN.md)

Interfaz de terminal moderna y de código abierto para auditar y preparar sistemas Linux utilizados como **Veeam Hardened Repositories**.

> **Estado:** versión comunitaria inicial / vista previa técnica. Utilícela primero en laboratorios. Todo cambio de almacenamiento debe ser validado por un administrador.

## Por qué existe este proyecto

VHRM está inspirado en el flujo de trabajo de [`tdewin/veeamhubrepo`](https://github.com/tdewin/veeamhubrepo), un proyecto con licencia MIT creado para preparar rápidamente repositorios Linux inmutables en entornos de laboratorio de Veeam.

En lugar de extender su implementación de 2021 basada en `dialog`, VHRM es una **reimplementación independiente** centrada en una experiencia de usuario moderna y mantenible, con un modelo de seguridad de solo lectura primero.

## Mejoras principales

| Área | Enfoque de veeamhubrepo | Enfoque de VHRM |
|---|---|---|
| Interfaz | asistente clásico con dialog | dashboard TUI moderno con Textual |
| Base objetivo | Ubuntu 20.04 / era Veeam V11 | conocimiento de Ubuntu 20.04/22.04/24.04/26.04 |
| Seguridad | el asistente ejecuta cambios | auditoría primero; los comandos destructivos se generan como planes |
| Visibilidad | menús y cuadros de diálogo | panel en vivo de sistema, seguridad y almacenamiento |
| Arquitectura | script procedural grande | UI separada de la lógica de sistema, auditoría y planificación |
| Validaciones | orientadas a instalación | XFS, permisos, SSH, firewall y servicios Veeam |
| Mantenimiento | dependencias antiguas fijadas | empaquetado Python moderno con `pyproject.toml` |
| Idiomas | interfaz única | English, Español, Português y 中文 con selector persistente |

## Funciones actuales

- Dashboard moderno controlado por teclado.
- Selector de idioma integrado.
- El idioma seleccionado se guarda en `~/.config/vhrm/config.json`.
- Resumen de distribución Linux, kernel, CPU, RAM y sistema de archivos raíz.
- Inventario de dispositivos de bloque mediante `lsblk`.
- Auditoría de seguridad y preparación para:
  - versión objetivo de Ubuntu;
  - presencia de firewall;
  - estado de SSH;
  - servicios Veeam Transport e Immutability;
  - existencia del directorio del repositorio;
  - permisos `0700`;
  - detección de XFS.
- Generador de planes revisables para aprovisionamiento.
- La versión v0.1.x no formatea discos automáticamente.

## Instalación

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip xfsprogs
python3 -m venv .venv
source .venv/bin/activate
pip install .
vhrm
```

## Modelo operativo recomendado

VHRM **no sustituye** la documentación oficial de Veeam ni el Veeam Infrastructure Appliance. Para repositorios Linux configurados manualmente, valide siempre el host contra los requisitos actuales de Veeam Backup & Replication antes de utilizarlo en producción.

Para un repositorio hardened, utilice almacenamiento de bloques dedicado y prefiera XFS cuando se requiera Fast Clone. La propiedad y permisos del repositorio, credenciales de un solo uso, política de firewall, ciclo de vida de SSH y servicios de Veeam deben formar parte del control de cambios.

## Roadmap

- [ ] Aprovisionamiento guiado con doble confirmación destructiva.
- [ ] Identificación de dispositivos mediante serial/WWN antes del formateo.
- [ ] Validación XFS/Reflink.
- [ ] Inspector de políticas UFW/firewalld.
- [ ] Temporizador de exposición SSH y cierre posterior al onboarding.
- [ ] Diagnóstico de componentes y puertos Veeam.
- [ ] Tendencias de capacidad e inodos.
- [ ] Exportación JSON para RMM/SIEM.
- [ ] Perfiles Debian/RHEL/Rocky cuando estén soportados por versiones actuales de Veeam.
- [ ] Paquete `.deb` y pipeline de releases mediante GitHub Actions.

## Atribución

La idea original y la inspiración del flujo de trabajo provienen de:

- **veeamhubrepo** por Thomas De Win (`tdewin`) — https://github.com/tdewin/veeamhubrepo

VHRM no copia la implementación Python original. Es una implementación limpia e independiente inspirada en el mismo problema operativo.

## Descargo de responsabilidad

Veeam® es una marca comercial de Veeam Software Group GmbH. Este proyecto comunitario no está afiliado, patrocinado ni respaldado por Veeam Software.

El formateo de discos, creación de sistemas de archivos, cambios de firewall y cambios de cuentas pueden provocar pérdida de datos o acceso. Valide siempre los comandos y pruebe primero en un entorno no productivo.

## Licencia

MIT. Consulte [LICENSE](LICENSE).
