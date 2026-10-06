#define AppVersion "0.2.0"
#define AppName "BİÇEB"

[Setup]
AppId={{33EB8450-7F48-4988-8C7C-38A26AEE7E90}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=BİÇEB Project
DefaultDirName={localappdata}\Programs\BICEB
DefaultGroupName={#AppName}
OutputDir=..\..\dist\installers
OutputBaseFilename=BICEB-{#AppVersion}-windows-x64-setup
SetupIconFile=..\..\biceb\resources\biodiversity.ico
UninstallDisplayIcon={app}\BICEB.exe
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "tr"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\..\dist\BICEB\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\BICEB.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\BICEB.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\BICEB.exe"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
