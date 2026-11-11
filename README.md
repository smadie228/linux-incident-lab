<div align="center">

# 🐧 Linux Incident Lab
**Linux · Bash · Incident Diagnostics**

![Linux](https://img.shields.io/badge/Linux-lab-152a3b?style=flat-square&logo=linux&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-read--only%20diagnostics-147d86?style=flat-square&logo=gnubash&logoColor=white)
![HTTP](https://img.shields.io/badge/HTTP-200%20%7C%20503%20%7C%20timeout-152a3b?style=flat-square)
![Status](https://img.shields.io/badge/status-learning%20lab-53677b?style=flat-square)
[![DevSecOps security checks](https://github.com/smadie228/linux-incident-lab/actions/workflows/devsecops-security.yml/badge.svg)](https://github.com/smadie228/linux-incident-lab/actions/workflows/devsecops-security.yml)

[← GitHub-профиль](https://github.com/smadie228) · [Service Checker](https://github.com/smadie228/service-checker)

</div>

---

## `01 / Назначение`

Локальный учебный стенд для начинающего инженера IT Support / Linux. Он специально моделирует успешный ответ, HTTP 503 и медленный ответ сервиса. Цель — научиться **собирать диагностические данные**, проверять гипотезы и оформлять учебные инциденты.

Все инциденты **симулированы**. Это не реальная эксплуатация production и не обращения клиентов.

## `02 / Сценарии`

| Режим | Поведение сервиса | Что наблюдаем |
|---|---|---|
| `healthy` | HTTP 200 | доступность сервиса |
| `error` | HTTP 503 | отказ на уровне HTTP |
| `slow` | задержка 4 секунды | таймаут `curl` при лимите 2 секунды |

## `03 / Запуск на Linux или WSL`

Нужны **Python 3.10+**, Bash и `curl`.

**Терминал 1:**

```bash
python3 demo_service.py --mode healthy --port 8080
```

**Терминал 2:**

```bash
curl -i http://127.0.0.1:8080/health
bash diagnose.sh 8080
```

Останови сервис через `Ctrl+C`, затем запускай другие сценарии по одному:

```bash
python3 demo_service.py --mode error
# после остановки
python3 demo_service.py --mode slow
```

**Что собирает `diagnose.sh`:** дату, версию ядра, HTTP-код, задержку, список TCP listeners, данные о памяти и диске. Скрипт не требует `sudo` и не изменяет системные настройки.

## `04 / Тесты и CI`

```bash
python3 -m unittest discover -s tests -v
bash -n diagnose.sh
```

Конфигурация [GitHub Actions](.github/workflows/linux-lab-tests.yml) проверяет Python unit-тесты и синтаксис Bash из корня нового репозитория. Выполнение проверок на собственной Linux-машине следует подтвердить отдельно.

**DevSecOps:** дополнительный [security workflow](.github/workflows/devsecops-security.yml) запускает те же тесты, Bandit (SAST) и pip-audit (SCA), использует токен только для чтения и закреплённые commit SHA внешних actions. [Пошаговый практикум с командами и ограничениями проверок](docs/DEVSECOPS_LAB.md).

## `05 / Документация`

- [INC-DEMO-001 — HTTP 503](docs/INC-001.md)
- [INC-DEMO-002 — таймаут](docs/INC-002.md)
- [Жизненный цикл учебного инцидента в Jira](docs/JIRA_WORKFLOW.md)
- [План изучения Active Directory](docs/ACTIVE_DIRECTORY.md)
- [DevSecOps-практикум: SAST, SCA и GitHub Actions](docs/DEVSECOPS_LAB.md)

## `06 / Дальнейшая практика`

- Воспроизвести три режима на собственной Linux-VM и записать результаты.
- Добавить учебные сценарии с `systemd`, `journalctl` и сетевой диагностикой.
- Изучать безопасность Linux и DevSecOps на изолированном стенде.

---

<div align="center"><sub>Learning by doing · <a href="https://github.com/smadie228">@smadie228</a></sub></div>
