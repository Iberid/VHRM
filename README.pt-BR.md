# VHRM — Veeam Hardened Repository Manager

[English](README.md) | [Español](README.es.md) | **Português** | [中文](README.zh-CN.md)

Interface de terminal moderna e de código aberto para auditar e preparar sistemas Linux usados como **Veeam Hardened Repositories**.

> **Status:** versão comunitária inicial / prévia técnica. Use primeiro em laboratórios. Qualquer alteração de armazenamento deve ser validada por um administrador.

## Por que este projeto existe

VHRM é inspirado no fluxo de trabalho do [`tdewin/veeamhubrepo`](https://github.com/tdewin/veeamhubrepo), um projeto sob licença MIT criado para preparar rapidamente repositórios Linux imutáveis em ambientes de laboratório Veeam.

Em vez de estender sua implementação de 2021 baseada em `dialog`, o VHRM é uma **reimplementação independente**, focada em uma experiência moderna e sustentável, com um modelo de segurança read-first.

## Principais melhorias

| Área | Abordagem do veeamhubrepo | Abordagem do VHRM |
|---|---|---|
| Interface | assistente clássico com dialog | dashboard TUI moderno com Textual |
| Base alvo | Ubuntu 20.04 / era Veeam V11 | reconhecimento de Ubuntu 20.04/22.04/24.04/26.04 |
| Segurança | o assistente executa mudanças | auditoria primeiro; comandos destrutivos são planos revisáveis |
| Visibilidade | menus e diálogos | painel ao vivo de sistema, segurança e armazenamento |
| Arquitetura | script procedural grande | UI separada da lógica de sistema, auditoria e planejamento |
| Verificações | orientadas à instalação | XFS, permissões, SSH, firewall e serviços Veeam |
| Manutenção | dependências antigas fixadas | empacotamento Python moderno com `pyproject.toml` |
| Idiomas | interface única | English, Español, Português e 中文 com seletor persistente |

## Recursos atuais

- Dashboard moderno controlado por teclado.
- Seletor de idioma integrado.
- O idioma escolhido é salvo em `~/.config/vhrm/config.json`.
- Resumo da distribuição Linux, kernel, CPU, RAM e sistema de arquivos raiz.
- Inventário de dispositivos de bloco através do `lsblk`.
- Auditoria de segurança e prontidão para:
  - versão alvo do Ubuntu;
  - presença de firewall;
  - estado do SSH;
  - serviços Veeam Transport e Immutability;
  - existência do diretório do repositório;
  - permissões `0700`;
  - detecção de XFS.
- Gerador de planos revisáveis para provisionamento.
- A série v0.1.x não formata discos automaticamente.

## Instalação

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip xfsprogs
python3 -m venv .venv
source .venv/bin/activate
pip install .
vhrm
```

## Modelo operacional recomendado

O VHRM **não substitui** a documentação oficial da Veeam nem o Veeam Infrastructure Appliance. Para repositórios Linux configurados manualmente, valide sempre o host com os requisitos atuais do Veeam Backup & Replication antes do uso em produção.

Para um repositório hardened, utilize armazenamento em bloco dedicado e prefira XFS quando Fast Clone for necessário. Propriedade e permissões do repositório, credenciais de uso único, política de firewall, ciclo de vida do SSH e serviços Veeam devem fazer parte do controle de mudanças.

## Roadmap

- [ ] Provisionamento guiado com confirmação destrutiva em duas etapas.
- [ ] Identificação de dispositivos por serial/WWN antes da formatação.
- [ ] Validação XFS/Reflink.
- [ ] Inspetor de políticas UFW/firewalld.
- [ ] Temporizador de exposição SSH e bloqueio após onboarding.
- [ ] Diagnóstico de componentes e portas Veeam.
- [ ] Tendências de capacidade e inodes.
- [ ] Exportação JSON para RMM/SIEM.
- [ ] Perfis Debian/RHEL/Rocky quando suportados por versões atuais do Veeam.
- [ ] Pacote `.deb` e pipeline de releases com GitHub Actions.

## Atribuição

A ideia original e a inspiração do fluxo de trabalho vieram de:

- **veeamhubrepo** por Thomas De Win (`tdewin`) — https://github.com/tdewin/veeamhubrepo

O VHRM não copia a implementação Python original. É uma implementação limpa e independente inspirada no mesmo problema operacional.

## Aviso legal

Veeam® é uma marca comercial da Veeam Software Group GmbH. Este projeto comunitário não é afiliado, patrocinado ou endossado pela Veeam Software.

Formatação de discos, criação de sistemas de arquivos, alterações de firewall e contas podem causar perda de dados ou de acesso. Valide todos os comandos e teste primeiro em ambiente não produtivo.

## Licença

MIT. Consulte [LICENSE](LICENSE).
