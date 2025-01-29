# Automatisere med Python skript

Begge oppgave skal fjerne manuelt arbeid og unngå feil.

Skriptene skal ha ta mappenavn som argument (og mappene inneholder alltid
undermappen "config" og filen "versions.yaml").


## Oppgave 1

Konvertere version.yaml til nytt format for MPS174 / MPS179:

Fra

  MPS179_BridgePanel:
    Version: 1.12.0
    SerialNrs:
      - 2401063
      - 2401087
      - 2401095
      - 2401096
      - 2401101
  MPS179_BridgePanelDisplay:
    Version: 1.10.0
  MPS174_BridgePanel:
    Version: 1.0.0

Til

  BridgeControlPanel01:
    SerialNr: 2401063
    MPS174:
      Version: 1.0.0
    MPS179:
      Version: 1.12.0
    MPS179_Display:
      Version: 1.10.0

og så videre - for alle thrustere.

## Oppgave 2

Sjekke at versions.yaml og config-mappe er konsistent
