; Configuração básica
Name "Conversor de PDF"
OutFile "Setup.exe"
InstallDir "$PROGRAMFILES64\Conversor de PDF"

; Interface básica
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

; Seção principal
Section "Instalação"
    SetOutPath "$INSTDIR"
    File /r "src\dist\Conversor de PDF\*.*"
    
    CreateDirectory "$SMPROGRAMS\Conversor de PDF"
    CreateShortCut "$SMPROGRAMS\Conversor de PDF\Conversor de PDF.lnk" "$INSTDIR\Conversor de PDF.exe"
    CreateShortCut "$DESKTOP\Conversor de PDF.lnk" "$INSTDIR\Conversor de PDF.exe"
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\uninstall.exe"
    Delete "$SMPROGRAMS\Conversor de PDF\Conversor de PDF.lnk"
    Delete "$DESKTOP\Conversor de PDF.lnk"
    
    RMDir "$SMPROGRAMS\Conversor de PDF"
    RMDir /r "$INSTDIR"
SectionEnd