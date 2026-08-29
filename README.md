# Pi R Setup Assist — Downloads

Official installers for **Pi R Setup Assist**, the setup helper for Pi R Academy courses.
The app checks whether your computer meets the course requirements, installs the tools the
course needs, and can update itself from inside the app.

## Download

Always use the links below. They point at the newest release, so they never change.

| Platform | Download | Notes |
|---|---|---|
| **macOS** 14 or later | [PiRSetupAssist-macOS.zip](../../releases/latest/download/PiRSetupAssist-macOS.zip) | Signed and notarized by Apple |
| **Windows** 10 build 1809 or later | [PiRSetupAssist-Windows.exe](../../releases/latest/download/PiRSetupAssist-Windows.exe) | **Recommended.** Just download and run |
| Windows (alternative) | [PiRSetupAssist-Windows.zip](../../releases/latest/download/PiRSetupAssist-Windows.zip) | For machines where policy blocks `.exe` files |

You can also browse every version on the [Releases](../../releases) page.

## Which course, and what your computer needs

The app supports two courses and checks the right requirements for whichever one you pick.

| Course | What it needs |
|---|---|
| **Claude Code** — Vibe Coding for Business | 4 GB RAM (8 GB recommended), 10 GB free |
| **Claude Cowork** — Agentic AI for Smart Working | 20 GB free (25 GB recommended). On macOS, an Apple Silicon Mac. On Windows, Hyper-V has to be switched on, and Windows Home only works partly |

Both courses need a Claude plan of Pro or above. The app cannot check that for you.

## How to install

**macOS** Unzip the file and drag `PiRSetupAssist.app` into your Applications folder, then open it.

**Windows** Download the `.exe` and double click it. Nothing to unzip, and nothing needs to be
installed first: .NET and the Windows App Runtime are bundled inside.
Windows may show a SmartScreen warning the first time because the file came from the internet.
Choose **More info**, then **Run anyway**.

If you use the `.zip` instead, extract **all** of it first, then run `Pi R Setup Assist` from the
extracted folder. Running it directly from inside the zip will fail.

## About the source code

This repository holds installers only. It contains no application source code.
The "Source code (zip / tar.gz)" links that GitHub attaches to every release therefore
contain nothing but this README file. GitHub adds those links automatically to every tag and
they cannot be turned off. The application source lives in a private company repository and is
not available for download.

© PI R SQUARE CO., LTD.
