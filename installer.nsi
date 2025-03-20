; Instalador do Conversor de PDF
Unicode True

; Definições do instalador
!define APPNAME "Conversor de PDF"
!define COMPANYNAME "ale"
!define DESCRIPTION "Conversor de PDF com suporte a OCR"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

; Arquivos necessários para o instalador
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Configurações do instalador
Name "${APPNAME}"
OutFile "Conversor_de_PDF_Setup.exe"
InstallDir "$PROGRAMFILES64\${COMPANYNAME}\${APPNAME}"
InstallDirRegKey HKCU "Software\${COMPANYNAME}\${APPNAME}" ""
RequestExecutionLevel admin

; Interface do instalador
!define MUI_ABORTWARNING
!define MUI_ICON "$%SystemRoot%\System32\shell32.dll,1"
!define MUI_UNICON "$%SystemRoot%\System32\shell32.dll,1"

; Páginas do instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas da desinstalação
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Idiomas
!insertmacro MUI_LANGUAGE "PortugueseBR"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    
    ; Arquivos do programa
    File /r "dist\Conversor de PDF\*.*"
    
    ; Criar atalho no menu iniciar
    CreateDirectory "$SMPROGRAMS\${COMPANYNAME}"
    CreateShortcut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\Conversor de PDF.exe"
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\Conversor de PDF.exe"
    
    ; Registro de desinstalação
    WriteUninstaller "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$INSTDIR\Conversor de PDF.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    
    ; Tamanho do programa instalado
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "EstimatedSize" "$0"
SectionEnd

Section "Uninstall"
    ; Remover arquivos do programa
    RMDir /r "$INSTDIR"
    
    ; Remover atalhos
    Delete "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${COMPANYNAME}"
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    ; Remover registro de desinstalação
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}"
SectionEnd 