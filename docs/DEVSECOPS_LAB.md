# DevSecOps Lab — проверки безопасности для Linux Incident Lab

Этот практикум дополняет [основной стенд](../README.md). Цель — собрать минимальный **security gate** в CI и научиться разбирать результаты, а не просто получать зелёный значок.

> Это учебный локальный HTTP-сервис, а не production-приложение. Автоматические проверки не гарантируют отсутствие уязвимостей.

## Что проверяем

| Проверка | Инструмент | На что смотрит |
|---|---|---|
| Корректность работы | `unittest` | Сценарии HTTP 200 и 503 |
| Синтаксис диагностики | `bash -n` | Синтаксис `diagnose.sh` без выполнения |
| SAST | [Bandit](https://bandit.readthedocs.io/en/latest/) | Известные подозрительные конструкции в `demo_service.py` (порог medium/high) |
| SCA | [pip-audit](https://github.com/pypa/pip-audit) | Опубликованные уязвимости в `security/requirements-tools.txt` и разрешённых зависимостях инструментов |
| CI hardening | GitHub Actions | `contents: read`, SHA-pinning внешних actions, отсутствие секретов и `pull_request_target` |

**Границы SCA:** сам `demo_service.py` использует только стандартную библиотеку Python; его сторонних runtime-зависимостей нет. Поэтому `pip-audit` проверяет инструменты Bandit/pip-audit и их зависимости, **не** безопасность Python, Linux, Bash или HTTP-сервера в целом. Если в будущем появятся зависимости самого сервиса, добавьте их в отдельный файл и отдельную проверку.

## 1. Запуск на своём компьютере

Нужны Python 3.11+, Git и подключение к PyPI для установки инструментов и аудита зависимостей. В Linux / WSL из корня репозитория:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r security/requirements-tools.txt

python -m unittest discover -s tests -v
bash -n diagnose.sh
python -m bandit -ll demo_service.py
python -m pip_audit -r security/requirements-tools.txt

deactivate
```

В Windows PowerShell активация окружения: `.venv\Scripts\Activate.ps1`. `bash -n` запускайте в WSL/Git Bash. Файл `.venv/` не должен попадать в коммиты.

## 2. Найти проверку в GitHub Actions

Откройте [DevSecOps security checks](../.github/workflows/devsecops-security.yml) и раздел **Actions** репозитория. Workflow запускается на push в `main`, pull request и вручную через `Run workflow`. GitHub Actions использует одноразовый Ubuntu runner.

Если проверка стала красной, откройте упавший шаг. Найдите **имя файла, строку, тип предупреждения, пакет, версию и идентификатор CVE/PYSEC**, если они выведены инструментом. Не отключайте проверку ради зелёного статуса.

## 3. Мини-практикум: вручную проверить опасный код

Создайте файл **за пределами репозитория**, например `/tmp/bandit-example.py`, с таким учебным примером:

```python
import subprocess
command = input("Command: ")
subprocess.run(command, shell=True)
```

Команда:

```bash
python -m bandit -ll /tmp/bandit-example.py
```

Bandit должен отметить опасное сочетание пользовательского ввода и `shell=True` (B602). **Не запускайте сам пример**: проверяйте только исходный файл через Bandit. Никогда не передавайте пользовательский ввод в shell. Исправленный локальный вариант:

```python
import subprocess
subprocess.run(["echo", "example"], check=True)
```

Снова запустите Bandit и сравните результат. **Не добавляйте** уязвимый пример в публичный репозиторий.

## 4. Что делать с находкой

1. Установить, подтверждается ли риск в конкретном контексте (инструменты иногда ошибаются).
2. Для зависимостей — найти безопасную версию, изучить advisory и влияние обновления.
3. Сделать минимальное исправление, не отключая проверку без задокументированной причины.
4. Перезапустить unit-тесты, SAST и аудит зависимостей.
5. В PR описать исходную проблему, шаги воспроизведения и фактически полученный результат.

## 5. Базовый чеклист безопасности стенда

- [x] В коде стенда указан loopback-адрес `127.0.0.1`, а не `0.0.0.0`.
- [x] Диагностика выполняется без `sudo` и не меняет системные настройки.
- [x] Токен GitHub Actions ограничен правом `contents: read`.
- [x] Внешние actions закреплены на полные commit SHA.
- [x] Существуют команды для unit-тестов, SAST и SCA.
- [ ] Выполнить все проверки лично и сохранить дату и версию окружения.
- [ ] Провести ручной обзор обработчиков HTTP, входных данных и управления ошибками.

Не сохраняйте реальные пароли, токены, личные данные и логи клиентских систем в коде, примерах или артефактах CI.

## Официальные материалы

- [GitHub — Secure use of GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use)
- [Bandit — документация](https://bandit.readthedocs.io/en/latest/)
- [pip-audit — документация](https://github.com/pypa/pip-audit)
- [OWASP — CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)
