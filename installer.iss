; Files-On - Script de Instalacao Inno Setup
; Gera um instalador.exe profissional igual Chrome/WhatsApp

#define MyAppName "Files-On"
#define MyAppVersion "1.0"
#define MyAppPublisher "Files-On Team"
#define MyAppURL "https://github.com/rufinogmr/Files-on"
#define MyAppExeName "Files-On.exe"

[Setup]
AppId={{F1L3S0N-0000-0000-0000-000000000001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer
OutputBaseFilename=Files-On-Instalador
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na &Area de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LEIA-ME.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "INSTALACAO_SIMPLES.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Leia-me"; Filename: "{app}\LEIA-ME.txt"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
var
  TesseractPage: TInputDirWizardPage;
  DownloadPage: TDownloadWizardPage;

procedure InitializeWizard;
begin
  // Pagina customizada para Tesseract
  TesseractPage := CreateInputDirPage(wpSelectDir,
    'Instalar Dependencias', 'O Files-On precisa de componentes adicionais',
    'O aplicativo precisa do Tesseract OCR e Poppler para funcionar.' + #13#10 + #13#10 +
    'Clique em Proximo para continuar. As paginas de download serao abertas automaticamente.',
    False, '');
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  ErrorCode: Integer;
begin
  Result := True;

  if CurPageID = TesseractPage.ID then
  begin
    // Verificar se Tesseract esta instalado
    if not FileExists('C:\Program Files\Tesseract-OCR\tesseract.exe') then
    begin
      if MsgBox('Tesseract OCR nao encontrado. Deseja baixar agora?', mbConfirmation, MB_YESNO) = IDYES then
      begin
        ShellExec('open', 'https://github.com/UB-Mannheim/tesseract/wiki', '', '', SW_SHOW, ewNoWait, ErrorCode);
        MsgBox('Por favor:' + #13#10 +
               '1. Baixe e instale o Tesseract' + #13#10 +
               '2. Durante instalacao, marque "Portuguese"' + #13#10 +
               '3. Execute este instalador novamente', mbInformation, MB_OK);
        Result := False;
      end;
    end;

    // Verificar se Poppler esta instalado
    if Result and not FileExists('C:\Program Files\poppler\Library\bin\pdftoppm.exe') then
    begin
      if MsgBox('Poppler nao encontrado. Deseja baixar agora?', mbConfirmation, MB_YESNO) = IDYES then
      begin
        ShellExec('open', 'https://github.com/oschwartz10612/poppler-windows/releases/', '', '', SW_SHOW, ewNoWait, ErrorCode);
        MsgBox('Por favor:' + #13#10 +
               '1. Baixe o arquivo Release-XX.XX.X-0.zip' + #13#10 +
               '2. Extraia para C:\Program Files\poppler' + #13#10 +
               '3. Execute este instalador novamente', mbInformation, MB_OK);
        Result := False;
      end;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  Path: string;
begin
  if CurStep = ssPostInstall then
  begin
    // Adicionar Poppler ao PATH
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path) then
    begin
      if Pos('poppler', Path) = 0 then
      begin
        Path := Path + ';C:\Program Files\poppler\Library\bin';
        RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path);
      end;
    end;
  end;
end;
