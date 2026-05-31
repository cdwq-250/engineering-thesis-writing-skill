# Publishing To GitHub

This repository is intended to be public, but only after local safety checks pass.

## 1. Authenticate GitHub CLI

Run in PowerShell:

```powershell
gh auth login
gh auth status
```

Recommended choices:

- Git protocol: `HTTPS`
- Authenticate Git with GitHub credentials: `Yes`
- Authentication method: browser login

If an old token is broken, reset it first:

```powershell
gh auth logout -h github.com -u cdwq-250
gh auth login -h github.com
```

## 2. Run Local Verification

From repository root:

```powershell
python engineering-thesis-zh\scripts\check_public_safety.py .
python C:\Users\HP\.codex\skills\.system\skill-creator\scripts\quick_validate.py D:\desktop\毕设\1\engineering-thesis-writing-skill\engineering-thesis-zh
git status --short
```

Expected:

- public safety check passes
- skill is valid
- git working tree is clean

## 3. Create The Public Repository

From repository root:

```powershell
gh repo create engineering-thesis-writing-skill --public --source . --remote origin --push
```

If the remote already exists:

```powershell
git remote add origin https://github.com/cdwq-250/engineering-thesis-writing-skill.git
git push -u origin master
```

## 4. Verify Remote Contents

After pushing:

```powershell
gh repo view cdwq-250/engineering-thesis-writing-skill --web
```

Confirm the remote does not contain:

- thesis PDFs
- CAJ/KDH files
- DOC/DOCX source theses
- OCR or extracted full text
- long verbatim thesis passages
- database credentials or session details

## 5. Resume Corpus Work

After publishing, continue local corpus analysis by placing legally obtained PDFs under:

```text
private_corpus/software/
private_corpus/control/
private_corpus/mechanical/
```

Then run:

```powershell
python engineering-thesis-zh\scripts\run_corpus_pipeline.py
```

