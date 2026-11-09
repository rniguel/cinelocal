; CineLocal - Script de Instalador Inno Setup Oficial (Windows)
; Gera o arquivo: CineLocal-Setup-v2.5.exe

#define MyAppName "CineLocal"
#define MyAppVersion "2.5.0"
#define MyAppPublisher "CineLocal Project"
#define MyAppURL "https://github.com/rniguel/cinelocal"
#define MyAppExeName "CineLocal.exe"

[Setup]
; Informações básicas do aplicativo
AppId={{9F82A7C4-13B2-498C-B8E5-3A25D7E08861}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\LEIAME.md
PrivilegesRequired=lowest
OutputDir=..\dist\installer
OutputBaseFilename=CineLocal-Setup-v{#MyAppVersion}
SetupIconFile=..\app\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Criar atalho na Barra de Tarefas"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Binário principal e arquivos do projeto
Source: "..\dist\CineLocal\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\app\icon.ico"; DestDir: "{app}\app"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app\icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\app\data\torrent_cache"
Type: filesandordirs; Name: "{app}\app\data\browser_profile"
